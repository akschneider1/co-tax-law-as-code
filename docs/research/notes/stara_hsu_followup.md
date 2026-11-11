# Follow-up research: STARA, Hsu, and the sources the roadmap left open

Written 11 November 2026, in a cloud session. It continues the research recorded in `docs/ROADMAP.md` and closes, or fails to close, the gaps that file named. Proposals drawn from it are in the roadmap under "Proposed changes from the follow-up research".

## How this was read, and what could not be

The session's network allowed GitHub and web search only. Every other host was refused by the network policy, including `arxiv.org`, `*.stanford.edu`, `leg.colorado.gov`, `tax.colorado.gov`, `coloradosos.gov` and Substack.

Each finding below carries one of three marks:

- **Read**: the page or file itself was fetched and read (GitHub only).
- **Search**: taken from a search engine's summary of a page that was not opened. Treat as a lead, not a source. Nothing marked Search may go into `parameters/`.
- **Not read**: the source exists and was not reachable.

Still not read after this pass: the STARA paper, the LaborBench paper, the Stanford HAI brief, every Colorado government page, Amendment 87's text and Blue Book, and Hsu's Substack posts.

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

- **A probable fifth conflict, for 2023.** PolicyEngine records 50% for 2023 and cites the Department of Revenue's 2023 104 Book, line 5 (`Book0104_2023.pdf`, page 18). Our 25% comes from the statute snapshot alone, and our own caveat says the agency page we read does not state a 2023 figure. PolicyEngine is a secondary source and the booklet was not read here, so the parameter file is unchanged. The booklet has to be read before anything is recorded.
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

## 4. STARA and LaborBench (Search only; papers Not read)

The roadmap said the STARA paper's method details were incomplete. They still are. From search summaries of the ICAIL 2025 paper and of "Benchmarking Legal RAG: The Promise and Limits of AI Statutory Surveys" (arXiv 2603.03300):

- STARA runs in three stages: segment the code into provisions and attach chosen context (hierarchy, definitions, cross-references); have a model classify each provision, extract structured data and give its reasoning; then organise and report.
- On LaborBench (state unemployment insurance law, with a Department of Labor compilation as the reference), STARA scored 83% against 58% for Westlaw AI and 64% for Lexis+ AI.
- **135 of STARA's 181 apparent false positives were correct**: provisions the Department of Labor's attorneys had missed. Corrected accuracy is reported as 92%.
- Some remaining "errors" were ambiguity in the question: a provision can stay in the code "with historical effect only", and the prompt did not say whether expired provisions count.
- Real errors included citing the wrong state's provisions, twice.

If the 135-of-181 figure holds when the paper is read, it changes how roadmap item 3 should work. A human-made reference list is not ground truth. A candidate span the hand marks lack is a disagreement to adjudicate, not automatically a false positive.

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

## 6. Colorado facts the roadmap left open (Search only)

None of this may enter `parameters/` until the page itself is read.

- **Amendment 87.** Reported at about 51% on 6 November 2026, with one outlet noting the Associated Press had not called it. No certification found. It was Initiative 2025-2026 #195. The legislature hosts a "Final Text" (received 9 January 2026), a Legislative Council draft packet and the Blue Book, all under `leg.colorado.gov/ballots/graduated-income-tax-2/files/`. The proponents' fact sheet gives the same six rates and thresholds we recorded from The Colorado Sun. Other outlets describe the top of the schedule differently (7.4% above $500,000 rising to 8.4% above $1 million, or 8.4% above $2 million), so the news reports do not agree with each other.
- **A hint that thresholds are indexed.** A snippet of the Legislative Council analysis refers to "Colorado taxable income of $510,834", which is not one of the round thresholds. Our 2027 caveat lists indexing as unknown; this suggests the answer is yes and that the round figures may not be the 2027 figures.
- **EITC from 2027.** A snippet of the Department of Revenue's "Income Tax Topics: Earned Income Tax Credit" page reads "2026 and later: 25%". The page we did read speaks only to 2026. If the topics page says this, the 2027 gap can be filled from an agency source.
- **The EITC trigger.** The HB24-1134 summary is reported to tie higher percentages for 2026 and later to an "estimated adjustment factor" (30% of the federal credit at 3% growth, up to 50% at 3.75%). This looks like the "trigger" missing from our snapshot. A Grant Thornton alert gives 35% as the 2025 base before the trigger, which would make the agency's 50% for 2025 a triggered value, not a statutory one.
- **The 2026 rate.** No Department of Revenue announcement of a 2026 reduction was found. Unresolved, as before.
- **Official text.** The Office of Legislative Legal Services has a "2026 CRS Titles for Download" page, described as current through the 2026 Second Regular Session, with uncertified HTM, PDF and DOCX files. The 2025 page says some Title 39 sections exist only as PDF. The Attorney General's site says the LexisNexis site is the only official source.

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

Found by search and not opened:

- STARA paper (ICAIL 2025): https://dl.acm.org/doi/10.1145/3769126.3769219
- LaborBench paper: https://arxiv.org/abs/2603.03300
- Amendment 87 final text: https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure
- Amendment 87 Blue Book: https://leg.colorado.gov/ballots/graduated-income-tax-2/files/blue-book
- Secretary of State, 2026 ballot measures: https://www.coloradosos.gov/pubs/elections/Initiatives/ballot/contacts/2026.html
- Department of Revenue, EITC topics: https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit
- HB24-1134: https://leg.colorado.gov/bills/hb24-1134
- 2026 CRS titles download: https://content.leg.colorado.gov/agencies/office-legislative-legal-services/2026-crs-titles-download
- Attorney General on the official source: https://ag.colorado.gov/colorado-revised-statutes
- Colorado Politics, 6 November 2026: https://www.coloradopolitics.com/2026/11/06/colorado-passes-graduated-income-tax-eliminates-flat-rate/
- Proponents' fact sheet: https://protectcoloradosfuture.com/wp-content/uploads/2026/06/Colorado-Graduated-Income-Tax-Fact-Sheet.pdf
- Grant Thornton alert on HB24-1134: https://www.grantthornton.com/insights/alerts/tax/2024/salt/a-e/co-enacts-legislation-amending-combined-reporting-06-10
