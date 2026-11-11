# Rules-as-code engines and approaches for encoding Colorado state tax law (as of November 2026)

Researcher note on method: about 40 search/fetch calls on 2026-11-11. Repository facts come from GitHub pages and the GitHub contents API read that day. Several GitHub fields (last-commit dates, contributor counts, release dates) did not render in the fetch tool and are listed under Gaps rather than guessed. Items marked "UNVERIFIED RECOLLECTION" in Gaps are background knowledge I could not confirm against a source in this session; the report writer should treat them as leads, not facts.

## 1. What does PolicyEngine's policyengine-us currently cover for Colorado, and what are its licence, testing, validation, contribution process and accuracy limits?

### Takeaway
policyengine-us already contains a substantial Colorado module: the individual income tax chain (additions, subtractions, exemptions, AMT, taxable income, non-refundable and refundable credits), the state EITC, CTC, Family Affordability credit, child care credit, care worker credit, senior housing credit, TABOR cash-back and sales tax refund, plus benefit directories for CCAP, CDHS, HCPF, DOI and state SSA supplements. It is AGPL-3.0, very actively developed (26k+ commits), validated mainly by cross-comparison with NBER TAXSIM rather than against administrative truth, and it has no transaction-level sales tax model.

### Cited Findings
- Colorado variable directory `policyengine_us/variables/gov/states/co/` contains: `ccap` (Colorado Child Care Assistance Program), `cdhs` (Dept of Human Services), `doi` (Division of Insurance), `hcpf` (Health Care Policy and Financing), `ssa` (state supplement), `tax`, and `co_child_care_subsidies.py`. — [GitHub contents API, co/](https://api.github.com/repos/PolicyEngine/policyengine-us/contents/policyengine_us/variables/gov/states/co)
- Colorado income tax directory contains sub-directories `additions`, `amt`, `credits`, `exemptions`, `subtractions`, and files `co_income_tax.py`, `co_income_tax_before_non_refundable_credits.py`, `co_income_tax_before_refundable_credits.py`, `co_income_tax_rebate_adjustment.py`, `co_non_refundable_credits.py`, `co_refundable_credits.py`, `co_taxable_income.py`, `co_withheld_income_tax.py`. — [GitHub contents API, co/tax/income](https://api.github.com/repos/PolicyEngine/policyengine-us/contents/policyengine_us/variables/gov/states/co/tax/income)
- Colorado credits directory contains: `care_worker`, `cdcc` (child and dependent care), `ctc`, `eitc`, `family_affordability`, `income_qualified_senior_housing`, `sales_tax_refund`, and `co_tabor_cash_back.py`. — [GitHub contents API, co/tax/income/credits](https://api.github.com/repos/PolicyEngine/policyengine-us/contents/policyengine_us/variables/gov/states/co/tax/income/credits)
- Colorado subtractions directory contains: `able_contribution`, `charitable_contribution`, `collegeinvest_contribution`, `military_retirement`, `pension`, plus `co_subtractions.py` and a catch-all `co_other_subtractions.py`. — [GitHub contents API, co/tax/income/subtractions](https://api.github.com/repos/PolicyEngine/policyengine-us/contents/policyengine_us/variables/gov/states/co/tax/income/subtractions)
- Licence is AGPL-3.0; the repo shows 26,272 commits on `main`, 171 stars, 220 forks; install example pins `policyengine-us==1.824.7`; supports Python 3.11 to 3.14. — [PolicyEngine/policyengine-us](https://github.com/PolicyEngine/policyengine-us)
- README describes the package as "a microsimulation model of the US state and federal tax and benefit system", and states that direct microsimulation via `Microsimulation()` is "deprecated" and "being migrated to `policyengine.py`"; this package remains the home of the rules and household-level calculations. — [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- Interpretive rule: "When a statute conflicts with a regulation, form, instructions, manual or stated agency practice, PolicyEngine US's rule is to follow the statute." Each conflict is recorded in a source-conflict register shared with the Axiom Foundation, and the code marks the deciding line with `# Source conflict <jurisdiction>:<id>`. — [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- README accuracy caveat: "Microsimulation results are estimates"; users are pointed to an external calibration-diagnostics site. — [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- The repo carries a Codecov badge, `.coveragerc`, `codecov.yml`, `CONTRIBUTING.md`, and also `AGENTS.md` and `CLAUDE.md` files (i.e., instructions for AI coding agents are part of the repo). — [PolicyEngine/policyengine-us](https://github.com/PolicyEngine/policyengine-us)
- Validation: PolicyEngine publishes `policyengine-taxsim`, described as an open-source drop-in TAXSIM-35 emulator; the project says PolicyEngine and TAXSIM "have been cross-validated against each other since 2021" across thousands of CPS households, under a memorandum of understanding with NBER and TAXSIM creator Daniel Feenberg, plus a three-way validation with the Atlanta Fed's Policy Rules Database. Years 2021 and later route to PolicyEngine, earlier years to TAXSIM35. — [policyengine-taxsim site](https://policyengine.github.io/policyengine-taxsim/)
- The emulator's comparison tooling uses a $15 tolerance for federal and state tax comparisons. — [policyengine-taxsim on PyPI](https://pypi.org/project/policyengine-taxsim/)
- A policyengine-us pull request (mirror of PR #8213, surfaced by search; I did not open the PR itself) reportedly lists residual numeric gaps versus TaxAct/TAXSIM including "CO ~$65 on income tax" after aligning an itemisation rule. — [mirror of PolicyEngine/policyengine-us PR 8213](https://1clonegithubbyxjn.1934672944.workers.dev/PolicyEngine/policyengine-us/pull/8213)
- PolicyEngine's own benchmark repo states its reference outputs are "PolicyEngine reference outputs, not administrative truth". — [PolicyBench mirror](https://tgfed.nhyvvfeijnh.workers.dev/PolicyEngine/policybench)
- Context on the law being encoded: Colorado tax is federal taxable income with adjustments times a flat rate (4.40% cited by Legislative Council Staff) less credits; many Colorado credits are refundable. — [Colorado Legislative Council Staff, individual income tax](https://content.leg.colorado.gov/agencies/legislative-council-staff/individual-income-tax); [Colorado DOR Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)
- Colorado credits change frequently: e.g., DOR notes the Colorado Works Program credit cannot be newly claimed for 2025 onward (carryforwards only); a July 2026 policy brief describes the Family Affordability Tax Credit as fully refundable. — [Colorado DOR December 2025 updates](https://tax.colorado.gov/december-2025-updates); [Appalachian State FEPL FATC brief, July 2026](https://fepl.appstate.edu/wp-content/uploads/2026/07/Colorado_FATC_policy_brief-072026.pdf)

### Inferences
- The Colorado credits named in the brief (state EITC, CTC, Family Affordability Tax Credit, TABOR refund mechanisms) all have directories in policyengine-us. I found no directory whose name corresponds to the Property Tax/Rent/Heat (PTC) rebate under `co/tax/income/credits`; it may live under `cdhs` or elsewhere, or be absent. This needs a direct repo check.
- The subtraction list is short (pension, military retirement, ABLE, CollegeInvest, charitable) with an `other_subtractions` catch-all input, which suggests the long tail of DR 0104AD subtractions and essentially all business credits are user inputs or unmodelled. Coverage is oriented to households in survey microdata, not full-return preparation.
- Because Colorado starts from federal taxable income, any Colorado encoding inherits the correctness of a federal model; PolicyEngine supplies that federal layer, which is the largest single argument for building on it.
- TAXSIM cross-validation is model-versus-model: agreement shows consistency, not correctness, and both can share a misreading. The "follow the statute over forms" rule means PolicyEngine may deliberately diverge from what DOR forms and commercial software compute.
- "Sales tax refund" in the repo is the TABOR refund paid via the income tax return, not a model of sales tax liability.

### Gaps
- Could not retrieve: Codecov percentage, number of Colorado YAML test files, last commit date, contributor count, latest release date (fields did not render).
- Did not read CONTRIBUTING.md in full (review requirements, CLA, changelog rules).
- Did not find published state-by-state TAXSIM match rates, or any Colorado-specific accuracy figure beyond the second-hand "$65" PR note.
- Did not confirm which tax years each Colorado credit is parameterised for, or whether 2025-2026 legislative changes are current.
- UNVERIFIED RECOLLECTION: PolicyEngine tests are YAML unit tests per variable plus integration tests, and each parameter YAML carries statute/form references; contributions go through GitHub PRs with a required changelog entry.

## 2. What is MyFriendBen, how does it use PolicyEngine, and what does its experience show?

### Takeaway
MyFriendBen is an open-source (MPL-2.0) Colorado benefits and tax-credit screener created by Gary Community Ventures and spun out as an independent nonprofit in 2025; it calls PolicyEngine's API for part of its calculations and runs its own Django rules for the rest. It is the clearest evidence that an open rules engine can sit behind a production Colorado service, but public material on accuracy or lessons learned is thin.

### Cited Findings
- MyFriendBen "was created by Gary Community Ventures, a Denver-based organization"; the backend is a "Python/Django rules engine", MPL-2.0, 3,763 commits; "currently live in Colorado and has been tested with over 40 benefits"; built "taking inspiration from AccessNYC, and connecting with PolicyEngine's API for benefits calculation". — [MyFriendBen/benefits-api](https://github.com/MyFriendBen/benefits-api)
- 2-1-1 Colorado piloted it in fall 2023; more than 55,000 Colorado households applied for about $33 million in benefits within two years; North Carolina was the first replication (with Code the Dream); the Denver national hub planned versions in five states in 2025; it "operates as an independent nonprofit". — [Gary Community Ventures case study](https://garycommunity.org/case-study/myfriendben/)
- PolicyEngine "powered MyFriendBen's eligibility calculations through its open-source rules engine", modelling SNAP, Medicaid, SSI, WIC and school meals, with TANF, CCDF and ACA premium tax credits being explored; derived tools include a Colorado Child Tax Credit Calculator and a Colorado Energy Savings Navigator. — [Gary Community Ventures case study](https://garycommunity.org/case-study/myfriendben/)
- MyFriendBen received a $2.4M grant to expand. — [Gary Community Ventures announcement](https://garycommunity.org/?p=6857)
- Larimer County partnered with MyFriendBen in February 2025. — [Larimer County](https://larimer.gov//spotlights/2025/02/13/larimer-county-partners-myfriendben-colorado-enhance-community-support)
- A 2026 policyengine-us changelog PR reportedly added Slack notices for "partner API contract test changes", indicating PolicyEngine maintains contract tests for API partners (bot-generated changelog, secondary). — [PolicyEngine API PR mirror](https://github.wyh1030873310.workers.dev/PolicyEngine/policyengine-api/pull/3631/)

### Inferences
- The split is instructive: roughly five large federal/state programmes come from PolicyEngine, while the "40+ benefits" total implies most local and smaller programmes are encoded in MyFriendBen's own Django code. A hybrid (upstream for the federal/state core, local code for the long tail) is the pattern actually in production in Colorado.
- MyFriendBen is a screener ("may be eligible", estimated value), a lower accuracy bar than tax computation or determination; its success does not demonstrate return-grade accuracy.
- MPL-2.0 (file-level copyleft) for MyFriendBen versus AGPL-3.0 for PolicyEngine: MyFriendBen consumes PolicyEngine over an API rather than importing it, which avoids AGPL obligations on its own code.

### Gaps
- No public post-mortem or accuracy audit of MyFriendBen's PolicyEngine integration was found; the case study's only lesson is that the engine helped keep rules current "as policies evolved".
- Did not confirm the current (late 2026) list of states or which Colorado tax credits MyFriendBen computes via PolicyEngine versus locally.

## 3. How do the main engines compare (OpenFisca/PolicyEngine, Catala, IRS Fact Graph, DMN/Drools, Blawx, Cosilico/RAC and other AI-assisted efforts)?

### Takeaway
The options split into three families: vectorised formula engines aimed at population simulation (OpenFisca, PolicyEngine), statute-shaped languages aimed at faithful, auditable computation (Catala, Blawx), and interview/decision engines aimed at service delivery (IRS Fact Graph, DMN/Drools). Only PolicyEngine has Colorado content today; Catala has the strongest statute traceability but an admittedly unstable compiler and no US state content; the Fact Graph is public and reusable but its host programme, Direct File, was suspended in October 2025 and did not run in 2026.

### Cited Findings
**PolicyEngine / OpenFisca**
- policyengine-us is AGPL-3.0, Python, 26,272 commits; README separates rules (this package) from population simulation (moving to `policyengine.py`). — [PolicyEngine/policyengine-us](https://github.com/PolicyEngine/policyengine-us)
- OpenFisca is described by a rules-as-code commentator as "designed specifically to process large number of queries simultaneously", and classed with Blawx as a rules-as-code tool as distinct from Drools, a production rules engine. — [Computational Law Diary, "Drooling over Rules as Code"](https://medium.com/computational-law-diary/computational-law-diary-drooling-over-rules-as-code-52aa0470b792)

**Catala**
- Apache-2.0, 2.4k stars, 120 forks, 5,808 commits; described as a domain-specific language for deriving algorithms from legislative texts, annotated article by article, producing a lawyer-readable PDF; embeds default logic based on Sarah Lawsky's work; designed with law professionals so that lawyers can review and certify the code. README states: "The compiler is yet unstable and lacks some of its features." It is an Inria research project with partial formal certification of the compiler. Tooling: VS Code extension, LSP server, test-suite interface, formatter (`catala-format`), Zulip chat. — [CatalaLang/catala](https://github.com/CatalaLang/catala)
- The Catala paper (Merigoux, Chataing, Protzenko, ICFP 2021) evaluated the language on IRC section 121 (US federal income tax) and French family benefits and "uncover[ed] a bug in the official implementation"; it claims a "correct-by-construction executable specification". — [arXiv 2103.03198](https://arxiv.org/abs/2103.03198)
- A later paper says Catala programs closely follow the logical structure of statutes, enabling "a pair programming and literate programming methodology". — [Springer/DeepDyve, "Catala: moving towards the future of legal expert systems"](https://plosjournal.deepdyve.com/lp/springer-journals/catala-moving-towards-the-future-of-legal-expert-systems-DMpEOYeZb2)
- A Catala 1.0.0 package exists on the OCaml registry (no date retrieved). — [ocaml.org catala 1.0.0](https://ocaml.org/p/catala/1.0.0/index.html)
- Mlang (same group) is a compiler for DGFiP's "M" language based on a reverse-engineered formalisation, validated against DGFiP's private test suite; the 2020 paper says DGFiP was "officially transitioning to Mlang for their production system". The Mlang repo reports passing all private DGFiP tests as of September 2022 for 2018-2021 income; the released DGFiP code was incomplete and the iterative "multiple liquidations" logic was never published, so the team built a separate DSL (M++). — [arXiv 2011.07966](https://arxiv.org/abs/2011.07966v3); [MLanguage/mlang](https://github.com/MLanguage/mlang)

**IRS Direct File and the Fact Graph**
- The Fact Graph repo describes itself as a "production-ready knowledge graph" for modelling US tax law including the Internal Revenue Code, usable from JavaScript or any JVM language; 427 stars, 54 forks, 70 commits; build files indicate Scala; development happens in a private repo with approved changes pushed publicly; README says "This repository is updated frequently" but also that the IRS does not "endorse, maintain, or guarantee the accuracy" of the code. — [IRS-Public/fact-graph](https://github.com/IRS-Public/fact-graph)
- The Fact Graph is described as a declarative business rules engine designed for reasoning about incomplete information, letting the software infer what it still needs to ask. — [Economic Security Project, Chapter 9: Direct File fact graph](https://economicsecurityproject.org/wp-content/uploads/Chapter-9_-Direct-File-fact-graph-and-a-new-way-of-building-civic-technology-products.pdf)
- IRS released most of the Direct File codebase publicly in 2025; commentary noted states could reuse it to build their own free filing platforms. — [GovCIO Media](https://govciomedia.com/irs-makes-direct-file-code-public-as-lawmakers-debate-programs-fate/); [NYSSCPA, 6 June 2025](https://nysscpa.org/news/1047571-irs-issues-direct-file-source-code-2025-06-06)
- Direct File usage: about 141,000 returns in 2024 (12 states) and over 309,000 in 2025 (25 states), against an IRS forecast of 450,000 to 1.25 million; satisfaction 90% and 94% "excellent" or "above average"; direct costs $32M (2024) and $41M (2025); GAO found the 2024 pilot successful. — [CRS In Focus IF13314, 17 Sept 2026](https://www.everycrsreport.com/files/2026-09-17_IF13314_7a5be865820f33882647d91cc0cadc376e538af6.html)
- Status: Treasury delivered the report required by P.L. 119-21 in October 2025 and simultaneously announced Direct File's suspension, citing cost, limited participation and other priorities; IRS told states "Direct File will not be available in Filing Season 2026" and "no launch date has been set for the future". As of 17 September 2026 it remained suspended; bills S. 3948 and H.R. 7806 would restore it. — [CRS IF13314](https://www.everycrsreport.com/files/2026-09-17_IF13314_7a5be865820f33882647d91cc0cadc376e538af6.html); [Federal News Network, Nov 2025](https://federalnewsnetwork.com/it-modernization/2025/11/irs-direct-file-will-not-be-available-in-2026-agency-tells-states/)
- Direct File integrated with several state online filing systems so users could also file state returns. — [CRS IF13314](https://www.everycrsreport.com/files/2026-09-17_IF13314_7a5be865820f33882647d91cc0cadc376e538af6.html)

**DMN / Drools**
- Drools is a Java rules engine needing Java and DRL expertise; DMN is an industry standard using decision tables and the FEEL expression language, portable between compliant products, and supported by Drools. — [Capital One, "The power of DMN"](https://www.capitalone.com/tech/software-engineering/decision-model-and-notation/); [Computational Law Diary](https://medium.com/computational-law-diary/computational-law-diary-drooling-over-rules-as-code-52aa0470b792)
- A University of Amsterdam paper proposes a systematic framework for assessing languages proposed for rules as code (useful as an evaluation rubric). — [UvA, "A Systematic Approach to Assess Languages Proposed for Rules as Code"](https://pure.uva.nl/ws/files/290695856/A_Systematic_Approach_to_Assess_Languages_Proposed_for_Rules_as_Code.pdf)

**Blawx**
- Open-source, web-based visual (block) tool for encoding, testing and running rules with explanations; its own page says it "is functional, but it is not production-quality software. It is intended for educational and experimental purposes." — [Lexpedite/blawx](https://www.github.com/Lexpedite/blawx)

**Cosilico / Rules Foundation / RAC / Axiom Foundation**
- Cosilico PBC describes itself as "Open source infrastructure for economic simulation" with claims "Every formula traced to statute", 50+ state tax systems, 100+ benefit programmes; says it is "built on Rules Foundation" open encodings and "provides commercial APIs on top"; sample output is marked "Sample output — API coming soon". No accuracy metrics on the landing page. — [cosilico.ai](https://cosilico.ai)
- Rules Foundation is presented as a 501(c)(3) with tagline "Encode the law" (an "OpenStreetMap for law"); core artefacts are a source archive in Akoma Ntoso XML, a `.rac` DSL, a reference compiler, and an "AutoRAC" validation harness with three tiers (CI tests, oracle checks, LLM reviewers). Cosilico and PolicyEngine are listed as downstream consumers. The page is an NSF POSE (Winter 2026) ecosystem map listing assumptions still to test, and target (not confirmed) stakeholders. — [Rules Foundation ecosystem map](https://pose-ecosystem.vercel.app/ecosystem-map-rules-foundation.html)
- Max Ghenis is described as "Builder of PolicyEngine, the Axiom Foundation, and the Thesis Institute"; his draft book "Society in Silico" has a chapter titled "Cosilico: infrastructure for the future". — [Society in Silico](https://societyinsilico.pages.dev/book/cosilico-infrastructure-for-the-future)
- OECD is running a 2026 public consultation "towards a shared reference framework for law as code". — [OECD consultation, July 2026](https://www.oecd.org/en/events/public-consultations/2026/07/consultation-on-the-digital-provision-of-law-towards-a-shared-reference-framework-for-law-as-code.html)
- OECD's 2020 "Cracking the Code" report frames rules as code as rethinking the core government function of rulemaking. — [OECD OPSI, Cracking the Code](https://oecd.org/gov/cracking-the-code-3afe6ba5-en.htm)

### Inferences
Comparison synthesised from the findings above (judgements are mine):

| Engine | Expressiveness / fit | Traceability to statute | Tooling and maturity | Community / activity | Who can maintain |
|---|---|---|---|---|---|
| PolicyEngine (policyengine-us) | Strong for annual household tax and benefit formulas; vectorised; weak for transactions, procedure, interviews | Citations as metadata on parameters/variables; code structure follows forms and variables, not statute sections; explicit source-conflict register | Mature, very high commit velocity, API, TAXSIM emulator | Largest US content base; only one with Colorado rules | Python programmers and policy analysts; lawyers review via PRs |
| OpenFisca (upstream) | Same model | Same | Mature core | International; no US state content | Same |
| Catala | Exceptions and defaults expressed as in statute; scalar, per-case computation | Strongest: literate source interleaved with statute text | Compiler self-described as unstable; LSP, formatter; partly verified | Research team at Inria; 2.4k stars; no Colorado or US state corpus beyond examples | Lawyer plus programmer pairs |
| IRS Fact Graph | Built for incomplete information and interview flows; federal tax facts | Fact definitions, not statute text | Proven in two filing seasons; IRS disclaims maintenance guarantee | Small public community; parent programme suspended | Programmers (Scala/JVM) with tax analysts |
| DMN / Drools | Decision tables; good for eligibility grids, awkward for long arithmetic chains | Weak unless added by convention | Commercial-grade, vendor ecosystem | Large enterprise community, little open tax content | Business analysts (DMN), Java developers (DRL) |
| Blawx | Logic programming with explanations | Good (rule to section mapping) | Self-described as not production quality | Very small | Lawyers in principle |
| Cosilico / RAC | Aims at statute-shaped DSL plus AI-assisted encoding and multi-tier validation | Claimed "every formula traced to statute" | Early: API "coming soon"; no published accuracy figures found | New; tied to PolicyEngine's founder | Unclear; designed for AI agents plus reviewers |

- No engine found is both statute-shaped and has Colorado content. Choosing Catala, the Fact Graph, DMN or RAC means encoding Colorado (and the federal base it depends on) from scratch or bridging to another engine for federal taxable income.
- The Fact Graph's strength (asking only for the facts still needed) matters for a filing or screener product, not for analysis or testing statute encodings.
- The shared personnel between PolicyEngine, the Axiom Foundation register and Cosilico/Rules Foundation suggests PolicyEngine's own leadership sees limits in the OpenFisca-style design and is building a successor format; that is a signal about long-run direction of the upstream, though I found no official statement of a migration plan.

### Gaps
- Naming inconsistency I could not resolve: the policyengine-us README refers to the "Axiom Foundation"; the POSE ecosystem page refers to the "Rules Foundation". Whether these are the same organisation, renamed, or distinct is unconfirmed. Founder and founding date of Cosilico were not stated on the pages read.
- No 2025-2026 source found confirming whether DGFiP runs Mlang in production today, or the current scope of Catala's use inside French administrations.
- Did not verify OpenFisca core's 2026 activity level, licence (UNVERIFIED RECOLLECTION: AGPL-3.0), or how far policyengine-core has diverged from it.
- UNVERIFIED RECOLLECTION: the Fact Graph defines facts in XML "fact dictionary" files with a Scala engine, and Direct File code was released as public-domain (CC0); the licence type did not render on the page I read.
- No evidence found of any US state revenue department using Catala, DMN or the Fact Graph for state income tax in production. Whether any state forked Direct File code after the suspension was not researched.
- Did not research other AI-assisted statute-encoding start-ups beyond Cosilico/RAC and the Policy2Code participants.

## 4. What is known about accuracy and failure modes of rules as code, and how do projects test?

### Takeaway
Documented failures cluster in two places: silent divergence between code and law that only surfaces when someone re-derives the rules independently (French family benefits, Universal Credit), and automation of a legally unsound method or removal of human review (Robodebt, MiDAS). Testing in open projects is mostly model-versus-model or against private official test suites, not against ground-truth returns.

### Cited Findings
- Encoding French family benefits in Catala uncovered a bug in the official implementation. — [arXiv 2103.03198](https://arxiv.org/abs/2103.03198)
- Mlang was validated against DGFiP's private test suite; parts of the official computation ("multiple liquidations") were not published, so outside reproduction required separate test cases and a second DSL. — [MLanguage/mlang](https://github.com/MLanguage/mlang); [arXiv 2011.07966](https://arxiv.org/abs/2011.07966v3)
- UK Universal Credit: CPAG's "You Reap What You Code" (June 2023) reviewed about 2,500 cases, interviewed 13 advisers and 28 claimants, and filed over 50 FOI requests; it argues digital design choices systematically produce unlawful decisions (e.g., not using held carer's allowance data so the carer element is missed; inability to accept advance claims the regulations allow; "claim closure" built into the system without clear legal basis); the UC source code is not public. This is an advocacy organisation's analysis; no DWP response was retrieved. — [CPAG, You reap what you code](https://cpag.org.uk/sites/default/files/2024-01/CPAG-Poverty-175-you-reap-what-you-code-universal-credit-digitalisation-and-the-rule-of-law.pdf)
- Australia Robodebt: the scheme averaged annual tax-office income across 26 fortnights and treated discrepancies as debts, reversing the onus of proof; the Royal Commission called it "amateurish, rushed and disastrous"; counts of people affected vary by source (roughly 433,000 to 443,000). — [The Register on the Royal Commission report](https://www.theregister.com/2023/07/07/robodebt_royal_comission_report_australia/); [ANU, Why Robodebt failed](https://reporter.anu.edu.au/all-stories/why-robodebt-failed)
- Michigan MiDAS: widely reported that 93% of fraud determinations made entirely by computer were false on review of over 22,000 determinations; affected-person counts range from about 20,000 to over 44,000 depending on definition; a 2016 Auditor General report found computer-determined fraud affirmed in only 8% of appealed cases; a 2017 law required human verification. Figures are not reconciled across sources. — [Government Technology](https://govtech.com/data/michigan-integrated-data-automated-system-experiences-93-percent-error-rate-during-nearly-two-years-of-operation.html); [Michigan Public](https://www.michiganpublic.org/post/state-falsely-penalizes-thousands-unemployment-benefits-fraud-now-victims-want-their-money-back)
- PolicyEngine testing/validation: Codecov coverage tracking, TAXSIM cross-validation since 2021 with a $15 tolerance, three-way check with the Atlanta Fed Policy Rules Database, partner API contract tests, and a statute-wins source-conflict register. — [policyengine-taxsim site](https://policyengine.github.io/policyengine-taxsim/); [policyengine-taxsim PyPI](https://pypi.org/project/policyengine-taxsim/); [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- IRS disclaims accuracy of the public Fact Graph code. — [IRS-Public/fact-graph](https://github.com/IRS-Public/fact-graph)

### Inferences
- Robodebt and MiDAS were not failures of a rules-as-code engine; they were failures of policy design, data matching and absent human review. Their lesson for a Colorado project is about deployment governance (burden of proof, appeal, human in the loop), not engine choice. The French and UK cases are the ones about code/law divergence.
- Transparency is the common mitigator: the French bug and the Mlang gaps were found because outsiders could re-implement; CPAG's central complaint is that UC code is closed.
- For Colorado, three independent oracles exist in principle: DOR forms and instructions worked by hand, TAXSIM, and commercial software output. PolicyEngine's reported Colorado gap of about $65 against TaxAct/TAXSIM in one comparison shows the oracles disagree at the tens-of-dollars level, which is outside a $15 tolerance and material for return preparation though not for screening or policy analysis.
- A statute-first rule can make an encoding "correct" in law yet different from what the Department of Revenue's forms and systems actually assess; a project must decide which target it is testing against.

### Gaps
- Did not retrieve primary documents (Robodebt Royal Commission report, Michigan Auditor General reports); numbers above are from secondary reporting and conflict.
- The specific nature of the French family-benefits bug was not retrieved.
- No published error rate for policyengine-us against actual filed Colorado returns was found; I am not aware that one exists.
- Did not find evidence on how Colorado DOR tests its own systems or whether it publishes test cases.

## 5. What role are LLMs playing in translating statutes to code in 2025-2026, and how reliable are they?

### Takeaway
LLMs are now a routine part of encoding workflows (PolicyEngine's repo ships agent instructions; Rules Foundation's validation harness includes LLM reviewers), but the evidence consistently shows they are unreliable when computing or encoding unaided and useful mainly as drafters inside a loop with structured templates, retrieval, executable tests and human review.

### Cited Findings
- Georgetown Beeck Center / Massive Data Institute report (March 2025), four experiments on SNAP and Medicaid policy: overall, LLMs "still require external knowledge and human oversight within an iterative process" for complex logic; "Accuracy and equity considerations must outweigh efficiency in high-stakes benefits systems." — [Digital Government Hub, AI-Powered Rules as Code](https://digitalgovernmenthub.org/publications/ai-powered-rules-as-code-experiments-with-public-benefits-policy/)
- Experiment 1 (chatbots: GPT-4o API, ChatGPT web, Gemini web): completeness scores 56-60%; "Chatbots used confident, authoritative language to convey information, even when inaccurate." — [same report](https://digitalgovernmenthub.org/publications/ai-powered-rules-as-code-experiments-with-public-benefits-policy/)
- Experiment 2 (GPT-4o with RAG over state policy manuals, 228 responses): accuracy 83-100% by state/programme but completeness only about 35-63%; Michigan SNAP had 0% of responses scoring 4 or 5 on completeness. — [same report](https://digitalgovernmenthub.org/publications/ai-powered-rules-as-code-experiments-with-public-benefits-policy/)
- Experiment 3 (machine-readable rules from a JSON template): plain prompting achieved 0% accuracy on income and asset limits in all three states tested; RAG reached 100% in most categories with exceptions; "Missing context in RAG led to erroneous outputs". Recommendations: structured templates/shared schemas, separate rule extraction from code generation, require citations, monitor policy change. — [same report](https://digitalgovernmenthub.org/publications/ai-powered-rules-as-code-experiments-with-public-benefits-policy/)
- Policy2Code challenge finding: directly tasking LLMs with writing policy code produced subpar code. — [Beeck Center announcement](https://beeckcenter.georgetown.edu/the-digital-benefits-network-and-massive-data-institute-experiment-with-ai-to-translate-public-benefits-policies-into-software-code/)
- TaxCalcBench (Bock, Molisee, Ozer, Shah; July 2025): state-of-the-art models correctly compute "less than a third of federal income tax returns" on a simplified set; they "consistently misuse tax tables", make calculation errors and misdetermine eligibility. Federal only. — [arXiv 2507.16126](https://arxiv.org/abs/2507.16126)
- PolicyBench (PolicyEngine's benchmark; provisional figures from a PR description): models alone about 70-75% within 10% of the PolicyEngine reference; with PolicyEngine tools 100%. The reference is PolicyEngine itself, not administrative truth. — [PolicyBench PR mirror](https://gh.r-mj.com/PolicyEngine/policybench/pull/2); [PolicyBench repo mirror](https://tgfed.nhyvvfeijnh.workers.dev/PolicyEngine/policybench)
- PolicyEngine practice: the repo includes `AGENTS.md` and `CLAUDE.md`; Max Ghenis has described (social media, informal) parallel subagents where one writes integration tests, another encodes rules, and checking agents run afterwards. — [PolicyEngine/policyengine-us](https://github.com/PolicyEngine/policyengine-us); [mirror of Max Ghenis Bluesky posts](https://www.bushdrum.com/author/maxghenis-bsky-social)
- Rules Foundation's AutoRAC harness uses three tiers: CI tests, oracle checks, then LLM reviewers. — [Rules Foundation ecosystem map](https://pose-ecosystem.vercel.app/ecosystem-map-rules-foundation.html)

### Inferences
- The benchmarks and the Beeck experiments point the same way: LLM as calculator is unreliable; LLM as drafter of deterministic, tested code is the workable pattern. The 100% "with tools" PolicyBench figure is circular (agreement with the engine that is also the reference) and shows tool use works, not that the engine is right.
- Beeck's experiments used 2024-era models (GPT-4o, Gemini 1.5 Flash); newer models are likely better, but I found no independent 2026 evaluation of statute-to-code accuracy for state tax law, and none for Colorado.
- The Beeck finding that HTML-accessible codes (Oklahoma) ease LLM use is relevant to source preparation for the Colorado Revised Statutes and DOR regulations.
- LLM assistance lowers the cost of encoding, which weakens the "too expensive to build separately" argument, but it raises the importance of an independent test oracle since the same model may write both the rule and its test.

### Gaps
- Experiment 4 (direct code generation) detailed findings were in the unread tail of the report.
- No peer-reviewed 2026 measurement of AI-encoded rules' error rates in PolicyEngine or RAC was found; published claims are informal or from the projects themselves.

## 6. Contributing Colorado rules upstream to PolicyEngine versus building a separate Colorado codebase

### Takeaway
Upstream contribution buys an existing Colorado module, the federal base Colorado law piggybacks on, validation infrastructure and a live community, at the price of AGPL copyleft, design constraints (annual, household-level, formula-per-variable) and dependence on one nonprofit's priorities. A separate codebase is justified mainly for things PolicyEngine's design does not address: transaction-level sales and use tax, procedural or facts-and-circumstances rules, and statute-shaped traceability for legal audiences.

### Cited Findings
- Existing upstream Colorado coverage and AGPL-3.0 licence (see section 1). — [PolicyEngine/policyengine-us](https://github.com/PolicyEngine/policyengine-us)
- Upstream is in architectural transition: population `Microsimulation()` in policyengine-us is deprecated and moving to `policyengine.py`. — [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- Upstream interpretive policy is fixed: statute prevails over regulation, form, instructions, manual or agency practice, with a shared conflict register. — [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- MyFriendBen precedent: consumes PolicyEngine through its API and keeps its own MPL-2.0 rules for other programmes. — [MyFriendBen/benefits-api](https://github.com/MyFriendBen/benefits-api)
- Colorado sales tax structure: Grant Thornton calls Colorado "notorious for having one of the most complex sales and use tax structures in the nation"; home-rule cities self-administer (commonly cited as about 70; a NASCIO summary says 97 home-rule jurisdictions among 272 municipalities); the state built SUTS for single-point filing and a GIS address lookup, but non-participating home-rule cities still require separate filing. Counts conflict across sources and several are vendor blogs. — [Grant Thornton alert](https://www.grantthornton.com/insights/alerts/tax/2021/salt/a-e/co-home-rule-jurisdictions-enact-new-taxes-03-16); [NASCIO award summary](https://www.nascio.org/awards-library/awards/simplifying-colorados-sales-use-tax-filings); [Colorado DOR SUTS final report, 2020](https://Tax.Colorado.Gov/sites/tax/files/Sales_and_Use_Tax_System_%28SUTS%29_Final_Report_07-08-2020.pdf)
- The state contracted Avalara for online sales tax rates and rules (2023). — [CPA Practice Advisor](https://www.cpapracticeadvisor.com/2023/08/09/state-of-colorado-turns-to-avalara-for-online-sales-tax-rates-and-rules/93068/)
- Cosilico positions commercial APIs on top of open encodings, i.e., the ecosystem around PolicyEngine's founder now includes a public-benefit corporation. — [cosilico.ai](https://cosilico.ai)

### Inferences
Arguments for contributing upstream:
- Most of the individual income tax and the headline credits already exist; marginal work is gap-filling (long-tail subtractions, business credits, possibly PTC rebate) rather than greenfield.
- Federal AGI and taxable income, on which Colorado's base depends, come for free and are kept current by others.
- TAXSIM emulator, CI, contract tests and reviewers already exist; Colorado users such as MyFriendBen benefit immediately.
- Avoids a fork that drifts as Colorado law changes annually.

Arguments against, or for a separate codebase:
- Licence: AGPL-3.0 obliges anyone who modifies and offers the software over a network to release source. Acceptable for government and nonprofit open projects; a constraint for proprietary products unless used at arm's length via API (as MyFriendBen does).
- Design fit: the model computes annual amounts for people, tax units and households. Colorado sales and use tax is per transaction, per address, per product category, across state, county, city and special-district layers with home-rule variation; this is a rate-and-taxability lookup problem served by GIS data and commercial engines, not by a household microsimulation. PolicyEngine contains no such model.
- Traceability: code is organised by variable and form line, with citations as metadata. A legal audience wanting section-by-section correspondence would be better served by Catala-style literate encoding, at the cost of rebuilding the federal base or bridging to PolicyEngine for federal taxable income.
- Governance and dependency: priorities, interpretive policy (statute over DOR forms), architecture migrations and release cadence are set upstream; the project is mid-migration and its leadership is simultaneously building a successor format (RAC). A Colorado project targeting "what DOR actually assesses" would conflict with the upstream statute-first rule.
- Review bottleneck: contributions require upstream review; a state-specific team cannot ship on its own schedule without forking.

Middle paths visible in practice:
- Contribute income tax and credits upstream; keep a thin Colorado layer (sales tax, local programmes, interview logic) separately and call PolicyEngine as a library or API (the MyFriendBen pattern).
- Maintain a Colorado test-case corpus (form-based worked examples) independent of any engine, so it can validate upstream code today and a different engine later; this hedges dependency risk regardless of choice.

### Gaps
- No source found that directly evaluates PolicyEngine for sales tax or states that it cannot be used that way; the unsuitability is my inference from the model's design and directory contents.
- Did not read CONTRIBUTING.md, so cannot state CLA requirements, review turnaround, or maintainers' appetite for return-grade detail (e.g., business credits).
- PolicyEngine's funding position and governance (board, bus factor) were not researched.
- Authoritative current counts of Colorado home-rule self-collecting jurisdictions and SUTS participation should be taken from DOR directly.

## 7. Which parts of tax law resist encoding, and how do projects handle them?

### Takeaway
Computational rules (rates, thresholds, phase-outs, credit formulas) encode well; open-textured predicates (residency and domicile, nexus and "doing business", facts-and-circumstances tests) do not, and every project examined handles them by treating the legal conclusion as an input fact supplied by the user or a human decision-maker, not by computing it.

### Cited Findings
- Catala's authors describe their targets as "legal texts that are algorithms in disguise", implicitly limiting scope to the computational parts of statute. — [arXiv 2103.03198](https://arxiv.org/abs/2103.03198)
- The Fact Graph is designed for "reasoning about incomplete information": legal predicates are facts collected from the taxpayer, and the graph infers what remains to be asked. — [Economic Security Project, Chapter 9](https://economicsecurityproject.org/wp-content/uploads/Chapter-9_-Direct-File-fact-graph-and-a-new-way-of-building-civic-technology-products.pdf)
- Direct File restricted eligibility to simple situations (W-2 wages, Social Security, limited interest, specific credits), i.e., it scoped out hard cases instead of encoding them. — [CRS IF13314](https://www.everycrsreport.com/files/2026-09-17_IF13314_7a5be865820f33882647d91cc0cadc376e538af6.html)
- PolicyEngine's Colorado module uses a catch-all `co_other_subtractions` input alongside the few explicitly modelled subtractions, i.e., unmodelled provisions enter as user-supplied amounts. — [GitHub contents API, co subtractions](https://api.github.com/repos/PolicyEngine/policyengine-us/contents/policyengine_us/variables/gov/states/co/tax/income/subtractions)
- PolicyEngine handles conflicts between sources of law by a fixed priority rule (statute wins) plus a public register, not by encoding the ambiguity. — [policyengine-us README](https://raw.githubusercontent.com/PolicyEngine/policyengine-us/main/README.md)
- Beeck: LLMs do better "when prompts are detailed and the policy logic is simple"; scattered and interdependent criteria degrade results. — [Digital Government Hub](https://digitalgovernmenthub.org/publications/ai-powered-rules-as-code-experiments-with-public-benefits-policy/)
- CPAG's Universal Credit analysis shows the failure mode when discretion or legally available options (advance claims) are simply left out of the system: the code's omissions become de facto law. — [CPAG](https://cpag.org.uk/sites/default/files/2024-01/CPAG-Poverty-175-you-reap-what-you-code-universal-credit-digitalisation-and-the-rule-of-law.pdf)
- Colorado sales tax obligations depend on location-specific and home-rule-specific rules that even the state's own lookup tooling handles imperfectly (one source says mapping sites are recommended over the state lookup because of inconsistencies; low-quality source). — [Squarespace-hosted vendor blog](https://clover-whale-gzsr.squarespace.com/blog/what-makes-sales-tax-so-complicated-in-colorado)

### Inferences
- Practical handling patterns seen across projects: (a) boolean input facts for legal conclusions (is a Colorado resident, has nexus); (b) scoping out hard populations; (c) catch-all numeric inputs for unmodelled provisions; (d) a fixed priority rule for conflicting sources; (e) default logic (Catala) for rule/exception structure, which helps with defeasibility but not with vagueness.
- For Colorado specifically, likely hard areas are: full-year/part-year/non-resident status and domicile, apportionment of income for part-year and non-residents, business nexus and "doing business", home-rule sales tax taxability definitions, and any credit conditioned on certification by another agency. These should be modelled as attested inputs with the statutory test documented beside them, not computed.
- An encoding that silently assumes residency (as a household microsimulation of state residents naturally does) is fine for policy analysis but not for a filing or advice tool.

### Gaps
- I did not retrieve Colorado-specific legal sources on residency/domicile rules, part-year apportionment (Form 104PN) or economic nexus thresholds; another researcher may cover them. Nothing here should be read as a statement of those rules.
- Did not verify how policyengine-us treats part-year and non-resident Colorado filers (no directory for it was visible in the listings read).
- No academic source specifically on encoding US state nexus or residency tests was found in this session; the ICAIL/JURIX literature was not searched in depth.
