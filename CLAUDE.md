# Colorado tax law as code

An unofficial prototype that encodes a small slice of Colorado tax law (income tax rate, C.R.S. 39-22-104; state earned income tax credit, C.R.S. 39-22-123.5) as structured text, dated parameters and executable rules, with every parameter grounded in exact spans of statute text and every agency quote checked against a stored copy of its source.

Read `README.md` for the layout and findings, and `docs/ROADMAP.md` for current state, lessons from STARA and Mike Hsu's work, and the planned improvements. Start there before changing anything.

## Checks to run after any change

```bash
python3 tools/validate.py
python3 tools/run_tests.py
python3 tools/build_web.py
```

All three must pass. `build_web.py` regenerates `web/index.html` from `web/template.html`; edit the template, never the generated file.

## Rules for this project

- Statute text in `text/*.xml` is verbatim. Never paraphrase, correct or complete it. After an intended text change, run `python3 tools/validate.py --stamp`.
- Never fill a parameter from memory. Every value needs a source recorded in the parameter file, and a value that any of its sources contradicts needs a `conflict_note`.
- A quote from an agency or the legislature must be in a stored copy under `sources/`. Add or refresh a copy with `python3 tools/snapshot_source.py ID URL`, then name it in the source's `snapshot` field. A search-engine summary is a lead, not a source.
- `tests/tax_tables.json` is generated. Regenerate it with `python3 tools/make_table_tests.py`; do not edit it by hand.
- Keep the README's "What each claim rests on" table true: a claim about checking needs a script that enforces it.
- Where a value is unknown, leave it unrecorded so the engine refuses to compute. Do not guess.
- Spans in `extractions/` must appear word for word in the provision.
- The viewer uses USWDS. Do not add the official government banner, a seal or a .gov identifier: this is not a government site.
- Everything except `tools/extract_langextract.py` must stay standard-library Python that runs on 3.8. `demo/server.py` is standard library too, and loads LangExtract only when a run starts.
- The live demo (`demo/server.py`, `demo/index.html`) spends a model key's money when a run starts. Never weaken its limits or send a key to the page. Converting a PDF in `tools/snapshot_source.py` also needs the `pdftotext` program.
- Say plainly in the README what is untested or unverified.
