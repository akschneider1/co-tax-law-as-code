# Colorado tax law as code: prototype slice

An unofficial prototype that encodes one small slice of Colorado tax law in linked layers: structured statute text, stored copies of agency sources, dated parameters, and executable rules. It is not tax advice and not a statement of Colorado law.

**The slice:** the individual income tax rate (C.R.S. 39-22-104, and for 2027 the text Amendment 87 proposes) and the state earned income tax credit (C.R.S. 39-22-123.5), for full-year residents, tax years 2022 to 2027.

Current state, lessons from related projects and planned improvements are in [docs/ROADMAP.md](docs/ROADMAP.md). The background research is in [docs/research/](docs/research/).

## Run it

Python 3.8 or later, standard library only. From this folder:

```bash
python3 tools/validate.py
```

```bash
python3 tools/run_tests.py
```

```bash
python3 calc.py --year 2025 --taxable-income 20000 --federal-eitc 4000
```

The calculator prints two tax figures: the amount the statutory rate gives, and the amount the Department of Revenue's printed tax table gives. They differ by a few dollars at or below $50,000. Add `--method form` to build the net figure on the table amount. Add `--eitc-basis under_25` or `--eitc-basis no_work_ssn` when the federal credit amount is the one the filer would have been allowed, not one they claimed.

## Live demo

A one-page web app that runs the model marking in front of you. Choose a model and a number of runs, press Run, and each provision appears as the model returns it, with its spans highlighted in the statute's words and checked on the spot. Repeat runs show how stable the marks are.

```bash
pip install -r requirements.txt
```

```bash
python3 demo/server.py
```

Then open http://localhost:5000. It needs Python 3.10 or later. The existing viewer is linked from the page.

**Keys** are read from the environment and never sent to the page: `ANTHROPIC_API_KEY` for Claude models, `LANGEXTRACT_API_KEY` for Gemini. With neither, a stand-in model still works. It answers from the hand marks, so it shows the pipeline and nothing about a model.

**On Replit:** import the repository (`https://replit.com/github.com/akschneider1/co-tax-law-as-code` imports the default branch), add the keys in the Secrets tool, and press Run. `.replit` and `requirements.txt` are set up for this. The Replit configuration has not been tried on Replit; it was written from Replit's documentation as summarised by a search engine.

**Limits.** Anyone who can open the page can spend the key's money, so the server enforces limits, each settable as an environment variable:

| Variable | Default | What it limits |
|---|---|---|
| `DEMO_ACCESS_CODE` | not set | If set, a run with a paid model must supply it. Set this before making the app public. |
| `DEMO_MAX_RUNS` | 3 | Runs per job |
| `DEMO_MAX_CALLS` | 300 | Model calls the server makes before it must be restarted. Cached results do not count. |
| `DEMO_WORKERS` | 4 | Provisions marked at once |

One job runs at a time. Results are cached in `extractions/cache/`, so a repeat of the same run costs nothing.

What has been tried: the stand-in and Gemini, in a browser, including the cache, the access code and the call limit. The Claude models reach the API but no Claude request has completed, because no Claude key was available.

## See how a parameter is built from the text

```bash
python3 tools/build_web.py
```

```bash
open web/index.html
```

The viewer shows the statute text on the left with the words that carry each piece of a parameter highlighted: the tax years, the number, what it applies to, who it covers, and any exception. Pick a tax year on the right to see the chain from those words to the value the engine uses, including any other source that overrode the text.

How the grounding works:

1. `extractions/extractions.json` records, for each provision, the exact words that matter and what they mean. A language model (Claude) marked these by reading the text; no lawyer has reviewed them.
2. `tools/build_web.py` finds every marked span verbatim in the provision. A span that is not in the text fails the build.
3. The script re-parses date phrases, number words and dollar amounts with ordinary code ("four and forty one-hundredths percent" becomes 0.044) and fails if its result differs from what the model recorded.
4. From the spans it derives what the text alone says for each tax year, and fails if a claim in `parameters/` that points to a provision is not backed by one. For 2027 it derives the six-bracket schedule from the rates and thresholds marked in the measure's text.

`web/index.html` is generated from `web/template.html` with the data inlined, so it opens by double-click with no server. It is styled with the U.S. Web Design System (USWDS 3.14.0), vendored in `web/assets/uswds/` with its licence file. The page carries no government banner or seal because it is not a government site.

### Marking spans with LangExtract

`tools/extract_langextract.py` replaces the hand marking with a model call per provision through Google's LangExtract library. Two hand-marked provisions serve as the examples; the model marks the rest. Each provision is sent with the context a reader needs: its heading, the lead-in text above it, later provisions that modify it, and the text it cross-refers to.

**Run once against a real model, in part.** Gemini 3.5 Flash, with context, has marked 22 of the 31 provisions; a free-tier daily quota stopped it there. On the 9 provisions that have hand marks it scored 72% precision and 76% recall on exact matches, and every span it returned was word for word in the text. No run without context, no repeat run and no Claude run has been made, and no person has decided the disagreements. The script has also been run end to end with a stand-in model that answers from the hand marks (`--dry-run`), which tests the plumbing only.

```bash
pip install -r requirements-langextract.txt
```

```bash
python3 tools/extract_langextract.py --ask-key
```

`--ask-key` prompts for the key in the terminal without showing it, uses it for that run and saves it nowhere. It needs an interactive terminal. Otherwise set `LANGEXTRACT_API_KEY` in the environment first and leave the flag off.

```bash
python3 tools/evaluate.py extractions/candidates.langextract.json
```

```bash
python3 tools/build_web.py --extractions extractions/candidates.langextract.json
```

`tools/evaluate.py` prints precision, recall and F1 by span class against the hand marks. It treats the hand marks as a reference, not as the truth: every disagreement is written to `extractions/adjudication.json` for a person to decide, and a second table shows the scores after those decisions. A candidate span that is not word for word in the text, or whose dates or number do not re-parse, marks the whole file not reliable whatever its scores. Give it several files from repeat runs to see how stable the marks are.

Other options: `--no-context` to measure what the context is worth, `--replay` to rebuild from cached model output without a key, `--model gpt-4o` with `OPENAI_API_KEY`, or `--model gemma2:2b --model-url http://localhost:11434` for a local Ollama model.

Claude models work too: `--model claude-opus-5-5` with `ANTHROPIC_API_KEY`. LangExtract has no Anthropic provider, so the script supplies a small one that calls the Anthropic SDK and hands the reply to LangExtract to parse and align. That path has reached the API but has not yet completed a request with a real key.

## The layers

| Layer | Where | What it holds |
|---|---|---|
| Structured text | `text/*.xml`, `text/manifest.json` | Verbatim provisions, each with a stable id such as `/us/co/crs/39-22-123.5/2/b`, plus source, retrieval date and a content hash. One file holds a ballot measure's proposed text and is labelled as such |
| Stored sources | `sources/*.txt`, `sources/manifest.json` | A text copy of each agency or legislature document a parameter quotes, with its address, retrieval date and hashes |
| Parameters | `parameters/*.json` | Each value with an effective date range, a status, and every source that states it |
| Rules | `engine/co_rules.py`, `engine/core.py` | Four rules, each citing the provision ids and parameters it relies on, by tax year; every result comes with a trace |

`tests/cases.json` is independent of the engine: facts in, expected whole-dollar results out. `tests/tax_tables.json` holds the Department of Revenue's printed tax tables for 2022 to 2025, generated from the stored booklets.

### What each claim rests on

Every claim this README makes about checking is enforced by a script. If a row here has no check, the claim should not be made.

| Claim | Enforced by | How |
|---|---|---|
| Text has not changed since it was recorded | `tools/validate.py` | Hash of every provision against `text/manifest.json` |
| Every provision a rule or parameter cites exists | `tools/validate.py` | Looks up each id |
| A value a source contradicts is explained | `tools/validate.py` | Fails without a `conflict_note` |
| Every quote from an agency or the legislature is real | `tools/validate.py` | Finds the quote, word for word, in the stored copy, and checks the copy's hash |
| A value called agency-published has a checked agency quote | `tools/validate.py` | Fails otherwise |
| Marked spans are the statute's own words | `tools/build_web.py` | Finds each span verbatim |
| Dates, percentages and dollar amounts are read correctly | `tools/build_web.py` | Re-parses the words with ordinary code |
| A value attributed to a provision is what the provision says | `tools/build_web.py` | Derives the value from the spans and compares |
| The form-table rule matches the Department's tables | `tools/run_tests.py` | 4,024 checks against 2,012 printed rows |
| The test rows are the ones in the booklets | `tools/run_tests.py` | Regenerates them from the stored copies and compares |

What no script checks: whether the right words were marked (no lawyer has reviewed the spans), whether a stored copy still matches the live page (a copy records one day), and whether the statute snapshot is current (it is known not to be).

Run `python3 tools/validate.py --strict` to fail on any value that rests on the statute snapshot alone. Today that is one value, the 2026 rate.

To refresh or add a stored copy:

```bash
python3 tools/snapshot_source.py dor-eitc-topics https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit
```

Converting a PDF needs the `pdftotext` program. Nothing else in the project needs anything beyond Python.

### Parameter statuses

- `agency_published`: stated by the Department of Revenue, with a quote checked against a stored copy.
- `statute_snapshot`: read from the ingested statute text only.
- `statutory_default`: the statute's value, which a trigger or later act may displace.
- `reported_passed_uncertified`: rests on an election result that was not certified when recorded.

The engine attaches a warning to any result that uses a value below `agency_published`, and it refuses to compute where no value is recorded.

## What the prototype found

**The statute snapshot and the agency disagree in five places.** The text comes from an unofficial mirror (public.law), which names the legislature's 2024 Title 39 PDF as its source. The Department of Revenue's pages, read on 11 November 2026, publish different numbers:

| Parameter | Tax year | Statute snapshot | Department of Revenue | Used |
|---|---|---|---|---|
| EITC share of federal credit | 2023 | 25% | 50% | 50% |
| EITC share of federal credit | 2024 | 38% | 50% | 50% |
| EITC share of federal credit | 2025 | 25% | 50% | 50% |
| EITC share of federal credit | 2026 | 20% | 25% | 25% |
| Income tax rate | 2024 | 4.40% | 4.25% | 4.25% |

The 2023 row was found later than the others: until the Department's 2023 form and its credit percentage table were read, this repository recorded 25% for 2023 from the snapshot alone.

The snapshot's own heading for 39-22-123.5 mentions a "trigger" that its text does not contain, and its copy of 39-22-627 (temporary rate reduction) describes only a 4.63% to 4.50% cut. So the mirror is behind current law. The amending provisions have not been ingested, which means the rules for those years rest on agency statements, not on text in this repository.

**Two values are not known.** No Department of Revenue rate for 2026 was found, so the statutory 4.40% is used with a warning. No EITC percentage for 2027 is recorded, so the engine refuses to compute the credit for that year. The Department's credit percentage table has a row "2026 and later 25%", which is not used for 2027 because the act behind it (HB24-1134) has not been read.

**The 2027 brackets come from the measure's text, and the result is not certified.** Amendment 87's six brackets were read from the final text of initiative 2025-2026 #195 on the legislature's site, and match The Colorado Sun's account. No certification of the result was found as of 11 November 2026. The text sets one schedule for every individual, estate and trust, with no filing-status thresholds, and the Blue Book says the brackets are not adjusted for inflation. Proposed subsection (1.8) is ingested in `text/co-2026-amendment-87.xml` and the schedule is derived from its marked words. The rest of the measure is not ingested, because struck words do not survive conversion of the PDF. Two parts are not modelled: a 4.40% rate on certain gain from selling a principal residence (the engine refuses a filer who reports such gain), and temporary rate changes under 39-22-627.

## Limits

- **Inputs, not computations:** Colorado taxable income and the federal credit are supplied by the caller. The additions and subtractions in 39-22-104(3) and (4) are not modelled.
- **Residency:** part-year residents and nonresidents are rejected.
- **Rounding:** whole dollars, half up. The 2023 104 Book says to round dollar amounts to the nearest whole dollar; its treatment of exact half dollars was not checked.
- **Tax table:** for taxable income under $50,000 the Department publishes tax tables that, in its words, "approximate" the tax at the prescribed rate. The engine reports both the statutory amount and the table amount. The table method (the rate applied to the middle of a $100 band) is inferred, not stated by the Department; it reproduces all 2,012 printed rows read from the 2022 to 2025 booklets. Four rows could not be read from the converted text. No table is recorded for 2026 or 2027.
- **Filers the federal credit excludes:** Colorado allows its credit to some filers who cannot claim the federal one (certain filers under 25, and filers without a Social Security number valid for work), based on the federal credit they would have been allowed. The caller says which case applies and supplies that would-be amount. The engine cites the matching provision and warns that it cannot check the amount, because it does not compute the federal credit.
- **Tests:** 21 of the 23 cases in `tests/cases.json` were worked by hand from the parameter files, so they check the engine against the parameters, not the parameters against the law. Two take their figures from the Department of Revenue's 2023 booklet. The printed tax tables add 4,024 official checks, but only of the form-table rule. None comes from a Department of Revenue test scenario.
- **Text format:** a USLM-inspired hierarchy, not schema-valid USLM. One snapshot only; no point-in-time history.
- **Citations by year are set by hand:** the trace for 2022 to 2026 cites 39-22-104(1.7)(c) and for 2027 cites the measure's proposed (1.8). The year ranges are written into the rule, not derived from effective dates in the text.
- **Stored copies are text, not the original files:** the PDFs were converted with `pdftotext`, which loses layout, strikethrough and some table rows. The hash of each original file is recorded.

## Next steps

1. Ingest the current official text of 39-22-104, 39-22-123.5 and 39-22-627 from the legislature's own Title 39 files, with the session laws that amended them, and re-run the validator to see which conflicts close. The 2026 files are on `olls.info`, which this project's sessions have not been allowed to reach.
2. Run the LangExtract script against a real model, with and without context, and have a person decide the disagreements.
3. Read HB24-1134, then decide the 2027 EITC share.
4. Cross-check results against PolicyEngine's Colorado model, then decide what to contribute upstream.
5. When Amendment 87's result is certified, update the 2027 status, and model the principal-residence rule.
