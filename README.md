# Colorado tax law as code: prototype slice

An unofficial prototype that encodes one small slice of Colorado tax law in three linked layers: structured statute text, dated parameters, and executable rules. It is not tax advice and not a statement of Colorado law.

**The slice:** the individual income tax rate (C.R.S. 39-22-104) and the state earned income tax credit (C.R.S. 39-22-123.5), for full-year residents, tax years 2022 to 2027.

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
3. The script re-parses date phrases and number words with ordinary code ("four and forty one-hundredths percent" becomes 0.044) and fails if its result differs from what the model recorded.
4. From the spans it derives what the text alone says for each tax year, and fails if a statute claim in `parameters/` is not backed by one.

`web/index.html` is generated from `web/template.html` with the data inlined, so it opens by double-click with no server. It is styled with the U.S. Web Design System (USWDS 3.14.0), vendored in `web/assets/uswds/` with its licence file. The page carries no government banner or seal because it is not a government site.

### Marking spans with LangExtract

`tools/extract_langextract.py` replaces the hand marking with a model call per provision through Google's LangExtract library. Two hand-marked provisions serve as the examples; the model marks the rest. Spans that are not verbatim, or that overlap, are dropped, and the script reports where the model and the hand marks differ.

**Not yet run.** It needs Python 3.10 or later and a model API key, and was written on a machine with neither. Only its non-model parts have been tested, with a stand-in for the library.

```bash
pip install -r requirements-langextract.txt
```

```bash
export LANGEXTRACT_API_KEY=your-key
```

```bash
python3 tools/extract_langextract.py
```

```bash
python3 tools/build_web.py --extractions extractions/candidates.langextract.json
```

The last command runs the same checks on the model's spans as on the hand-marked ones and rebuilds the viewer from them. Use `--model gpt-4o` with `OPENAI_API_KEY`, or `--model gemma2:2b --model-url http://localhost:11434` for a local Ollama model.

## The three layers

| Layer | Where | What it holds |
|---|---|---|
| Structured text | `text/*.xml`, `text/manifest.json` | Verbatim statute provisions, each with a stable id such as `/us/co/crs/39-22-123.5/2/b`, plus source, retrieval date and a content hash |
| Parameters | `parameters/*.json` | Each value with an effective date range, a status, and every source that states it |
| Rules | `engine/co_rules.py`, `engine/core.py` | Three rules, each citing the provision ids and parameters it relies on; every result comes with a trace |

`tools/validate.py` checks the links between the layers: every provision a rule or parameter cites must exist, the text must match its recorded hashes, and any parameter value that one of its own sources contradicts must carry a written explanation.

`tests/cases.json` is independent of the engine: facts in, expected whole-dollar results out.

### Parameter statuses

- `agency_published`: stated by the Department of Revenue.
- `statute_snapshot`: read from the ingested statute text only.
- `statutory_default`: the statute's value, which a trigger or later act may displace.
- `reported_passed_uncertified`: from news reports of an uncertified election.

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

**The 2027 brackets come from the measure's text, and the result is not certified.** Amendment 87's six brackets were read from the final text of initiative 2025-2026 #195 on the legislature's site, and match The Colorado Sun's account. No certification of the result was found as of 11 November 2026. The text sets one schedule for every individual, estate and trust, with no filing-status thresholds, and the Blue Book says the brackets are not adjusted for inflation. The measure's text is not ingested into `text/` and has no marked spans. Two parts of it are not modelled: a 4.40% rate on certain gain from selling a principal residence, and temporary rate changes under 39-22-627.

## Limits

- **Inputs, not computations:** Colorado taxable income and the federal credit are supplied by the caller. The additions and subtractions in 39-22-104(3) and (4) are not modelled.
- **Residency:** part-year residents and nonresidents are rejected.
- **Rounding:** whole dollars, half up. The 2023 104 Book says to round dollar amounts to the nearest whole dollar; its treatment of exact half dollars was not checked.
- **Tax table:** for taxable income under $50,000 the Department publishes tax tables that, in its words, "approximate" the tax at the prescribed rate. The 2023 table works in $100 bands. The engine applies the rate to the exact income, so its result can differ from the form's by a few dollars in that range.
- **Filers the federal credit excludes:** Colorado allows its credit to some filers who cannot claim the federal one (certain filers under 25, and filers without a Social Security number valid for work), based on the federal credit they would have been allowed. The engine takes the federal credit as given, so the caller must supply that would-be amount for these filers.
- **Tests:** 15 of the 16 cases were worked by hand from the parameter files, so they check the engine against the parameters, not the parameters against the law. One case takes its tax and credit figures from the Department of Revenue's 2023 booklet. None comes from a Department of Revenue test scenario.
- **Text format:** a USLM-inspired hierarchy, not schema-valid USLM. One snapshot only; no point-in-time history.
- **Citations are per rule, not per year:** the trace for a 2027 calculation still lists 39-22-104(1.7)(c), the flat-rate provision. A warning says no ingested text supports the value.

## Next steps

1. Ingest the current official text of 39-22-104, 39-22-123.5 and 39-22-627 from the legislature's own Title 39 files, with the session laws that amended them, and re-run the validator to see which conflicts close.
2. Add effective-date ranges to provisions so a rule cites the text in force for the tax year.
3. Replace derived test cases with official ones: DR 0104 worked examples and, if obtainable, e-file acceptance scenarios.
4. Cross-check results against PolicyEngine's Colorado model, then decide what to contribute upstream.
5. Ingest Amendment 87's text into `text/` once the result is certified, mark its spans, and model the principal-residence rule.
