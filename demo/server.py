"""Live demo: mark statute spans with a model and watch the checks run.

  python3 demo/server.py            then open http://localhost:5000

One page. Choose a model and a number of runs, press Run, and each provision
appears as the model returns it: its spans highlighted in the statute's own
words, checked word for word, re-parsed, and scored against the hand marks.
Repeat runs show how stable the model's marks are.

The server itself is standard-library Python. Marking needs Python 3.10+ and
`pip install -r requirements.txt` (LangExtract, and the Anthropic SDK for
Claude models). Keys are read from the environment and never sent to the page:
  ANTHROPIC_API_KEY     Claude models (COTAX_CLAUDE_API_KEY is read first, if set)
  LANGEXTRACT_API_KEY   Gemini models
With no key, the stand-in model still works: it answers from the hand marks,
so it shows the pipeline and nothing about a model.

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
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import evaluate  # noqa: E402
from tools.textlib import index, load_sections  # noqa: E402

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
    models = [{"id": STAND_IN, "label": "Stand-in (answers from the hand marks; no key, no cost)", "ready": True, "why": ""}]
    for model_id, label in CLAUDE_MODELS:
        why = ("" if claude_key() and have_anthropic else
               "the Anthropic SDK is not installed" if claude_key() else "ANTHROPIC_API_KEY is not set")
        models.append({"id": model_id, "label": label, "ready": not why, "why": why})
    for model_id, label in GEMINI_MODELS:
        why = "" if os.environ.get("LANGEXTRACT_API_KEY") else "LANGEXTRACT_API_KEY is not set"
        models.append({"id": model_id, "label": label, "ready": not why, "why": why})
    return models


def corpus():
    """The provisions a run can cover, with their text and hand marks located."""
    sections = load_sections()
    by_id = index(sections)
    config = json.loads(evaluate.CONFIG.read_text(encoding="utf-8"))
    examples = set(config["example_provisions"])
    reference_file = json.loads(evaluate.REFERENCE.read_text(encoding="utf-8"))
    texts = {pid: p["text"] for pid, p in by_id.items() if p["text"]}
    reference = evaluate.locate(reference_file["groups"], texts, examples)
    cite = {p["id"]: s["citation"] + p["label"] for s in sections for p in s["provisions"]}
    hand = {}
    for (pid, cls, start, end), span in reference.items():
        hand.setdefault(pid, []).append({"c": cls, "s": start, "e": end, "n": span.get("normalized")})
    targets = [pid for pid in sorted(texts) if pid not in examples]
    return {
        "targets": targets, "texts": texts, "cite": cite, "reference": reference,
        "hand": {pid: sorted(spans, key=lambda x: x["s"]) for pid, spans in hand.items()},
        "classes": reference_file["classes"], "examples": len(examples),
    }


CORPUS = corpus()


class Job:
    def __init__(self, job_id, model, runs, with_context, scope):
        self.id = job_id
        self.model, self.runs, self.with_context, self.scope = model, runs, with_context, scope
        self.events, self.cond = [], threading.Condition()
        self.cancel = threading.Event()
        self.finished = False
        self.targets = [pid for pid in CORPUS["targets"] if scope == "all" or pid in CORPUS["hand"]]

    def emit(self, kind, **data):
        with self.cond:
            self.events.append({"type": kind, **data})
            if kind in ("done", "error", "stopped"):
                self.finished = True
            self.cond.notify_all()


def summarise(reference, candidate, flags):
    """Scores for one run against the hand marks, limited to the provisions in the run."""
    rows = evaluate.score(reference, candidate, [])  # only the "all" row
    _, n_ref, n_cand, exact, overlap = rows[0]
    return {"reference": n_ref, "candidate": n_cand,
            "precision": exact[0], "recall": exact[1], "f1": exact[2],
            "overlap_precision": overlap[0], "overlap_recall": overlap[1],
            "fabricated": sum(1 for f in flags if f[0] == "fabricated"),
            "misparse": sum(1 for f in flags if f[0] == "misparse")}


def run_job(job):
    try:
        error = load_engine()
        if error:
            job.emit("error", message=error)
            return
        extract, lx, env = engine["extract"], engine["lx"], engine["env"]
        dry = job.model == STAND_IN
        model_name, options = extract.model_options(lx, env, job.model, dry_run=dry)
        reference = {k: v for k, v in CORPUS["reference"].items() if k[0] in job.targets}
        runs_located = []

        for run in range(1, job.runs + 1):
            job.emit("run_start", run=run)
            dropped, groups, lock = Counter(), [], threading.Lock()
            failure = []

            def one(pid, run=run, dropped=dropped, groups=groups, lock=lock, failure=failure):
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
                job.emit("provision", run=run, id=pid, spans=spans, cached=cached, returned=len(raw), dropped=lost)

            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                list(pool.map(one, job.targets))
            if failure:
                job.emit("error", message=failure[0])
                return
            if job.cancel.is_set():
                job.emit("stopped")
                return
            flags = []
            located = evaluate.locate(groups, CORPUS["texts"], set(), flags)
            runs_located.append(located)
            job.emit("run_done", run=run, summary=summarise(reference, located, flags),
                     dropped=dict(dropped))

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
    scope = body.get("scope", "hand")
    if scope not in ("hand", "all"):
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
             provisions=[{"id": pid, "cite": CORPUS["cite"][pid], "text": CORPUS["texts"][pid],
                          "hand": CORPUS["hand"].get(pid)} for pid in job.targets])
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
                "provisions_hand": sum(1 for p in CORPUS["targets"] if p in CORPUS["hand"]),
                "examples": CORPUS["examples"], "classes": CORPUS["classes"],
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
