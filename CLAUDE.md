# Colorado tax law as code

An unofficial prototype that encodes a small slice of Colorado tax law (income tax rate, C.R.S. 39-22-104; state earned income tax credit, C.R.S. 39-22-123.5) as structured text, dated parameters and executable rules, with every parameter grounded in exact spans of statute text.

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
- Where a value is unknown, leave it unrecorded so the engine refuses to compute. Do not guess.
- Spans in `extractions/` must appear word for word in the provision.
- The viewer uses USWDS. Do not add the official government banner, a seal or a .gov identifier: this is not a government site.
- Everything except `tools/extract_langextract.py` must stay standard-library Python that runs on 3.8.
- Say plainly in the README what is untested or unverified.
