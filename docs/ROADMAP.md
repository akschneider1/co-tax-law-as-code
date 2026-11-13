# Roadmap and handoff

Written 11 November 2026, when the work moved from a local machine to GitHub. It records where the prototype stands, what was learned from other projects, and what is planned next. Governance is deliberately deferred.

## Where things stand

| Piece | State |
|---|---|
| Text, parameters, engine, validator | Working. `tools/validate.py` passes. |
| Tests | Working. 23 cases, and 4,024 checks against the Department of Revenue's printed tax tables. |
| Stored sources (`sources/`, `tools/snapshot_source.py`) | Working. Nine documents; every agency quote is checked against one. |
| Amendment 87 text (`text/co-2026-amendment-87.xml`) | Proposed (1.8) ingested and marked. The rest of the measure is not. |
| Grounding build (`tools/build_web.py`) | Working. 66 reference spans located verbatim and re-parsed. Imports `textlib.py`. |
| Viewer (`web/index.html`, USWDS 3.14.0) | Working. Checked in a browser: both parameters, every year, no script errors. |
| LangExtract script (`tools/extract_langextract.py`) | Run against Gemini 3.5 Flash on the nine core provisions under the dictionary's instructions. Eight of nine complete; bracket thresholds still unmarked. Claude provider added, not yet run with a key. |
| Data dictionary (`dictionary/dictionary.json`, `tools/dictionary.py`) | Draft 0.1.0, enforced by the validator. 8 of 12 span classes and 9 of 20 provision types in use. 19 of 33 provisions marked. |
| Live demo (`demo/server.py`, `.replit`) | Working locally with the stand-in and Gemini. Not yet tried on Replit. |
| Scoring (`tools/evaluate.py`) | Working. Tried on altered copies of the hand marks. No real candidates yet. |
| Current official statute text | Not ingested. The 2026 files are on `olls.info`, which was not allowed. |

### Known weaknesses

- **The statute text is out of date.** It comes from an unofficial mirror (public.law). Five values it gives differ from what the Department of Revenue publishes; see the README table. The amending provisions are not ingested.
- **Most test cases are hand-derived** from the parameter files. The official checks cover the form-table rule only.
- **Span marking is unreviewed.** A language model marked the spans; no lawyer has checked them.
- **The model run is partial and unadjudicated.** One model, one run, 22 of 31 provisions. Whether context helps on this text is unmeasured, and nobody has decided the disagreements with the hand marks.
- **The tax-table method is inferred.** The Department does not state it. It reproduces every printed row that could be read.

### Environment notes

- Everything except LangExtract runs on Python 3.8+ with the standard library.
- LangExtract needs Python 3.10+ and a model key (`LANGEXTRACT_API_KEY` for Gemini, `OPENAI_API_KEY`, or a local Ollama model). On the original machine (Intel Mac, macOS 13) the install failed because `cryptography` had no prebuilt package and needed a Rust toolchain. A Linux cloud environment should not have that problem.
- Before first use, confirm the `lx.extract` signature (`python -c "import langextract as lx, inspect; print(inspect.signature(lx.extract))"`), in particular whether it accepts `additional_context`. The script was written from the README for v1.7.2.
- To preview the viewer: `python3 -m http.server 8765 --directory web`.

## What other projects teach

### Stanford RegLab: STARA (Statutory Research Assistant)

Read from the project page, FAQ and policy page, and later from the paper itself and its follow-up benchmark paper. Method details are in `docs/research/notes/stara_hsu_followup.md`.

- **Context is the largest lever.** Their ablation on federal criminal statutes: a bare model call scored precision 0.58 and extraction quality 0.28. Adding basic context raised these to 0.96 and 0.70. The full system reached 0.98 and 0.76, with recall 0.998. The context the paper describes is headings, definitions, lead-in sentences and trailing provisos.
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
6. **Ingest current official text** of 39-22-104, 39-22-123.5 and 39-22-627 with the session laws that amended them, then re-run the validator to see which of the five conflicts close.

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

## Proposed changes from the follow-up research

Two further research passes on 11 November 2026 are written up in `docs/research/notes/stara_hsu_followup.md`. The first could reach GitHub and web search only. The second could also reach the legislature, the Department of Revenue, the Secretary of State, arXiv and Stanford, and read both STARA papers and the Colorado sources.

Done in the second pass, because each rests on a source that was read:

- The 2023 EITC share is corrected from 25% to 50% (a fifth conflict with the snapshot).
- The 2022 EITC share and the 2027 brackets gained primary sources.
- One test now comes from the 2023 104 Book.
- The README states the tax-table, rounding and under-25 limits.

Everything lettered below was a proposal. Most have since been implemented; "Status of these proposals" below says which.

### Corrections to the roadmap as written

- **Item 10: do not use `lawscraper`.** It has no licence, scrapes Justia and FindLaw (unofficial mirrors), has no Colorado output, and its FindLaw parser keeps only the first paragraph of a section. Build ingestion on the legislature's own title files. The 2026 files, current through the 2026 Second Regular Session, are linked from the Office of Legislative Legal Services download page and hosted on `olls.info`, which no session has yet been allowed to reach.
- **Environment note on `lx.extract`: answered.** `additional_context` exists, as do `extraction_passes`, `max_workers` and `max_char_buffer` (read on `main`, not checked against the v1.7.2 tag).
- **Item 5: `extraction_passes` is not consensus.** It merges passes with "first extraction wins for overlaps". A majority vote needs separate runs compared by our own code.
- **Item 8: parallel workers already exist** in LangExtract (`max_workers`, `batch_length`). Nothing to build for the LangExtract path.
- **STARA lessons: the published repositories hold no code or prompts.** Nothing can be reused; the method comes from the paper, which has now been read.
- **STARA lessons: two figures corrected in place.** The full system's precision is 0.98, not 0.96, and the paper's context list does not name cross-references as a separate item.

### Fix before the first LangExtract run

A. **Set `max_char_buffer` above the longest provision.** The default of 1,000 characters splits longer provisions, and a span across the split is lost.
B. **Use `char_interval`, not `text.find`,** in `keep_grounded`. `find` returns the first occurrence, so a second mark of a repeated phrase is dropped as an overlap.
C. **Record `alignment_status` on every candidate** and accept `match_exact` only. Fuzzy alignment is on by default in the library.
D. **Pass `additional_context`** from `textlib.context_for` (this is item 1; it is now known to be possible).
D2. **Add the two kinds of context STARA uses that `context_for` lacks.** STARA attaches four things to each unit: headings, definitions of terms used in it, the lead-in sentence a list item completes, and trailing provisos from following units. `context_for` sends headings, parent text and cross-referenced text. It does not look up defined terms or following provisos.
D3. **Check provision size.** STARA found units under 100 words lack context and units over 2,000 words are unreliable, and aims for about 1,000. Report the word count of each provision and merge or split the outliers before extraction.

### Accuracy

E. **Treat the hand marks as a reference, not as truth.** STARA's benchmark found 135 of 181 apparent false positives were correct and missing from the attorneys' list. In `tools/evaluate.py` (item 3), a candidate span the hand marks lack goes to an adjudication list with three outcomes: model wrong, hand marks wrong, both defensible. Report precision before and after adjudication.
F. **Keep the two example provisions out of the score.** They are shown to the model, so scoring them measures copying.
G. **Measure run-to-run stability.** Run each provision three times and report the share of spans that appear in all three. Hsu's target for repeat-run agreement is above 0.95.
H. **Tag each provision with the structural tasks it needs**: defined term, cross-reference, lead-in clause, amendment. Report accuracy by tag, so a failure points to missing context of a named kind.
I. **Say in the prompt how to treat provisions limited to past tax years.** Most of our provisions are. Many of the 44 reasoning errors in STARA's benchmark came from a prompt that did not say whether provisions with "historical effect only" count.
J. **Give every source a verification record.** Fields: `support_type` (quoted or paraphrased), `verifier_status` (unverified, verified, contradicted), `method`, `checked_on`. The validator fails an `agency_published` value whose agency source is not `verified`.
K. **Snapshot agency pages.** Store the page text under `sources/<id>/` with `url`, `retrieved` and `sha256`, and have the validator confirm each recorded `quote` is in the stored text. Today the quotes are checked against nothing.
L. **Decide a re-verification schedule.** A snapshot does not notice change. Suggested: re-read every agency source each January, when new forms are published, and after each legislative session.
M. **Add a staleness class to each provision in the manifest**: active, partially amended, formally superseded, effectively dead, unknown. The four conflict provisions are "partially amended" now, and this replaces item 2's single flag with something the viewer can show.
N. **Keep README claims no stronger than the checks.** Two of Hsu's repositories state more than their code tests. Add a short table to the README: each claim, and the script and check that enforces it.

### Parameters

O. **2023 EITC share: done.** The 2023 form says 50%; the parameter file now records it with a conflict note.
P. **EITC from 2027: a decision is needed.** The Department's table reads "2026 and later 25%". It is not recorded for 2027, because HB24-1134 has not been read and the percentage may depend on a revenue trigger. Either accept the agency's row as an `agency_published` value with that caveat, or keep refusing until the act is read.
Q. **Amendment 87: sources done, ingestion not.** The brackets are confirmed from the measure's text. They are not indexed and do not vary by filing status. Still to do: ingest the text into `text/`, mark spans, add effective dates so (1.7)(c) ends with 2026, and model proposed (1.8)(b) on principal-residence gain. Watch for certification of the result.
R. **HB24-1134 and the 2026 rate: still open.** The bill page refused the download. The Department's rate table still stops at 2025.
S. **Cross-check against PolicyEngine in a script** (`tools/crosscheck_policyengine.py`) that fetches its two Colorado parameter files at run time and reports differences. Fetch, do not copy: PolicyEngine is AGPL-3.0. A manual comparison is in the research note; after the 2023 correction the two agree on every value both record.
S2. **Model the form's tax table** for taxable income under $50,000, as a separate rule from the statutory rate, so the engine can reproduce the amount on the form as well as the amount the statute implies.
S3. **Take official tests from the 104 Books.** Each year's tax table gives hundreds of income and tax pairs. A script could turn a table into test cases once S2 exists.

### Scalability

T. **Item 7, specified.** Cache by provision hash, prompt hash and model. Add a replay mode that fails on a cache miss instead of calling a model, so a published run can be reproduced without a key. Pin the model id in the output file. Add a call budget.
U. **Item 9, extended.** Add the columns `staleness_class`, `supersedes` and `superseded_by` to the inventory, and report the share of rows with no decision.

### Usability

V. **Item 12, specified.** Review states: `auto_ok`, `needs_review`, `accepted`, `rejected`, `modified`. Each record has `subject_id`, `state`, `from_state`, `reviewer`, `date`, `rationale`. Reviewer verdicts are final until the text hash changes. Anything a model produced starts at `needs_review`.
W. **State the under-25 and ITIN limit in the README.** Colorado extends the credit to filers the federal credit excludes. A caller who passes the federal amount for such a filer gets the wrong result.
X. **Item 13: one content store, two readers.** Hsu's FR 2052a site serves the same records as pages and through an `/llms.txt` index. A static `web/llms.txt` listing provisions, parameters and tests would do this with no server.

### What not to adopt

- **A typed-operation calculus for amendments.** Hsu's own held-out test found it no more accurate than a plain model; its value was auditability. With two sections ingested, the validator already gives us that.
- **Model judges for our output.** Our checks are mechanical (verbatim, re-parse, source agreement). A judge would add a less reliable check on top of a more reliable one.

### Status of these proposals

Implemented on 11 November 2026, after the proposals were accepted:

| Item | State |
|---|---|
| A, B, C, D | Done. The script sets the chunk size, uses the library's character offsets, accepts exact matches only, and passes context. |
| D2 | Done for lead-ins and provisos. Definitions are looked up, but the ingested text defines no quoted terms, so that path is untested on real text. |
| D3 | Partly. Each provision's word count is recorded; the longest is 145 words and 28 of the 33 are under 100, the size below which STARA found context lacking. Nothing is merged or split. |
| E, F | Done in `tools/evaluate.py`: disagreements go to `extractions/adjudication.json`, and example provisions are left out. |
| G | Done as a report: give `evaluate.py` several runs. No real runs exist yet. |
| H | Not done. Provisions are not tagged by the structural task they need. |
| I | Done in the prompt. |
| J | Done differently. Verification is computed by the validator, not recorded by hand: a source is verified when its quote is found in a stored copy. |
| K | Done. `sources/` holds nine documents. |
| L | Not done. No re-verification schedule is set. |
| M | Partly. A provision can record that a later instrument ends its effect (`superseded-from`). The four-way staleness class is not added. |
| N | Done. See "What each claim rests on" in the README. |
| O, Q | Done, except the principal-residence rule, which the engine refuses instead of modelling, and the parts of the measure outside (1.8). |
| P, R | Open. They need HB24-1134. |
| S | Not done as a script. The manual comparison stands. |
| S2, S3 | Done. Rule `co.income_tax.form_table`, and `tools/make_table_tests.py`. |
| T | Done, except the call budget. |
| U | Not done. There is no inventory yet (item 9). |
| V | Partly. `evaluate.py` records decisions on disagreements. Per-provision review status and viewer buttons are not built. |
| W | Done, and taken further: the caller states the basis of the federal amount. |
| X | Not done. |

Numbered items this also closed: 1 (context is sent; the with and without comparison awaits a real model), 3, 4, 7, 8, 11, and "add effective-date ranges" in part.

Blocked: item 6 and item 10, ingesting the current official text. The host that serves it was not allowed.

### Next for the data dictionary

1. Give the model a bracket example. Gemini marked no thresholds in the 2027 bracket list under instructions that ask for them; the two example provisions contain none.
2. Mark the 14 provisions that have a type and no marks: the (2.5) and (2.7) credit variants, the first five bracket items, apportionment and the benefit disregard.
3. Read the sections behind the provisional types (39-22-104(3) and (4), 39-22-110) and confirm or revise them.
4. Ingest the amended 39-22-123.5 and 39-22-627, which need the `trigger`, `delegation` and `temporary_rate_adjustment` types and the `index` class.
5. Record inclusive and exclusive edges on thresholds, and deltas and replacements on values. The dictionary names them; nothing parses them yet.
6. Have a person decide who may change the dictionary and whether a change needs a second reviewer.

### Suggested order from here

1. A real LangExtract run, with and without context, then adjudication of the disagreements.
2. Item 6, if `olls.info` is allowed.
3. HB24-1134, then the decision in P.
4. The inventory (item 9 with U) and the review workflow (item 12 with V).

## Open decisions

- **Licence.** Settled: the repository is Apache 2.0 (`LICENSE`). USWDS files keep their own licences (`web/assets/uswds/LICENSE.md`).
- **Governance.** Deferred. `docs/research/tradeoffs-report.md` covers stewardship models and precedents.
- **Model provider** for LangExtract runs. LangExtract ships Gemini, OpenAI and Ollama providers. It has no Anthropic provider; Claude is reachable only through the community LiteLLM plugin.

## Research in this repository

- `docs/research/tradeoffs-report.md`: the full tradeoffs report (structured text, parameters, engines, governance, sequencing after Amendment 87), with a section on what is unverified.
- `docs/research/notes/`: the five sets of source notes behind it.
- `docs/research/notes/stara_hsu_followup.md`: the follow-up to this roadmap's STARA and Hsu sections, with what was read and what could not be.

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
