"""Live demo: mark statute spans with a model and watch the checks run.

  python3 demo/server.py            then open http://localhost:5000

One page. Choose a model and a number of runs, press Run, and each provision
appears as the model returns it: its spans highlighted in the statute's own
words, checked word for word and re-parsed. When a run ends, the marks are
turned into a value for each tax year and set beside the value this project
uses (mostly the Department of Revenue's) and the value in PolicyEngine's
Colorado model. Repeat runs show how stable the model's marks are.

The server itself is standard-library Python. Marking needs Python 3.10+ and
`pip install -r requirements.txt` (LangExtract, and the Anthropic SDK for
Claude models). Keys are read from the environment and never sent to the page:
  ANTHROPIC_API_KEY     Claude models (COTAX_CLAUDE_API_KEY is read first, if set)
  LANGEXTRACT_API_KEY   Gemini models
With no key, the replay still works: it plays back the reference marks stored
in extractions/extractions.json, which a language model made earlier and no
person has reviewed. It shows the pipeline and says nothing new about a model.

PolicyEngine's two Colorado parameter files are fetched from its public
repository when first needed, not copied into this one (it is AGPL-3.0). If
they cannot be reached, that column says so.

Anyone who can open the page can spend the key's money, so there are limits,
all settable in the environment:
  DEMO_ACCESS_CODE   if set, a run must supply it
  DEMO_MAX_RUNS      most runs per job (default 3)
  DEMO_MAX_CALLS     most model calls this server will make before it must be
                     restarted (default 300); cached results do not count
  DEMO_WORKERS       provisions marked at once (default 4)
  PORT               default 5000
One job runs at a time.
"""
import hmac
import json
import os
import pathlib
import queue
import sys
import re
import threading
import urllib.request
from collections import Counter
from decimal import Decimal
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import engine.co_rules  # noqa: E402,F401  (registers the rules build_web expects)
from engine.core import Parameters  # noqa: E402
from tools import build_web, evaluate  # noqa: E402
from tools.textlib import attach_cross_refs, index, load_sections  # noqa: E402

PORT = int(os.environ.get("PORT", "5000"))
MAX_RUNS = max(1, int(os.environ.get("DEMO_MAX_RUNS", "3")))
MAX_CALLS = max(0, int(os.environ.get("DEMO_MAX_CALLS", "300")))
WORKERS = max(1, int(os.environ.get("DEMO_WORKERS", "4")))
ACCESS_CODE = os.environ.get("DEMO_ACCESS_CODE", "")

STAND_IN = "stand-in"
CLAUDE_MODELS = [
    ("claude-opus-5-5", "Claude Opus 5.5"),
    ("claude-sonnet-5-5", "Claude Sonnet 5.5"),
    ("claude-haiku-5-5", "Claude Haiku 5.5"),
]
GEMINI_MODELS = [("gemini-3.5-flash", "Gemini 3.5 Flash")]

STATIC = {
    "/": (ROOT / "demo" / "index.html", "text/html; charset=utf-8"),
    "/viewer/": (ROOT / "web" / "index.html", "text/html; charset=utf-8"),
}
ASSET_ROOT = (ROOT / "web" / "assets").resolve()
TYPES = {".css": "text/css", ".js": "application/javascript", ".svg": "image/svg+xml",
         ".woff2": "font/woff2", ".woff": "font/woff", ".ttf": "font/ttf", ".png": "image/png", ".jpg": "image/jpeg"}

state_lock = threading.Lock()
state = {"job": None, "calls_made": 0, "next_id": 1}
engine = {"lx": None, "version": None, "env": None, "error": None, "extract": None}
engine_lock = threading.Lock()


def load_engine():
    """Import the extraction script and LangExtract once. Returns an error string or None."""
    with engine_lock:
        if engine["env"] is not None or engine["error"]:
            return engine["error"]
        if sys.version_info < (3, 10):
            engine["error"] = "Marking needs Python 3.10 or later; this is %s." % sys.version.split()[0]
            return engine["error"]
        try:
            from tools import extract_langextract as extract
            lx, version = extract.load_langextract()
        except ImportError:
            engine["error"] = "LangExtract is not installed. Run: pip install -r requirements.txt"
            return engine["error"]
        engine.update(lx=lx, version=version, extract=extract, env=extract.setup(lx))
        return None


def claude_key():
    return os.environ.get("COTAX_CLAUDE_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")


def available_models():
    """Every model the page offers, with whether it can run and why not."""
    have_anthropic = True
    try:
        import anthropic  # noqa: F401
    except ImportError:
        have_anthropic = False
    models = [{"id": STAND_IN, "label": "Replay of the stored reference marks (no key, no cost)", "ready": True, "why": ""}]
    for model_id, label in CLAUDE_MODELS:
        why = ("" if claude_key() and have_anthropic else
               "the Anthropic SDK is not installed" if claude_key() else "ANTHROPIC_API_KEY is not set")
        models.append({"id": model_id, "label": label, "ready": not why, "why": why})
    for model_id, label in GEMINI_MODELS:
        why = "" if os.environ.get("LANGEXTRACT_API_KEY") else "LANGEXTRACT_API_KEY is not set"
        models.append({"id": model_id, "label": label, "ready": not why, "why": why})
    return models


def corpus():
    """The provisions a run can cover."""
    sections = load_sections()
    by_id = index(sections)
    config = json.loads(evaluate.CONFIG.read_text(encoding="utf-8"))
    examples = set(config["example_provisions"])
    texts = {pid: p["text"] for pid, p in by_id.items() if p["text"]}
    cite = {p["id"]: s["citation"] + p["label"] for s in sections for p in s["provisions"]}
    classes = json.loads(evaluate.REFERENCE.read_text(encoding="utf-8"))["classes"]
    targets = [pid for pid in sorted(texts) if pid not in examples]
    return {
        "targets": targets, "texts": texts, "cite": cite, "classes": classes,
        "core": [pid for pid in targets if pid in set(config["core_provisions"])],
        "examples": [g for g in json.loads(evaluate.REFERENCE.read_text(encoding="utf-8"))["groups"]
                     if g["provision"] in examples],
    }


CORPUS = corpus()

YEARS = range(2022, 2028)
PARAMETERS = [("co.eitc.match_rate", "Earned income credit, as a share of the federal credit"),
              ("co.income_tax.rate_schedule", "Income tax rate")]
POLICYENGINE = {
    "co.eitc.match_rate": "https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/"
                          "policyengine_us/parameters/gov/states/co/tax/income/credits/eitc/match.yaml",
    "co.income_tax.rate_schedule": "https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/"
                                   "policyengine_us/parameters/gov/states/co/tax/income/rate.yaml",
}
policyengine_cache = {}
policyengine_lock = threading.Lock()


def policyengine_values(parameter_id):
    """PolicyEngine's dated values for one parameter, or None if its file cannot be read.

    Reads only the 'values:' block of the YAML, which is a list of 'date: number' lines.
    """
    with policyengine_lock:
        if parameter_id not in policyengine_cache:
            values = None
            try:
                with urllib.request.urlopen(POLICYENGINE[parameter_id], timeout=15) as response:
                    text = response.read().decode("utf-8")
                block = ("\n" + text).split("\nvalues:", 1)[1]
                values = []
                for line in block.splitlines()[1:]:
                    if line.strip() and not line.startswith((" ", "#")):
                        break  # the next top-level key ends the block
                    match = re.match(r"\s+(\d{4}-\d{2}-\d{2}):\s*([0-9.]+)", line)
                    if match:
                        values.append((match.group(1), match.group(2)))
                values = sorted(values) or None
            except Exception:
                values = None
            policyengine_cache[parameter_id] = values
        return policyengine_cache[parameter_id]


def plain(value):
    """A value as a list of brackets with tidy numbers, or None."""
    if value is None:
        return None
    return [{"over": str(over.normalize() if over else 0), "rate": format(rate.normalize(), "f")}
            for over, rate in build_web.canonical(value)]


def year_values(groups):
    """Turn one run's marks into a value per tax year, beside two other sources.

    For each parameter and year: what the model's marks say the text gives, the
    value this project uses and where it comes from, and PolicyEngine's value.
    Spans whose dates or numbers did not re-parse are left out first.
    """
    clean = []
    for group in groups:
        flags = []
        spans = []
        for span in group["spans"]:
            before = len(flags)
            evaluate.check_parse(group["provision"], span, flags)
            if len(flags) == before:
                spans.append(span)
        clean.append(dict(group, spans=spans))
    sections = attach_cross_refs(load_sections())
    by_id = build_web.ground(sections, {"groups": clean}, [])
    recorded = Parameters()
    tables = []
    for parameter_id, title in PARAMETERS:
        theirs = policyengine_values(parameter_id)
        rows = []
        for year in YEARS:
            day = "%d-01-01" % year
            hits = build_web.statute_value(by_id, parameter_id, day)
            # A provision with several rates and no marked thresholds gives no usable value:
            # taking its first rate would misstate what was marked.
            note, usable = None, []
            for hit in hits:
                provision = by_id[hit["provision"]]
                rates = sorted({Decimal(sp["normalized"]) for sp in provision["spans"] if sp["class"] == "value"})
                if len(rates) > 1 and provision.get("derive") != "schedule":
                    note = ("%d rates marked, from %s%% to %s%%, but no thresholds, so no bracket schedule can be built"
                            % (len(rates), (rates[0] * 100).normalize(), (rates[-1] * 100).normalize()))
                else:
                    usable.append(hit)
            hits = usable
            readings = sorted({build_web.canonical(h["value"]) for h in hits})
            entry = next((e for e in recorded.by_id[parameter_id]["values"]
                          if e["effective_from"] <= day and (e.get("effective_to") is None or day <= e["effective_to"])), None)
            pe = pe_since = None
            if theirs:
                earlier = [(date, value) for date, value in theirs if date <= day]
                if earlier:
                    pe_since, pe = earlier[-1]
            model = plain(hits[0]["value"]) if len(readings) == 1 else None
            used = plain(entry["value"]) if entry else None
            rows.append({
                "year": year,
                "model": model,
                "model_from": [CORPUS["cite"][h["provision"]] for h in hits],
                "model_note": note,
                "model_conflict": [plain(h["value"]) for h in hits] if len(readings) > 1 else None,
                "used": used, "status": entry["status"] if entry else "not_recorded",
                "policyengine": plain(pe) if pe else None,
                # PolicyEngine records a value from a date until its next entry.
                "policyengine_since": int(pe_since[:4]) if pe_since else None,
                "agrees_used": None if model is None or used is None else model == used,
                "agrees_policyengine": None if model is None or pe is None else model == plain(pe),
            })
        tables.append({"id": parameter_id, "title": title, "rows": rows,
                       "policyengine_reached": theirs is not None})
    return tables


class Job:
    def __init__(self, job_id, model, runs, with_context, scope):
        self.id = job_id
        self.model, self.runs, self.with_context, self.scope = model, runs, with_context, scope
        self.events, self.cond = [], threading.Condition()
        self.cancel = threading.Event()
        self.finished = False
        self.targets = CORPUS["targets"] if scope == "all" else CORPUS["core"]

    def emit(self, kind, **data):
        with self.cond:
            self.events.append({"type": kind, **data})
            if kind in ("done", "error", "stopped"):
                self.finished = True
            self.cond.notify_all()


def run_job(job):
    try:
        error = load_engine()
        if error:
            job.emit("error", message=error)
            return
        extract, lx, env = engine["extract"], engine["lx"], engine["env"]
        dry = job.model == STAND_IN
        model_name, options = extract.model_options(lx, env, job.model, dry_run=dry)
        runs_located = []

        for run in range(1, job.runs + 1):
            job.emit("run_start", run=run)
            dropped, groups, lock = Counter(), [], threading.Lock()
            failure, totals = [], Counter()

            def one(pid, run=run, dropped=dropped, groups=groups, lock=lock, failure=failure, totals=totals):
                if job.cancel.is_set() or failure:
                    return
                try:
                    with state_lock:
                        over_budget = not dry and state["calls_made"] >= MAX_CALLS
                    raw, cached = extract.mark_provision(
                        lx, engine["version"], env, pid, model_name, options, with_context=job.with_context,
                        run=run, replay=over_budget, use_cache=not dry)
                except extract.CacheMiss:
                    failure.append("This server has reached its limit of %d model calls. Restart it to reset." % MAX_CALLS)
                    return
                except Exception as exc:  # a provider error: quota, network, bad key
                    failure.append("%s: %s" % (CORPUS["cite"][pid], " ".join(str(exc).split())[:400]))
                    return
                if not cached and not dry:
                    with state_lock:
                        state["calls_made"] += 1
                with lock:
                    before = sum(dropped.values())
                    group = extract.group_for(env, pid, raw, dropped)
                    lost = sum(dropped.values()) - before
                    if group:
                        groups.append(group)
                flags = []
                located = evaluate.locate([group] if group else [], CORPUS["texts"], set(), flags)
                bad = {(f[2], f[3]) for f in flags}
                spans = [{"c": cls, "s": start, "e": end, "n": span.get("normalized"),
                          "i": (cls, span["text"]) in bad}
                         for (_, cls, start, end), span in sorted(located.items(), key=lambda kv: kv[0][2])]
                with lock:
                    totals["returned"] += len(raw)
                    totals["kept"] += len(spans)
                    totals["failed"] += sum(1 for span in spans if span["i"])
                job.emit("provision", run=run, id=pid, spans=spans, cached=cached, returned=len(raw), dropped=lost)

            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                list(pool.map(one, job.targets))
            if failure:
                job.emit("error", message=failure[0])
                return
            if job.cancel.is_set():
                job.emit("stopped")
                return
            runs_located.append(evaluate.locate(groups, CORPUS["texts"], set(), []))
            # The provisions shown to the model as examples carry their stored marks, so the
            # years they cover are not left blank.
            job.emit("run_done", run=run, values=year_values(groups + CORPUS["examples"]),
                     summary={"returned": totals["returned"], "kept": totals["kept"],
                              "not_verbatim": totals["returned"] - totals["kept"], "failed": totals["failed"]})

        stability = None
        if len(runs_located) > 1:
            union = set().union(*[set(r) for r in runs_located])
            everywhere = set(runs_located[0]).intersection(*[set(r) for r in runs_located[1:]])
            stability = {"in_every_run": len(everywhere), "distinct": len(union),
                         "share": (len(everywhere) / len(union)) if union else 1.0,
                         "unstable": sorted({"%s|%d|%d" % (k[0], k[2], k[3]) for k in union - everywhere})}
        job.emit("done", stability=stability)
    except Exception as exc:  # never leave the page waiting
        job.emit("error", message="The run failed: %s" % " ".join(str(exc).split())[:400])


def start_job(body):
    """Validate a run request and start it. Returns (status, payload)."""
    model = body.get("model")
    models = {m["id"]: m for m in available_models()}
    if model not in models:
        return 400, {"error": "Choose a model from the list."}
    if not models[model]["ready"]:
        return 400, {"error": "That model cannot run here: %s." % models[model]["why"]}
    try:
        runs = int(body.get("runs", 1))
    except (TypeError, ValueError):
        return 400, {"error": "Runs must be a whole number."}
    if not 1 <= runs <= MAX_RUNS:
        return 400, {"error": "Runs must be between 1 and %d." % MAX_RUNS}
    scope = body.get("scope", "core")
    if scope not in ("core", "all"):
        return 400, {"error": "Choose which provisions to mark."}
    if ACCESS_CODE and model != STAND_IN:
        supplied = str(body.get("code", ""))
        if not hmac.compare_digest(supplied.encode("utf-8"), ACCESS_CODE.encode("utf-8")):
            return 403, {"error": "That access code is not right."}
    with state_lock:
        current = state["job"]
        if current is not None and not current.finished:
            return 409, {"error": "A run is already in progress. Wait for it to finish, or stop it."}
        job = Job(state["next_id"], model, runs, bool(body.get("context", True)), scope)
        state["next_id"] += 1
        state["job"] = job
    job.emit("start", model=model, runs=runs, context=job.with_context, scope=scope,
             provisions=[{"id": pid, "cite": CORPUS["cite"][pid], "text": CORPUS["texts"][pid]}
                         for pid in job.targets])
    threading.Thread(target=run_job, args=(job,), daemon=True).start()
    return 200, {"job": job.id}


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):  # keep the console quiet; never log request bodies
        pass

    def send_json(self, status, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_file(self, path, content_type):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        path = url.path
        if path == "/viewer":
            self.send_response(301)
            self.send_header("Location", "/viewer/")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if path in STATIC:
            return self.send_file(*STATIC[path])
        for prefix in ("/assets/", "/viewer/assets/"):
            if path.startswith(prefix):
                target = (ASSET_ROOT / path[len(prefix):]).resolve()
                # Serve files under web/assets only.
                if ASSET_ROOT in target.parents and target.is_file():
                    return self.send_file(target, TYPES.get(target.suffix, "application/octet-stream"))
                return self.send_json(404, {"error": "not found"})
        if path == "/api/config":
            with state_lock:
                job, made = state["job"], state["calls_made"]
            return self.send_json(200, {
                "models": available_models(), "max_runs": MAX_RUNS,
                "calls_left": max(0, MAX_CALLS - made), "max_calls": MAX_CALLS,
                "needs_code": bool(ACCESS_CODE), "workers": WORKERS,
                "provisions_all": len(CORPUS["targets"]),
                "provisions_core": len(CORPUS["core"]),
                "examples": len(CORPUS["examples"]), "classes": CORPUS["classes"],
                "running": job.id if job is not None and not job.finished else None,
            })
        if path == "/api/events":
            return self.stream(parse_qs(url.query))
        self.send_json(404, {"error": "not found"})

    def stream(self, query):
        """Server-sent events for one job, from the start or from Last-Event-ID."""
        with state_lock:
            job = state["job"]
        wanted = query.get("job", [""])[0]
        if job is None or str(job.id) != wanted:
            return self.send_json(404, {"error": "no such run"})
        try:
            position = int(self.headers.get("Last-Event-ID", "-1")) + 1
        except ValueError:
            position = 0
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True
        try:
            while True:
                with job.cond:
                    if position >= len(job.events) and not job.finished:
                        job.cond.wait(timeout=15)
                    batch = job.events[position:]
                    finished = job.finished
                if not batch:
                    if finished:
                        return
                    self.wfile.write(b": waiting\n\n")  # keeps proxies from closing an idle stream
                    self.wfile.flush()
                    continue
                for event in batch:
                    self.wfile.write(("id: %d\ndata: %s\n\n" % (position, json.dumps(event))).encode("utf-8"))
                    position += 1
                self.wfile.flush()
                if finished and position >= len(job.events):
                    return
        except (BrokenPipeError, ConnectionResetError):
            return

    def do_POST(self):
        path = urlparse(self.path).path
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            length = 0
        if length > 10000:
            return self.send_json(413, {"error": "request too large"})
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(body, dict):
                raise ValueError
        except ValueError:
            return self.send_json(400, {"error": "The request was not valid JSON."})
        if path == "/api/run":
            return self.send_json(*start_job(body))
        if path == "/api/stop":
            with state_lock:
                job = state["job"]
            if job is not None and not job.finished:
                job.cancel.set()
            return self.send_json(200, {"stopping": job is not None})
        self.send_json(404, {"error": "not found"})


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    ready = [m["label"] for m in available_models() if m["ready"]]
    print("Colorado tax law as code: live demo on port %d" % PORT)
    print("models ready: %s" % "; ".join(ready))
    print("limits: %d runs per job, %d model calls before restart, access code %s"
          % (MAX_RUNS, MAX_CALLS, "required" if ACCESS_CODE else "not set"))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
