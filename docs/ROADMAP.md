# Roadmap and handoff

Written 11 November 2026, when the work moved from a local machine to GitHub. It records where the prototype stands, what was learned from other projects, and what is planned next. Governance is deliberately deferred.

## Where things stand

| Piece | State |
|---|---|
| Text, parameters, engine, 15 tests, validator | Working. `tools/validate.py` and `tools/run_tests.py` pass. |
| Grounding build (`tools/build_web.py`) | Working. 33 hand-marked spans located verbatim and re-parsed. |
| Viewer (`web/index.html`, USWDS 3.14.0) | Working. Checked in a browser: both parameters, year selection, no console errors. |
| LangExtract script (`tools/extract_langextract.py`) | Written, never run. Only its non-model parts were tested, with a stand-in for the library. |
| `tools/textlib.py` (cross-references, context, parsers) | Written and sanity-checked. Not yet used by any other script. |
| Everything under "Planned improvements" below | Not started, except `textlib.py`. |

### Known weaknesses

- **The statute text is out of date.** It comes from an unofficial mirror (public.law). Four values it gives differ from what the Department of Revenue publishes; see the README table. The amending provisions are not ingested.
- **Tests are hand-derived** from the parameter files. None comes from an official form example.
- **Span marking is unreviewed.** A language model marked the spans; no lawyer has checked them.
- **`build_web.py` duplicates code** that now also lives in `textlib.py` (section loading and the two parsers). The first refactor is to make it import from `textlib.py`.

### Environment notes

- Everything except LangExtract runs on Python 3.8+ with the standard library.
- LangExtract needs Python 3.10+ and a model key (`LANGEXTRACT_API_KEY` for Gemini, `OPENAI_API_KEY`, or a local Ollama model). On the original machine (Intel Mac, macOS 13) the install failed because `cryptography` had no prebuilt package and needed a Rust toolchain. A Linux cloud environment should not have that problem.
- Before first use, confirm the `lx.extract` signature (`python -c "import langextract as lx, inspect; print(inspect.signature(lx.extract))"`), in particular whether it accepts `additional_context`. The script was written from the README for v1.7.2.
- To preview the viewer: `python3 -m http.server 8765 --directory web`.

## What other projects teach

### Stanford RegLab: STARA (Statutory Research Assistant)

Read from the project page, FAQ and policy page. The paper and policy brief PDFs could not be read as text, so the method details below are incomplete.

- **Context is the largest lever.** Their ablation on federal criminal statutes: a bare model call scored precision 0.58 and extraction quality 0.28. Adding basic context (headings, definitions, cross-references) raised these to 0.96 and 0.70. The full system reached 0.96 and 0.76, with recall 0.998.
- **Subsections are fragments.** They only make sense with their parent provision, so each unit is annotated with non-local context before a model sees it.
- **Enumerate, then aggregate.** They process a complete list of units in batches and aggregate, not one open-ended search. General research tools reached recall of 0.04 to 0.14 on the same task.
- **Measure against human-compiled lists**, with precision and recall.
- **Hallucinated citations are a measured failure.** A commercial legal tool returned 121 provisions that do not exist.
- **Access.** STARA is in closed beta, available to researchers on request. Its datasets are public with no stated licence. RegLab's `lawscraper` repository scrapes state codes from Justia and FindLaw; its licence and Colorado coverage were not verified.

### Mike Hsu: policy-sludge work

Read from two public repositories and one open Substack post. His "Policy as code" post is paywalled and was not read.

- **Inventory first** (`policy-sludge-cleanup`, MIT). Every instrument gets a row: id, title, date, type, status, supersedes, superseded by, triage, rationale.
- **Audit checks on the inventory.** "Zombies" are items marked live that something else supersedes. "Orphans" are items with no destination. Both are data errors to report.
- **Full traceability.** Every source item is mapped, repealed or retained with a written reason.
- **Integrity outranks polish** (`bank-board-policy-sludge`, no licence seen). His rubric weights citation integrity and accuracy at 45 of 100 points. Any central integrity flag (fabricated source, misattribution, stale presented as current, invented obligation) marks the whole output unreliable whatever its score.
- **Several models, several judges.** Run more than one model on the same task, sample citations with a fixed seed, check them against official sources, and confirm serious findings by hand.
- **Human and machine views** of the same item, with typed fields and explicit cross-reference links (his FR 2052a reference site).

## Planned improvements

### Accuracy

1. **Send context with every provision.** Use `textlib.context_for` to give the model the section heading, parent provisions and cross-referenced text. Done when the LangExtract script passes it and a run with and without context is compared.
2. **Flag unread dependencies.** `textlib.find_cross_refs` already finds them: both rate provisions defer to section 39-22-627, which is not ingested, and that is exactly why the text-only 2024 rate is wrong. Done when the build marks any text-derived value whose provision points to unread Colorado text, and the viewer shows it.
3. **Score extractions.** Add `tools/evaluate.py`: precision, recall and F1 by span class against the hand marks, exact and overlapping match. Done when it prints a table for any candidates file.
4. **Integrity flags that override the score.** Not verbatim (fabricated), date or number that does not re-parse (misparse), text contradicted by a higher-status source (stale). Any flag marks the candidate set as not reliable.
5. **Model comparison and consensus.** Run two or more models, score each, and keep only spans a majority agree on. Disagreements go to review.
6. **Ingest current official text** of 39-22-104, 39-22-123.5 and 39-22-627 with the session laws that amended them, then re-run the validator to see which of the four conflicts close.

### Scalability

7. **Cache model output** by provision hash, prompt hash and model, so unchanged provisions are never re-sent.
8. **Parallel workers** for the per-provision calls.
9. **Inventory and audit.** Add `tools/inventory.py` writing `inventory.csv`, one row per provision: id, citation, status, source, retrieval date, hash, parameter, span count, cross-references, unread dependencies, review status, contradicted years, triage, rationale. Audit output: zombies (in-force text contradicted by the agency), orphans (parameter values with no statute grounding, such as the 2027 brackets), unread dependencies, share unreviewed.
10. **Generic ingestion.** A script that turns a section from the official source into `text/*.xml`, so adding a section is one command. Look at `lawscraper` first.
11. **Move the section-to-parameter mapping** out of the LangExtract script into a config file.

### Usability

12. **Review workflow.** Per-provision status (unreviewed, accepted, needs fix) with reviewer, date and note, stored in `extractions/review.json` and keyed to the text hash, so a text change voids the review. The viewer gets accept and flag buttons and a download of the review file.
13. **Human and machine toggle** in the viewer: the same year shown as prose steps or as its JSON record.
14. **Clickable cross-references** in the statute text: jump to the target if ingested, show "not ingested" if not.
15. **Coverage summary** at the top of the viewer: provisions, spans, share reviewed, unread dependencies, open conflicts.
16. **Search** across provisions.

### Carried over from earlier

- Add effective-date ranges to provisions so a rule cites the text in force for the tax year.
- Replace derived tests with official ones: DR 0104 worked examples, and e-file acceptance scenarios if obtainable.
- Cross-check results against PolicyEngine's Colorado model, then decide what to contribute upstream. The Property Tax/Rent/Heat rebate is missing there.
- Ingest Amendment 87's certified text once available: filing-status thresholds, indexing, income base.
- Extend span marking to 39-22-123.5 (2.5) and (2.7).

## Open decisions

- **Licence.** Settled: the repository is Apache 2.0 (`LICENSE`). USWDS files keep their own licences (`web/assets/uswds/LICENSE.md`).
- **Governance.** Deferred. `docs/research/tradeoffs-report.md` covers stewardship models and precedents.
- **Model provider** for LangExtract runs.

## Research in this repository

- `docs/research/tradeoffs-report.md`: the full tradeoffs report (structured text, parameters, engines, governance, sequencing after Amendment 87), with a section on what is unverified.
- `docs/research/notes/`: the five sets of source notes behind it.

## Sources for this roadmap

- STARA project page: https://reglab.github.io/stara
- STARA FAQ: https://reglab.github.io/stara/faq.html
- Stanford HAI policy page: https://hai.stanford.edu/policy/cleaning-up-policy-sludge-an-ai-statutory-research-system
- RegLab lawscraper: https://github.com/reglab/lawscraper
- Hsu, policy-sludge-cleanup: https://github.com/mhsu2112/policy-sludge-cleanup
- Hsu, bank-board-policy-sludge: https://github.com/mhsu2112/bank-board-policy-sludge
- Hsu, "Cumulative policy sludge": https://mhsu2112.substack.com/p/cumulative-policy-sludge
- Hsu, FR 2052a reference: https://fr2052a-as-code.netlify.app/
- Recoding America portfolio: https://recodingamerica.org/portfolio
- LangExtract: https://github.com/google/langextract
