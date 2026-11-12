# Follow-up research: STARA, Hsu, and the sources the roadmap left open

Written 11 November 2026, in a cloud session, in two passes. It continues the research recorded in `docs/ROADMAP.md` and closes, or fails to close, the gaps that file named. Proposals drawn from it are in the roadmap under "Proposed changes from the follow-up research".

## How this was read, and what could not be

In the first pass the network allowed GitHub and web search only. In the second, a new environment also allowed the legislature (`leg.colorado.gov`, `content.leg.colorado.gov`), the Department of Revenue (`tax.colorado.gov`), the Secretary of State, `arxiv.org` and three Stanford hosts.

Each finding below carries one of three marks:

- **Read**: the page or file itself was fetched and read.
- **Search**: taken from a search engine's summary of a page that was not opened. Treat as a lead, not a source. Nothing marked Search may go into `parameters/`.
- **Not read**: the source exists and was not reachable.

Still not read: Hsu's Substack posts, HB24-1134 (the bill page refused the download with HTTP 406), the 2026 statute files (hosted on `olls.info`, not on the allowed list), the Stanford HAI brief, and any certified election result.

**A caution from this work.** The first pass took one lead from a search snippet that turned out to be wrong when the document was read: a mention of "$510,834" looked like an inflation-indexed threshold. It is the income at which Amendment 87 stops being a tax cut, and the Blue Book says the brackets are not indexed. Section 6 records what was read. This is the reason for the Read and Search marks.

## 1. PolicyEngine's Colorado parameters (Read)

Files read from `PolicyEngine/policyengine-us` on `main`: `parameters/gov/states/co/tax/income/credits/eitc/match.yaml`, `parameters/gov/states/co/tax/income/rate.yaml`, and `tests/policy/baseline/gov/states/co/tax/income/credits/eitc/co_eitc.yaml`. The repository is AGPL-3.0.

| Parameter | Tax year | This repository | PolicyEngine | Agree |
|---|---|---|---|---|
| EITC share | 2022 | 0.20 (statute snapshot) | 0.20 | Yes |
| EITC share | 2023 | 0.25 (statute snapshot) | 0.50 | **No** |
| EITC share | 2024 | 0.50 (agency) | 0.50 | Yes |
| EITC share | 2025 | 0.50 (agency) | 0.50 | Yes |
| EITC share | 2026 | 0.25 (agency) | 0.25 | Yes |
| EITC share | 2027 to 2033 | not recorded | 0.25 (carried forward) | n/a |
| EITC share | 2034 on | not recorded | 0.10 | n/a |
| Rate | 2022, 2023 | 0.044 | 0.044 | Yes |
| Rate | 2024 | 0.0425 | 0.0425 | Yes |
| Rate | 2025 | 0.044 | 0.044 | Yes |
| Rate | 2026 | 0.044 (statutory default) | no entry after 2025 | n/a |
| Rate | 2027 | six brackets (news report) | nothing | n/a |

What this shows:

- **A fifth conflict, for 2023, now confirmed and corrected.** PolicyEngine records 50% for 2023 and cites the Department of Revenue's 2023 104 Book. When the first pass ran, this repository recorded 25% from the statute snapshot alone (the table above shows that state). The second pass read the booklet: form DR 0104CR, line 5, says "COEITC, multiply line 4 by 50% (0.50)". The parameter file now records 50% with a conflict note. See section 6.
- **Every value we already took from the agency matches.** That is some independent support for the four known conflicts being resolved the right way.
- **PolicyEngine does not help with our two unknowns.** It has no 2026 rate and nothing for Amendment 87. It carries 25% forward to 2033 as a default, with a comment that the match "can rise higher depending on state revenue", which is the trigger our snapshot's heading mentions and its text lacks.
- **Its reference list is a map to official test material.** It cites the 104 Book for each year by page: 2022 (`DR_104_Book_2022.pdf`, pages 16 and 19), 2023 (`Book0104_2023.pdf`, pages 18 and 21), 2024 (`DR0104_book_2024.pdf`, pages 11 and 25), 2025 (`Book104_2025.pdf`, pages 11 and 25). Those are the documents the roadmap wants for official tests and for the rounding rule.
- **Its tests go further than our slice.** They cover Colorado's expansion of the credit to filers under 25, to filers with an ITIN, and to homeless and foster youth. Our engine takes the federal credit as an input, so a caller who passes the federal amount for one of these filers gets the wrong state credit. That is a limit the README does not yet state.
- **Licence.** AGPL-3.0 code and test files cannot be copied into this Apache 2.0 repository. The values are facts and can be compared; the YAML should be fetched at check time, not vendored.

## 2. LangExtract as it actually is (Read)

Read from `google/langextract` on `main`: `README.md`, `langextract/extraction.py`, `langextract/core/data.py`, `pyproject.toml`, `COMMUNITY_PROVIDERS.md`. Latest release v1.7.2; `requires-python >= 3.10`; Apache 2.0. The signature was read on `main` and not checked against the v1.7.2 tag.

The roadmap asked whether `lx.extract` accepts `additional_context`. It does. The full list of what matters to us:

| Parameter | Default | Consequence for `tools/extract_langextract.py` |
|---|---|---|
| `additional_context` | `None` | Exists. The script does not pass it yet. |
| `max_char_buffer` | `1000` | The script does not set it, so any provision longer than 1,000 characters is split into chunks, and a span that crosses a chunk edge cannot be found. |
| `extraction_passes` | `1` | With more than one pass, results are merged and "first extraction wins for overlaps". It raises recall; it is not a vote. |
| `max_workers`, `batch_length` | `10`, `10` | Parallelism is built in, limited to the smaller of the two, and documented as "Supported by Gemini models". |
| `context_window_chars` | `None` | Carries text from the previous chunk; relevant only if chunking stays on. |
| `resolver_params` | fuzzy alignment on, threshold 0.75, `accept_match_lesser` true | By default the library will align a span that is only roughly in the text. |
| `model_id` | `gemini-3.5-flash` | Matches the script's default. |

Each extraction comes back with `char_interval` (start and end offsets, or `None` when the text could not be located) and `alignment_status` (`match_exact`, `match_greater`, `match_lesser`, `match_fuzzy`).

Two defects in our script follow from this:

1. `keep_grounded` ignores `char_interval` and calls `text.find`, which returns the first occurrence. Where a phrase occurs twice in a provision, the second mark is treated as overlapping the first and dropped.
2. It does not record `alignment_status`, so a fuzzy match that happens to be verbatim elsewhere in the provision is indistinguishable from an exact one.

Providers: Gemini, OpenAI and Ollama are built in. There is no Anthropic provider; the only route to Claude is the community LiteLLM plugin. This bears on the open "model provider" decision, since comparing against the model that made the hand marks needs that plugin or a second, direct script.

## 3. RegLab's lawscraper (Read)

Read: the repository root, `README.md`, `ms_fl_scraper.py`, `scraper_utils.py`, the `codes/` listing and the commit list.

- **No licence file**, so no right to reuse the code is granted. Last commit 30 October 2025.
- **It scrapes Justia and FindLaw**, which are unofficial mirrors of the kind that put our text out of date in the first place.
- **Colorado is in its state tables but not in its output.** The published `codes/` folder holds AK, AL, AR, AZ, CA, CT, KS and UT only.
- **The FindLaw parser keeps the first paragraph of each section only** (`select_one("div.codes-content p")`), so multi-paragraph sections are truncated.
- **Its record is flat**: `url`, `state`, `path`, `title`, `univ_cite`, `citation`, `content`, `lex_path`. No subsection hierarchy, no definitions, no cross-references.

Conclusion: roadmap item 10 said to "look at `lawscraper` first". It has been looked at and should not be used. It would reproduce the staleness problem, lose text, and cannot legally be copied.

RegLab's `stara` and `stara_public` repositories contain only a pointer to the project website. No STARA code, prompts or schema are published on GitHub.

## 4. STARA and LaborBench (Read)

Both papers were read in the second pass: "What Is the Law? A System for Statutory Research (STARA) with Large Language Models" (ICAIL 2025) and "Benchmarking Legal RAG: The Promise and Limits of AI Statutory Surveys" (arXiv 2603.03300).

### Method

- **The unit is the smallest enumerated provision**, not the section. Each unit keeps its numbering, text, parents and children.
- **Units are then resized.** "Provisions shorter than 100 words often lack sufficient context for effective extraction, while those longer than 2,000 words tend to be too complex for reliable LLM processing." Small related units are merged and large ones split, aiming at about 1,000 words.
- **Each unit gets up to four pieces of context**:
  1. a heading: citation, position in the code, and the titles of its parent divisions;
  2. definitions of terms that appear in the unit and are defined in a relevant part of the code;
  3. lead-ins ("chapeaus"): the opening of a sentence that a list item completes;
  4. suffixes: provisos or continuations in following units that change the unit's meaning.
- **Definitions are scoped.** A definition that says "for purposes of this Chapter 41" is attached to every unit inside Chapter 41 and to no others. This takes pattern matching, model-based parsing and scope logic over the hierarchy.
- **Parsing varies by code.** For the U.S. Code they use the House's XML. For others they use regular expressions for structural markers, definitions and cross-references.
- **A search runs in four steps**: the user describes what counts as relevant; a model turns that into a detailed prompt with multi-step criteria, with positive and negative examples if the user gives them; an optional broad keyword filter makes a shortlist; a model classifies every shortlisted unit, gives its reasoning, and extracts named fields.
- **The model was Llama 3.3 70B.** The gain came from context, not from a frontier model.

### Results

Ablation on the federal criminal statutes task (Table 4 of the paper):

| Configuration | Precision | Recall | Extraction |
|---|---|---|---|
| Base | 0.58 | 0.990 | 0.28 |
| + Prompt engineering | 0.76 | 0.987 | 0.32 |
| + Basic context | 0.96 | 0.984 | 0.70 |
| Full system | 0.98 | 0.998 | 0.76 |

Recall was high in every configuration. Context bought precision and extraction quality. The roadmap had recorded the full system's precision as 0.96; it is 0.98.

On the same task, Gemini Deep Research reached recall 0.144, OpenAI Deep Research 0.044 and Westlaw's survey tool 0.072.

### What the benchmark paper adds

- **135 of STARA's 181 apparent false positives were correct**: provisions the Department of Labor's attorneys had missed. Every flagged case was checked by hand. Corrected accuracy is 92%, up from 83%.
- **44 were reasoning errors, and many of those were ambiguity in the question.** "A statute can remain in the code with historical effect only, and the prompt does not specify whether such expired provisions should count."
- **2 were system errors**: citing another state's provisions.
- **69 false negatives**, some because the rule lived in a regulation or an agency interpretation and STARA searched statutes only.
- The paper's own limits: one legal domain, and the commercial tools' false positives were not all checked.

Its stated limits in the first paper: the keyword pre-filter can drop relevant provisions, and results are not de-duplicated.

### What this means for us

- A human-made reference list is not ground truth. A candidate span the hand marks lack is a disagreement to adjudicate.
- Our `context_for` sends headings, parent text and cross-referenced text. It does not look up defined terms, and it does not carry trailing provisos. Parent text covers lead-ins only where the lead-in is the parent's own text.
- Most of our provisions are limited to past tax years. The prompt has to say how to treat them.
- The rule for a year can live outside the statute. For us that is the Department of Revenue's forms and tables, which is where four of the five conflicts were found.

## 5. Hsu's work since the roadmap was written (Read)

The roadmap covered two repositories. His account has 27 public ones. Read here: `policy-sludge-cleanup` (README, `references/templates.md`, `scripts/sludge_audit.py`), `bank-board-policy-sludge` (README and the judge instructions), `fr2052a-policy-as-code`, `fin-reg-sludge-evals` (README and `EVAL-FRAMEWORK.md`), and `board-duties-distill` (README, `AGENTS.md`, the product spec, the B0 and B6 task files, and five source files). The paywalled "Policy as code" post is still unread.

### 5.1 `board-duties-distill` (October 2026; Apache 2.0 code, CC BY 4.0 documents)

The closest project to ours found so far: it reduces 227 board-duty statements to 26, with every claim tied to source text.

- **Claims carry their own verification state.** `LegalClaim` has `source_span_ids`, `support_type` (`quoted` or `paraphrased`), `authority_type` (statute, regulation, enforceable guideline, guidance, manual, comparator, secondary), `as_of_valid`, `confidence`, and `verifier_status` (`unverified`, `verified`, `contradicted`, default `unverified`). A separate `VerifierRecord` names the `method`: `span_present`, `quote_match`, `cross_reference`, `manual` or `live_retrieval`.
- **Sources are cached and hashed.** Each document is stored under `data/sources/<source_id>/` with a manifest of `url`, `retrieved_at` and `sha256`, so a run "replays offline, byte-identical". We do this for statute text and not for the agency pages our values rest on.
- **Model output is cached by `(model, prompt_sha256)`**, the model is pinned, replay mode raises an error on a cache miss instead of calling out, and there is a call and token budget. This is roadmap item 7 with the details filled in.
- **Borderline matches are never auto-verified.** A fuzzy anchor score between 0.40 and 0.60 goes to a human.
- **Unanchored output is dropped, not passed through**, and the hallucinated-citation rate is a release gate that must be zero.
- **Review is a small state machine.** `ReviewDisposition` has `subject_id`, `state`, `reviewer_id`, `timestamp`, `rationale`, `from_state`. States: `auto_ok`, `needs_review`, `reviewer_accepted`, `reviewer_rejected`, `reviewer_modified`. Reviewer verdicts are terminal. The model never settles a normative question.
- **"No baseline" has its own value.** Each finding gets an effect class: `codify`, `clarify`, `fill_gap`, `change` or `unresolved`. `unresolved` is what results when there is no baseline to compare against: "Never guess".
- **Held-out validation uses a sealed answer key.** The pipeline cannot read the key; a test guards the path; model output is scanned for leakage.

Three things the project reports against itself, which are the most useful part:

- Its README says "142/227 pinned verbatim". The offline check in `verify.py` says of itself that it "checks *citation presence*, not that the cited law says what the claim asserts". **The claim is stronger than the check.** Our build does compare text, which is a real difference, and the lesson is to keep README wording no stronger than what the code tests.
- On held-out data its typed-operation engine scored "~0 delta vs the plain-LLM baseline on grouping" (F1 0.52, precision 0.92, recall 0.36). Its own conclusion is that the method "generalizes as a structuring/auditing discipline, not as a better clusterer than a capable LLM". **Structure bought auditability, not accuracy.**
- "B1 pins a snapshot; it does not subscribe to changes." No re-verification schedule is decided. We have the same gap: the agency pages were read once, on 11 November 2026.

Also: 85 of the 227 statements remain unverified, and the README says so.

### 5.2 `fin-reg-sludge-evals` (a plan, not results)

Five evaluations for models reading regulation. Three map directly onto our extraction task:

- **Consistency.** The same question in 8 to 10 phrasings, three runs each. Targets: agreement across phrasings above 0.90, across repeat runs above 0.95.
- **Structural comprehension.** Four task types: definition resolution, cross-reference chains, lead-in clauses, and amendment recognition. The "structural trap" is answering from a word's ordinary meaning when the text defines it.
- **Staleness.** Four classes: formally superseded, effectively dead ("technically still on the books" and inoperative), partially amended, still active. Metrics include a false-staleness rate.

The others are conflict detection and calibration (expected calibration error below 0.10). Shared scoring codes: `CORRECT`, `INCORRECT`, `AMBIGUOUS`, `REFUSED`, `HALLUCINATED`.

### 5.3 More detail on the two repositories the roadmap already cites

- **Rubric weights** (`bank-board-policy-sludge`): coverage 20, source and citation integrity 25, substantive accuracy and currency 20, sludge-analysis quality 15, structure 10, calibration and transparency 10. Seven flags: fabricated source, misattribution, stale presented as current, invented obligation, false exhaustiveness, scope evasion, unsupported central legal conclusion.
- **Citation checks** sample 20 citations per report with a fixed seed. Verdicts: `SUPPORTS`, `WRONG-ATTRIBUTION`, `NOT-SUPPORTED`, `STALE`, `FABRICATED`, `UNVERIFIABLE`. Anything that cannot be checked is marked `UNVERIFIABLE` "rather than guessing". A human confirms every `FABRICATED` or `STALE` verdict.
- **Judges** "disagree in strictness, not in ranking", and "can both miss real citation errors and over-flag good ones".
- **Inventory columns** (`policy-sludge-cleanup`), in order: `instrument_id`, `title`, `issue_date`, `instrument_type`, `issuing_unit`, `entity_types`, `theme`, `status`, `supersedes`, `superseded_by`, `triage`, `destination_cell`, `triage_rationale`. Status values: live, superseded, expired, spent, unknown.
- **A triage warning**: "RETAIN above ~5% of the stock signals triage avoidance."
- **The audit script does less than its documentation says.** The templates say it reports rows missing from a mapping appendix; the script only checks for a blank `destination_cell`. Same lesson as 5.1.

### 5.4 `fr2052a-policy-as-code`

147 Markdown files with YAML front matter, served to people as pages and to programs through a small API, an `/llms.txt` file and an MCP server with 11 tools. No evaluation. Relevant to roadmap item 13 only as a pattern: one content store, two readers.

## 6. Colorado sources (Read)

Read in the second pass. Values taken from them are recorded in `parameters/` with the quote, the retrieval date and, for PDFs, a hash of the file.

### Amendment 87

- **The text.** Read from the legislature's copy, stamped "CDOS Received: January 9, 2026 ... 2025-2026 #195 - Final Text". Section 3 amends C.R.S. 39-22-104: it ends (1.7)(c), the flat 4.40%, with tax years beginning before 1 January 2027, and adds (1.8).
- **The brackets match what we had recorded** from The Colorado Sun: 3.70% up to $25,000; 4.20% to $100,000; 4.40% to $500,000; 7.40% to $750,000; 7.90% to $1,000,000; 8.40% above. Each rate applies only to the income in its band.
- **One schedule for everyone.** (1.8)(a) applies to "every individual, estate, and trust". There are no filing-status thresholds.
- **Not indexed.** The Blue Book: "Unlike the federal income tax, the new state income tax brackets are not adjusted for inflation".
- **The base** is federal taxable income, modified by subsections (3) and (4) as before.
- **Something we did not know about.** Proposed (1.8)(b) taxes gain on the sale of a principal residence, above the federal exclusion, at 4.40%. The engine does not model it.
- **Still subject to 39-22-627.** (1.8)(a) opens "Except as otherwise provided in section 39-22-627", so a temporary rate change could apply to the graduated rates. How is not stated.
- **Section 2 amends the TABOR section of the constitution**, article X, section 20 (8)(a). The Blue Book says the measure removes the single-rate requirement. Struck words do not survive conversion of the PDF to text, so exactly which words are struck was not seen. Section 4 applies the same six brackets to corporations.
- **Certification.** The Secretary of State's page lists the measure as certified for the ballot. No certified result was found.

### Earned income tax credit

- **The Department's credit percentage table** ("Income Tax Topics: Earned Income Tax Credit"): 2017 to 2021, 10%; 2022, 20%; 2023, 50%; 2024, 50%; 2025, 50%; "2026 and later", 25%.
- **2022 is now agency-backed** and agrees with the snapshot.
- **2023 is a fifth conflict.** The snapshot says 25%. The table says 50%, and so does the 2023 form (DR 0104CR, line 5). Corrected.
- **2027 is not recorded.** "2026 and later 25%" would fill it, and it is an agency statement. It was left out because HB24-1134 could not be read and PolicyEngine notes the percentage can rise with state revenue. This is a decision for the project owner; see roadmap item P.
- **Who can claim.** The same page confirms the credit reaches filers the federal credit excludes: from 2020, those without a Social Security number valid for employment; from 2022, certain filers under 25 without a qualifying child. For them the credit is a percentage of the federal credit they "would have been allowed". The README now states this limit.

### Rate, rounding and the tax table

- **The Department's rate table** still stops at 2025 (4.4%). The 2026 rate is unresolved.
- **The tax table.** "For individuals with Colorado taxable incomes of less than $50,000, the Department publishes tax tables which approximate the individual's Colorado tax determined at the applicable prescribed rate." The 2023 table uses $100 bands and gives the tax at the middle of each band: over $20,300 but not over $20,400 is $895, which is 20,350 times 0.044. The engine applies the rate to the exact income, so it can differ from the form by about two dollars below $50,000. This is a new limit, now in the README.
- **Rounding.** The 2023 booklet: "Round all dollar amounts to the nearest whole dollar." Exact half dollars were not checked.
- **A first official test.** One case in `tests/cases.json` now uses that table row and the form's 50% line.

### Official statute text

- The Office of Legislative Legal Services page "2026 CRS Titles for Download" says the files are "current with the changes made by amendments, additions, and repeals to Colorado Revised Statutes by the Seventy-fifth General Assembly at its Second Regular Session in 2026".
- The files are hosted on `olls.info`; the page links `https://olls.info/crs/crs2026-title-39.pdf` for Title 39. That host was not on the allowed list, so the file was not downloaded and the current text is still not ingested.
- From search only: the Attorney General's site says the LexisNexis site is the only official source.

## Sources

Read:

- https://github.com/PolicyEngine/policyengine-us (three files named in section 1, and `LICENSE`)
- https://github.com/google/langextract
- https://github.com/reglab/lawscraper
- https://github.com/reglab/stara and https://github.com/reglab/stara_public
- https://github.com/mhsu2112/board-duties-distill
- https://github.com/mhsu2112/fin-reg-sludge-evals
- https://github.com/mhsu2112/policy-sludge-cleanup
- https://github.com/mhsu2112/bank-board-policy-sludge
- https://github.com/mhsu2112/fr2052a-policy-as-code

Read in the second pass:

- STARA paper (ICAIL 2025): https://law.stanford.edu/wp-content/uploads/2025/08/STARA-Daniel-Ho.pdf
- LaborBench paper: https://arxiv.org/abs/2603.03300
- Amendment 87 final text: https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure
- Amendment 87 Blue Book: https://leg.colorado.gov/ballots/graduated-income-tax-2/files/blue-book
- Secretary of State, 2026 ballot measures: https://www.coloradosos.gov/pubs/elections/Initiatives/ballot/contacts/2026.html
- Department of Revenue, EITC topics: https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit
- Department of Revenue, Individual Income Tax Guide: https://tax.colorado.gov/individual-income-tax-guide
- Department of Revenue, 2023 104 Book: https://tax.colorado.gov/sites/tax/files/documents/Book0104_2023.pdf
- 2026 CRS titles download: https://content.leg.colorado.gov/agencies/office-legislative-legal-services/2026-crs-titles-download

Found by search and not opened:

- HB24-1134: https://leg.colorado.gov/bills/hb24-1134
- Attorney General on the official source: https://ag.colorado.gov/colorado-revised-statutes
- Colorado Politics, 6 November 2026: https://www.coloradopolitics.com/2026/11/06/colorado-passes-graduated-income-tax-eliminates-flat-rate/
- Proponents' fact sheet: https://protectcoloradosfuture.com/wp-content/uploads/2026/06/Colorado-Graduated-Income-Tax-Fact-Sheet.pdf
- Grant Thornton alert on HB24-1134: https://www.grantthornton.com/insights/alerts/tax/2024/salt/a-e/co-enacts-legislation-amending-combined-reporting-06-10
