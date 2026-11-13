# Structure of the Colorado individual income tax (C.R.S. 39-22 and Department of Revenue forms): provision patterns and kinds of quantity

How to read the evidence marks. **[RD]** = read directly, either in a stored copy in this repository (`sources/`, `text/`) or in a document fetched on 2026-11-13 from tax.colorado.gov, leg.colorado.gov or content.leg.colorado.gov. **[SS]** = known only from a search-engine summary; the page itself was not read (colorado.public.law, Justia, FindLaw and similar hosts are not reachable here). No number below is from memory. Statute text was read directly only for: 39-22-104(1.7)(b),(c),(2) and 39-22-123.5 (repository mirror copy, known to be out of date); and, as amended by session laws read on leg.colorado.gov, 39-22-627, 39-22-2003, 39-22-104(3)(p.5)(II), 39-22-119, 39-22-123.5, 39-22-129 and 39-22-130. A session law shows the text as that act left it, not necessarily the text in force today.

Two cautions about the fetched acts. The signed-act PDFs for HB23-1112 and HB24-1134 are scanned images; struck-through words come out garbled in text conversion (for example "2{32-6" where a struck year stood), so only the new capitalised text and unstruck text were relied on. The session-law PDFs (chapters 170 and 293 of 2024) are born-digital, but strike-through is also lost in conversion, so old and new wording run together.

## 1. What is the calculation path on the individual return, form DR 0104, line by line?

### Takeaway
The 2025 return is a 47-line chain: federal taxable income, plus seven named additions, minus one subtraction total carried from the 22-line DR 0104AD, gives Colorado taxable income; tax comes from a table or from the apportioned figure on DR 0104PN; alternative minimum tax and credit recapture are added; nonrefundable credits (capped at the tax) come off; then prepayments and refundable credits are summed, the TABOR sales tax refund is added from a table keyed to a separately computed "modified AGI", and the result is a refund or a balance due with penalty and interest. Line numbers shift from year to year (the TABOR refund is line 33 in 2022, 34 in 2023, 35 in 2024 and 38 in 2025), so a line number is only meaningful together with a form year.

### Cited Findings
All from the 2025 104 Book unless marked. [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf) (stored copy `sources/dor-104-book-2025.txt`)

**DR 0104 (2025), income section**
- Line 1 Federal taxable income, "from your federal income tax form 1040, 1040 SR, or 1040 SP, line 15"; may be negative.
- Line 2 State income tax addback (state income tax deducted on federal Schedule A, plus a partner's or shareholder's share from form DR 0106K).
- Line 3 Qualified business income deduction addback: required if AGI "is greater than $500,000 ($1,000,000 if filing jointly)"; "You must add back the entire deduction regardless of the extent to which your adjusted gross income exceeds the threshold"; not applicable to a taxpayer required to file federal Schedule F; separately required in full for owners of an entity that made a SALT Parity election.
- Line 4 Standard or itemized federal deduction addback: applies when federal AGI "exceeds $300,000"; addback is deductions on Form 1040 line 12e minus $12,000 (single, married filing separately, head of household) or minus $16,000 (joint), reduced by state income tax already added back on line 2.
- Line 5 Business meals deduction addback (full amount from Schedule C line 24b).
- Lines 6 and 7 Non-qualifying distribution addbacks (CollegeInvest tuition savings; Colorado ABLE): recapture of an earlier subtraction unless the withdrawal was for a listed qualifying reason.
- Line 8 Reserved. Line 9 Other additions: non-Colorado state and local bond interest ("not bonds issued by the State of Colorado or its political subdivisions on or after May 1, 1980"), conservation easement deduction also claimed as a credit, unauthorized alien labor expenses, partnership/fiduciary adjustments, expenses at clubs that restrict membership, forfeited employer home-savings contributions.
- Line 10 Subtotal (lines 1 through 7 and 9). Line 11 Subtractions from DR 0104AD line 22. Line 12 Colorado taxable income = line 10 minus line 11.

**DR 0104 (2025), tax and nonrefundable credits**
- Line 13 Colorado tax: "The income tax rate is currently 4.4%. Full-year residents should refer to the tax table in this booklet"; part-year residents and nonresidents take "the apportioned tax amount from the DR 0104PN line 36".
- Line 14 Alternative minimum tax (from DR 0104AMT line 8). Line 15 Recapture of prior year credits (six housing, historic and clean-energy credits are listed as examples). Line 16 Subtotal of 13 to 15.
- Line 17 Nonrefundable credits from DR 0104CR line 65; line 18 nonrefundable enterprise zone credits (DR 1366); line 19 nonrefundable CHIPS zone credit (DR 1370); line 20 strategic capital tax credits (DR 1330). Together they "cannot exceed line 16".
- Line 21 Net income tax = line 16 minus lines 17 to 20; "This cannot be a negative number". Line 22 Repayment of credit (DR 0619). Line 23 Net tax and required repayment.

**DR 0104 (2025), prepayments and refundable credits**
- Line 24 Colorado income tax withheld; 25 prior-year estimated tax carryforward; 26 quarterly estimated payments; 27 extension payment (DR 0158); 28 other prepayments (DR 0104BEP, DR 1079); 29 gross conservation easement credit (DR 1305G); 30 innovative motor vehicle and truck credits (DR 0617); 31 refundable credits from DR 0104CR line 26; 32 additional credit from DR 0619; 33 subtotal of 24 to 32.

**DR 0104 (2025), TABOR refund and settlement**
- Lines 34 to 37 "are only used to calculate your TABOR amount, and do not affect your Colorado tax liability": federal AGI (Form 1040 line 11a) + nontaxable Social Security (line 6a minus 6b) + nontaxable state and local bond interest = "Modified AGI for TABOR Amount".
- Line 38 TABOR state sales tax refund, looked up in a six-tier table by modified AGI and filing status. Eligibility: full-year resident; return "postmarked or transmitted by October 15, 2026"; "18 or older as of January 1, 2025" (or under 18 with a tax liability or a withholding refund claim); not "convicted of a felony and incarcerated ... for 180 days or more during the year".
- Line 39 = 33 + 38; line 40 overpayment; 41 estimated tax carryforward; 42 refund (voluntary contributions are made from the refund on DR 0104CH); 43 net tax due; 44 delinquent payment penalty ("the greater of $5 or 5% of the net tax due for the first month after the due date and increased by 0.5% for each additional month ... The maximum penalty is 12%"); 45 interest; 46 estimated tax penalty (DR 0204); 47 amount you owe.

**DR 0104AD (2025), subtractions, 22 lines**
- 1 state income tax refund; 2 U.S. government interest; 3 Social Security benefits (primary taxpayer); 4 pension and annuity subtraction; 5 and 6 the spouse's versions of 3 and 4; 7 and 8 military retirement subtraction (taxpayer, spouse); 9 Colorado agricultural land capital gain subtraction ("limited to $100,000"); 10 CollegeInvest contribution; 11 Colorado ABLE contribution; 12 qualifying charitable contributions (contributions less a "$500" Colorado adjustment, non-itemizers only); 13 qualified reservation income; 14 PERA/DPSRS subtraction (contributions "between July 1, 1984, and December 31, 1986"); 15 railroad benefit; 16 marijuana and natural medicine business deduction (difference between actual and pro forma federal schedules); 17 reacquisition of Colorado residency during active duty ("on or after January 1, 2016"); 18 employer contribution to home savings account; 19 FAMLI benefits; 20 other subtractions; 21 carryforward subtractions under HB21-1002; 22 subtotal.

**DR 0104CR (2025), credits**
- Part I, refundable, lines 1 to 26: 1 child tax credit (from DR 0104CN line 11, or line 13 for part-year residents); 2 child and dependent care expenses credit (DR 0347; AGI "$60,000 or less"); 3 to 6 Colorado EITC for filers with a Social Security number ("Multiply line 4 by 50% (0.50)"; part-year residents multiply by "the percentage on the DR 0104PN line 34. (If the percentage exceeds 100%, use 100%.)"); 7 business personal property credit; 8 refundable renewable energy credit; 9 Colorado EITC for ITIN filers or certain filers under age 25 (DR 0104TN); 10 early childhood educator credit; 11 owner's share of tax paid with a composite return or SALT Parity election; 12 employee-owned business credits; 13 alternative transportation options; 14 heat pump credit for registered contractors; 15 refundable residential energy storage; 16 certified greenhouse gas avoidance credits; 17 food accessibility; 18 electric lawn equipment (retailers); 19 film incentive; 20 refundable CHIPS zone; 21 Colorado Promise tuition and fee; 22 aircraft modification for unleaded fuel; 23 apprenticeship; 24 disability assistance; 25 qualified care worker; 26 total.
- Part II, lines 27 to 34: credit for tax paid to another state = the smaller of (Colorado tax × other-state modified Colorado AGI ÷ total modified Colorado AGI, rounded to four decimal places) and the tax liability to the other state. Nonresidents do not qualify; part-year residents "generally do not".
- Nonrefundable credits, lines 35 to 63, total on line 65: plastic recycling investment (35), Colorado minimum tax credit (36, "generally equal to 12% of your federal minimum tax credit"), historic property preservation (37, 50 to 52), child care center investment (38, "20% of the qualified investment"), employer child care facility investment (39, "10%"), school-to-career (40), Colorado Works (41), child care contribution (42, "50% of the total qualifying contribution"), long-term care insurance (43, "25% ... cannot exceed $150 per policy"; federal taxable income not over $50,000, or $100,000 joint with two policies), aircraft manufacturer new employee (44), remediation of contaminated land (45), job growth incentive (46), disability funding committee licence fee (47), advanced industry investment (48), CHFA housing credits (49), rural jump-start (53), rural and frontier health care preceptor (54), visitability retrofit (55, "up to $5,000"), employer 529 contributions (56), organ donation leave (57), wildfire mitigation (58, "100% of the costs incurred up to the first $1,000"; not if federal taxable income "is greater than $129,200"), enterprise zone contribution (59, "25% ... limited to $100,000"), nonrefundable residential energy storage (60), homeless contribution (61, 62), employer assistance for home purchase (63, "5%").

**DR 0104PN (2025), apportionment**
- Two parallel columns ("Federal Information", "Colorado Information") for each income and adjustment item. Line 32 modified AGI; line 33 modified Colorado AGI; line 34 "Divide line 33 by line 32. Round to the fourth decimal place, i.e. xxx.xxxx"; line 35 tax from the table on DR 0104 line 12; line 36 "Apportioned tax. Multiply line 35 by the percentage on line 34".
- Residency boxes: full-year nonresident, full-year resident, part-year resident with month and year dates, and "Nonresident 305-day rule Military".

**Other steps stated in the Book**
- Tax table: bands of taxable income ("Over / But not over") mapped to whole-dollar tax; headed "2025 Colorado Income Tax Table with tax rate of 4.4%". The Guide says the tables cover Colorado taxable incomes of less than $50,000 and "approximate" the tax at the prescribed rate. [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)
- Filing status must match the federal return; dependents generally follow IRS Form 1040.
- Estimated tax is expected if next year's liability after credits is "greater than $1,000"; an amended return is due "within 180 days after a federal adjustment is finalized"; records kept "at least 4 years".
- AMT, four steps: federal alternative minimum taxable income less the federal exemption; modified by Colorado additions and subtractions "(except for state income tax addback and the state income tax refund subtraction)"; multiplied "by 3.47%" and apportioned for part-year residents and nonresidents; less the normal Colorado tax. [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide), Part 2

**Year-to-year movement of the same step** [RD] — [2022 Book](https://tax.colorado.gov/sites/tax/files/documents/DR_104_Book_2022.pdf); [2023 Book](https://tax.colorado.gov/sites/tax/files/documents/Book0104_2023.pdf); [2024 Book](https://tax.colorado.gov/sites/tax/files/documents/DR0104_book_2024.pdf); [2025 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)
- TABOR refund line: 33 (2022), 34 (2023), 35 (2024), 38 (2025). Modified AGI for TABOR: line 32 (2022), 33 (2023), 34 (2024), 37 (2025).
- The 2024 Book carried a credit absent from the 2025 schedule: an income-qualified senior housing credit with a lookup table of AGI bands of $500 by three filing-status columns, starting at $800 (single, joint) and $400 (married filing separately) for AGI of "$25,499 or less" and falling by $8, $4 and $4 per band.

### Inferences
- The return is a directed graph of about 150 named line items across DR 0104, 0104AD, 0104CR, 0104PN, 0104CN, 0104TN, 0104AMT and about 20 feeder forms. Each line item is a candidate parameter or rule node, and its identity needs (form, year, line), because numbers are reassigned every year.
- Three different income measures gate provisions and must be kept apart: federal taxable income (tax base; long-term care and wildfire credit limits), federal AGI (most credit limits and phase-outs, deduction addback), and "modified AGI" (two different ones: the TABOR one on DR 0104 and the apportionment one on DR 0104PN).
- The order of operations carries legal content the forms state but a single provision does not: nonrefundable credits are limited to line 16; the TABOR refund "will be applied first against your income tax liability"; the pension subtraction is reduced by the Social Security subtraction on the line above it.

### Gaps
- DR 0104AMT, DR 0104CN, DR 0104TN and DR 0347 are not reproduced in the stored 104 Books; their line-by-line arithmetic was not read. The AMT steps above come from the Guide's prose.
- The line order of DR 0104 for 2022 to 2024 was sampled (rate, EITC, TABOR lines), not transcribed in full.
- The Book does not cite a statute section for most lines; the mapping in section 2 comes from the Guide and the Department's credit index.

## 2. Which sections of C.R.S. 39-22 govern each step, and what is the drafting pattern of each?

### Takeaway
One section (39-22-104) carries the rate and both lists of modifications; apportionment, AMT, each credit, and the TABOR mechanisms each have their own section. The drafting is highly formulaic: a period clause, an eligible-person clause, an allowance verb ("is imposed", "is allowed ... against the taxes due under this article 22"), a number written in words, a base often defined by reference to a federal amount, then separate short subsections for refundability, part-year apportionment, interaction with public benefits, and repeal. Newer credit sections add definitions, a formula, a forecast-driven trigger and an inflation instruction.

### Cited Findings

**Map of steps to sections**
- Residency and definitions: 39-22-103; rule 39-22-103(8)(a). Tax imposed, rate, additions (3), subtractions (4): 39-22-104. AMT: 39-22-105. Temporary rate adjustment: 39-22-627. Returns: 39-22-601. [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide), Parts 1 and 2 "Statutes and regulations"
- Additions also draw on 39-22-504 (net operating losses) and 39-22-529 (unauthorized alien labor); rule 39-22-104(3)(g) (conservation easement addition). Subtractions also draw on 39-22-518 (net capital gains); rules 39-22-104(4), (4)(f) pension and annuity, (4)(m) charitable contribution. Estimated tax: 39-22-605. [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide), Parts 3, 4, 6
- Part-year residents and nonresidents: 39-22-107 (filing status), 39-22-109 (income of a nonresident), 39-22-110 (apportionment for a part-year resident), 39-22-326 (part-year residence), rules 39-22-109 and 39-22-110; Schedule C business income is apportioned under 39-22-303.6. [RD] — [Income Tax Topics: Part-Year Residents & Nonresidents](https://tax.colorado.gov/income-tax-topics-part-year-residents-nonresidents)
- Credits, from the Department's alphabetical index, each entry giving "Applicable tax years", "Maximum carryforward period", "Required forms", "Required documentation", "Statutory citation": child tax credit 39-22-129; family affordability credit 39-22-130; low-income child care expenses credit 39-22-119.5; long-term care insurance 39-22-122; income-qualified senior housing 39-22-544; early childhood educator 39-22-547; qualified care worker 39-22-566; advanced industry investment 39-22-532 and 24-48.5-112; affordable housing 39-22-2101 et seq.; TABOR state sales tax refund 39-22-2003. [RD] — [Income Tax Credits](https://tax.colorado.gov/income-tax-credits)
- Earned income credit: 39-22-123.5; rule 39-22-123.5; 26 U.S.C. 32. [RD] — [Income Tax Topics: Earned Income Tax Credit](https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit) (stored copy `sources/dor-eitc-topics.txt`)
- Child and dependent care expenses credit: 39-22-119 (amended by HB24-1134 section 1; the section number is taken from a search result title and the act's structure, the act's heading line was not legible). [RD for text, SS for section number] — [HB24-1134 signed act](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf)
- Other credit sections named in the 2025 Book: 39-22-114.5 (plastic recycling), 39-22-514 and 514.5 (historic), 39-22-517 (child care investment), 39-22-520, 521, 535, 540, 560; 39-35-104 (aircraft manufacturer). [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)

**39-22-104, rate (pattern: exception + exception + period + imposes + rate in words + base by federal reference + who)**
- "Except as otherwise provided in section 39-22-627, subject to subsection (2) of this section, with respect to taxable years commencing on or after January 1, 2022, a tax of four and forty one-hundredths percent is imposed on the federal taxable income, as determined pursuant to section 63 of the internal revenue code, of every individual, estate, and trust." [RD, unofficial mirror copy] — [C.R.S. 39-22-104 (public.law)](https://colorado.public.law/statutes/crs_39-22-104) (stored `text/crs-39-22-104.xml`)
- Subsection (2) is a pure ordering rule: "Prior to the application of the rate of tax prescribed in subsection (1), (1.5), or (1.7) of this section, the federal taxable income shall be modified as provided in subsections (3) and (4) of this section." [RD, same source]
- Subsection (3) opens "There shall be added to the federal taxable income:" followed by lettered items. Item (p.5)(II) is not a tax rule at all but an appropriation and voter-approval clause: "the general assembly shall annually appropriate an amount at least equal to the amount of revenue generated by the addition ... calculated without regard to any temporary rate reduction pursuant to section 39-22-627"; "constitute a voter-approved revenue change, approved by the voters at the statewide election in November of 2022"; and a condition ending the addition: it "does not apply for an income tax year that commences after the healthy school meals for all program, or any successor program, is repealed. Upon repeal ... the commissioner of education shall promptly notify the executive director in writing". [RD] — [SB24-228, 2024 Session Laws ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)
- Section heading as amended by Amendment 87: "Income tax imposed on individuals, estates, and trusts - report - tax preference performance statement - legislative declaration - definitions - repeal". [RD] — [Amendment 87 text](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure)

**39-22-627, temporary rate adjustment (pattern: fiscal-year period + condition on certified excess revenue + actor + delta to the rate, in tiers + annual adjustment of the tier amounts + override conditions + deadline)**
- "if, for any state fiscal year commencing on or after July 1, 2024, but before July 1, 2034, the amount of state revenues in excess of the limitation on state fiscal year spending imposed by section 20 (7)(a) of article X of the state constitution that are required to be refunded ... exceeds the amount specified in subsection (1)(b) of this section, the executive director shall temporarily reduce the state income tax rate for the income tax year commencing during the calendar year in which the state fiscal year ended". [RD] — [SB24-228, ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)
- Seven tiers, each "If the amount of such excess state revenues is greater than [A] but less than or equal to [B], the income tax rate is reduced by [N] one-hundredths of one percent": over $300 million to $500 million, 0.04; over $500 million to $600 million, 0.07; over $600 million to $700 million, 0.09; over $700 million to $800 million, 0.11; over $800 million to $1 billion, 0.12; over $1 billion to $1.5 billion, 0.13; over $1.5 billion, 0.15 (all written in words in the act). [RD, same source]
- Indexing of the tier amounts: "the executive director shall annually adjust the excess state revenue amounts ... by a percentage equal to the percentage of allowable increase in state fiscal year spending calculated pursuant to section 24-77-103 (2)(a)(I)". [RD, same source]
- Override: "if the permanent state income tax rate then in effect is four and twenty-five one-hundredths percent or less ... any otherwise applicable temporary income tax rate reduction ... does not take effect; except that, if the amount of excess state revenues ... is equal to or greater than two billion dollars, the executive director shall temporarily reduce the state income tax rate to the extent necessary to refund all excess state revenues". [RD, same source]
- One-year fixed reduction: "For the income tax year beginning on January 1, 2024, the executive director shall temporarily reduce the state income tax rate from four and forty one-hundredths percent ... to four and twenty-five one-hundredths percent ... as a method to refund excess state revenues ... for state fiscal year 2023-24." [RD, same source]
- Deadline and certification: "no later than October 1, 2024, and no later than each October 1 thereafter of any calendar year during which it is certified in accordance with the provisions of section 24-77-106.5 ... the executive director shall estimate the amount by which state revenues would be decreased". [RD, same source]
- A Department rule for this section says the rate was reduced to four and one-half percent for tax years commencing in 2019 and 2021. [SS] — [search result for Rule 39-22-627](https://colorado.public.law/statutes/crs_39-22-627)

**39-22-123.5, earned income credit (pattern: period + who + "is allowed ... against the taxes due under this article 22" + "equal to [percent] of the federal credit" + base; variants by counterfactual federal eligibility; then refund, apportionment, benefits, repeal)**
- Three parallel families of subsection, identical except for the base: (2) "the federal credit that the resident individual claimed on his or her federal tax return for the same tax year"; (2.5) "the federal credit that the resident individual would have been allowed, but for the fact that the resident individual, the resident individual's spouse, or one or more of the resident individual's dependents do not have a social security number that is valid for employment"; (2.7) "would have been allowed under section 32 (n)(1) of the internal revenue code, notwithstanding the date limitation set forth in section 32 (n) ... as specified in section 9621 (a) of the 'American Rescue Plan Act of 2021', Pub.L. 117-2". [RD, mirror copy] — [C.R.S. 39-22-123.5 (public.law)](https://colorado.public.law/statutes/crs_39-22-123.5) (stored `text/crs-39-22-123.5.xml`)
- "(4) The amount of the credit allowed under this section that exceeds the resident individual's income taxes due is refunded to the individual." "(5) In the case of a part-year resident, the credit allowed under this section is apportioned in the ratio determined under section 39-22-110 (1)." "(6) The credit allowed under this section is not considered to be income or resources for the purpose of determining eligibility for the payment of public assistance benefits". [RD, same source]
- As amended in 2024, the percentage moves into a year list: "Except as otherwise provided in subsection (3.5) of this section, the credit amount that can be claimed ... is: (A) for the income tax year commencing on January 1, 2024, fifty percent ...; (B) for the income tax year commencing on January 1, 2025, thirty-five percent ...; and (C) for income tax years commencing on or after January 1, 2026, twenty-five percent". [RD] — [HB24-1134 signed act](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf)
- Trigger, new (3.5): "For the income tax year commencing on January 1, 2025, the percentage of the federal earned income tax credit ... is increased by fifteen percentage points if the estimated adjustment factor is equal to or greater than two percent." For 2026 on, five tiers: factor at least 3 but under 3.18 percent, plus 5 points; 3.18 to under 3.37, plus 10; 3.37 to under 3.56, plus 15; 3.56 to under 3.75, plus 20; 3.75 or more, plus 25 (all in words). [RD, same source]

**39-22-129, child tax credit (pattern: definition by federal reference + period + filing-status variant + fixed dollar amount "for each eligible child" by AGI band + explicit denial above the top band + inflation instruction + repeal of the superseded subsections)**
- Definition switched by period: "'Eligible child' means for income tax years commencing on or after January 1, 2024, a qualifying child, as defined in section 152 (c) of the internal revenue code, who is under six years of age at the end of the taxable year for which the credit is claimed." [RD] — [HB23-1112 signed act](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf)
- "(4.5) (a) (I) For income tax years commencing on or after January 1, 2024, a resident individual who files a single return is allowed a child tax credit against the income taxes due under this article 22 for each eligible child of the taxpayer in the following amounts: (A) one thousand two hundred dollars if the individual's federal adjusted gross income is twenty-five thousand dollars or less; (B) six hundred dollars if ... greater than twenty-five thousand dollars but less than or equal to fifty thousand dollars; and (C) two hundred dollars if ... greater than fifty thousand dollars but less than or equal to seventy-five thousand dollars." Joint filers: the same amounts at $35,000, $60,000 and $85,000. [RD, same source]
- Denial: "A resident individual who files a single return and whose federal adjusted gross income is greater than seventy-five thousand dollars is not allowed a credit under this section." [RD, same source]
- Earlier form (2022 and 2023) was a percentage of a federal credit with a counterfactual base: "could have claimed a federal child tax credit ... had section 24 (h)(7) of the internal revenue code not applied to the definition of qualifying child"; and a federal-law contingency: "if the changes specified in section 9611 of the 'American Rescue Plan Act of 2021', Pub.L. 117-2, are no longer applicable to the federal child tax credit ... then the amount of the child tax credit allowed in this section is as follows". [RD, same source]
- Legislative intent sentence inside the section: "it is the intent of the general assembly to establish a permanent and refundable state child tax credit for eligible Colorado taxpayers". [RD, same source]

**39-22-130, family affordability credit (pattern: declaration + performance statement + definitions + formula + base amount + age tiers + AGI phase-out by step + trigger tiers that change both the amount and the phase-out rate + inflation instructions + apportionment + refund + monthly payment authority + repeal)**
- Allowance: "In addition to the child tax credit allowed by section 39-22-129, for income tax years commencing on or after January 1, 2024, but before January 1, 2034, a resident individual who files a single return is allowed a family affordability tax credit against the income taxes due under this article 22 for: (I) each eligible child ... who is five years of age or younger at the close of the income tax year in the amount of three thousand two hundred dollars, adjusted for inflation and as modified by subsections (4), (5), and (6) of this section; and (II) each eligible child ... who is six years of age or older but less than seventeen years of age at the close of the income tax year in an amount that is seventy-five percent of the amount allowed in subsection (3)(a)(I)". [RD] — [HB24-1311, 2024 Session Laws ch. 293](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_293.pdf)
- Phase-out: the credit amounts "are reduced, but not below zero, by an amount equal to six and eight hundred seventy-five one-thousandths percent for each five thousand dollars by which a resident individual's adjusted gross income exceeds fifteen thousand dollars" (joint: "twenty-five thousand dollars"). [RD, same source]
- Trigger for 2025: "if the estimated adjustment factor is: (a) greater than or equal to two percent" the full schedule applies; "(b) less than two percent, no credit is allowed pursuant to this section." [RD, same source]
- Trigger for 2026 to 2033, six outcomes keyed to the factor: at least 3.75 percent, full amount and 6.875 percent step; 3.56 to under 3.75, step 9.06 percent; 3.37 to under 3.56, step 13.59 percent; 3.18 to under 3.37, amount "reduced to two thousand six hundred dollars, adjusted for inflation" and step 19.23 percent; 3 to under 3.18, amount "reduced to one thousand six hundred fifty dollars, adjusted for inflation" and step 30.30 percent; under 3 percent, "no credit is allowed" (all in words). [RD, same source]
- Formula in the statute: "'Estimated adjustment factor' means, for a given income tax year, the CAGR for nonexempt revenue that is calculated according to the following formula", printed as CAGR = ((EV/BV)^(1/n) − 1) × 100, with defined terms "applicable forecast", "applicable state fiscal year", "BV", "CAGR", "EV", "N", "nonexempt revenue", "TABOR". [RD, same source; the formula's layout is damaged in text conversion and was reconstructed from the surrounding definitions]
- Adjustment to the factor: it "must be increased by one-tenth of one percentage point if the Colorado unemployment rate, as calculated by the United States bureau of labor statistics, reaches five percent and must be increased by an additional one-tenth of one percentage point for every one percentage point increase in the Colorado unemployment rate above five percent". [RD, same source]
- Actor: "The executive director shall calculate the estimated adjustment factor in accordance with this section." [RD, same source]
- Administrative authority: "The department of revenue is authorized and encouraged to develop a means of refunding the credits ... in twelve equal monthly refunds rather than annually." Repeal: "This section is repealed, effective December 31, 2037." [RD, same source]

**39-22-119, child and dependent care expenses credit (pattern: AGI band + percentage of a federal credit; later an AGI ceiling with an inflation instruction)**
- 1996 to 2018 form: "If the resident individual's federal adjusted gross income is twenty-five thousand dollars or less, the credit shall be in an amount equal to fifty percent of the credit for child care expenses claimed on the resident individual's federal tax return"; thirty percent "between twenty-five thousand one dollars and thirty-five thousand dollars"; ten percent "between thirty-five thousand one dollars and sixty thousand dollars"; none at "sixty thousand one dollars or more". [RD] — [HB24-1134 signed act](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf)
- 2026 on: "if a resident individual's federal adjusted gross income is less than or equal to sixty thousand dollars, then the individual is allowed a child and dependent care expenses credit ... equal to seventy percent of the federal credit allowed pursuant to section 21 of the internal revenue code and calculated without regard to the limitation imposed by section 26 of the internal revenue code." [RD, same source]
- Refund without carryforward: the credit "is not carried forward and must be refunded to the individual". Anti-duplication: not allowed to a person "receiving child care assistance from the department of early childhood except to the extent of the taxpayer's unreimbursed out-of-pocket expenses". [RD, same source]

**39-22-2003, TABOR state sales tax refund (pattern: definition with exclusions + condition on excess revenue + amount as a share of an aggregate divided by an estimated head count, by AGI band)**
- "'Qualified individual' does not include: (I) Any natural person who was convicted of a felony and who served a sentence of incarceration ... for a total of one hundred eighty days or more during the fiscal year ending during the taxable year". [RD] — [SB24-228, ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)
- "If the qualified individual's adjusted gross income for the tax year is less than or equal to twenty-five thousand dollars, the refund is an amount equal to the amount of excess state revenues required to be refunded ..., multiplied by twenty-five percent, divided by the estimated number of said qualified individuals expected to claim the credit for that taxable year"; further bands use 23, 19, 12, 6 and 15 percent at $50,000, $75,000, $100,000, $125,000 and above. Joint filers get "double the amount ... for such aggregate income amount". Below an "identical refund threshold" every qualified individual gets the same amount. [RD, same source]

**39-22-110 and 39-22-109, apportionment and nonresident income**
- 39-22-110 apportions the tax under 39-22-104 "in the ratio" of federal AGI relating to the period of Colorado residency (numerator) to total federal AGI (denominator), both as modified under 39-22-104. [SS] — [C.R.S. 39-22-110 (public.law)](https://colorado.public.law/statutes/crs_39-22-110)
- 39-22-109(1) defines "Colorado nonresident federal adjusted gross income" as the part of federal AGI, determined under section 62 of the Internal Revenue Code, derived from Colorado sources. [SS] — [C.R.S. 39-22-109 (public.law)](https://colorado.public.law/statutes/crs_39-22-109)
- The Department's description: tax is "initially calculated in the same manner as Colorado income tax for full-year residents and then apportioned"; some federal adjustments are prorated by Colorado wage and self-employment income over the federal totals, others by total Colorado income over total income. Wages are Colorado-source "if the employee was physically present in Colorado when performing the work". [RD] — [Income Tax Topics: Part-Year Residents & Nonresidents](https://tax.colorado.gov/income-tax-topics-part-year-residents-nonresidents)
- A day-count fraction also exists: for a part-year resident's net operating loss, the remainder is allocated by "the number of days during the tax year that the taxpayer was a Colorado resident" over "the total number of days in the tax year". [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide), Part 3

**39-22-103, definitions**
- Residency test as the Department states it: domiciled in Colorado, or "maintains a permanent place of abode in Colorado and spends, in aggregate, more than six months of the tax year in Colorado". [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide), Part 1
- 39-22-103 defines "internal revenue code" by reference to the federal code of 1986 as it may become effective at any time, and gives undefined terms their federal meaning. [SS] — [C.R.S. 39-22-103 (public.law)](https://colorado.public.law/statutes/crs_39-22-103)

**39-22-105, alternative minimum tax**
- Search summaries disagree on the statutory rate: one copy (2024 compilation) shows 3.75 percent in (1)(a) and 3.47 percent in (1.5); another shows 3.47 percent in (1)(a). The Department's Guide uses 3.47 percent. [SS for statute] — [C.R.S. 39-22-105 (public.law)](https://colorado.public.law/statutes/crs_39-22-105); contradicted by [Counsel Stack copy](https://law.counselstack.com/statute/co/39/39-22-105); [RD for 3.47%] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)

### Inferences
- A credit section decomposes into the same slots almost every time: period; filing-status variant; eligible person; qualifying unit (child, policy, beneficiary, aircraft); amount (percent of a federal amount, percent of an expense, fixed dollars, or an amount on an agency certificate); income gate; phase-out; cap; refundability or carryforward; part-year apportionment; interaction with other benefits; inflation instruction; trigger; repeal. A span dictionary organised around those slots would cover the family credits read here.
- The rate itself now has three layers that must be modelled separately: the permanent rate (39-22-104), a temporary reduction computed from certified excess revenue (39-22-627), and, if Amendment 87 takes effect, a bracket schedule with a carve-out rate for one kind of gain.
- Statute sections contain much text that sets no taxpayer-facing number: declarations, performance statements, appropriation clauses, reporting duties, authority to design payment methods. A dictionary needs a way to mark these as non-operative rather than leave them unlabelled.

### Gaps
- The current official text of 39-22-103, -104(3) and (4), -105, -108, -109, -110 was not read. Everything about them here is from Department publications or search summaries. In particular the lettered lists in 39-22-104(3) and (4) were not seen, so their drafting patterns (other than (p.5)(II)) are inferred from the forms.
- 39-22-108 (the brief names it for residency) was not found in any source read; the Department cites 39-22-103, -107, -109, -110 and -326 for residency and apportionment.
- The act that set the 2023 EITC percentage at 50 percent (the Department's table) was not read; the mirror statute copy says 25 percent for 2023.
- Whether later acts (2025 and 2026 sessions) changed 39-22-627, -129 or -130 was not checked. A search summary mentions a 2025 bill (SB25-138) and a 2025-2026 initiative touching 39-22-627; their fate is unknown.

## 3. How do Colorado statutes express time, numbers, repeals, triggers, inflation adjustments and declarations? The distinct drafting formulas

### Takeaway
There are about a dozen recurring formulas, and several have more than one surface form for the same meaning (four ways to say "tax years from"; three ways to write a percentage). Numbers in statute are always spelled out in words; the same numbers appear as digits in agency material and in appropriation clauses. The newest formulas (forecast triggers, per-step phase-outs, conditional inflation rounding) pack three or four linked numbers into one sentence.

### Cited Findings
Sources: [39-22-104 mirror](https://colorado.public.law/statutes/crs_39-22-104) and [39-22-123.5 mirror](https://colorado.public.law/statutes/crs_39-22-123.5) (stored in `text/`); [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf); [HB24-1134](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf); [HB24-1311 ch. 293](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_293.pdf); [SB24-228 ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf); [Amendment 87 text](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure). All [RD].

**A. Tax-year periods**
- Closed range: "For income tax years commencing on or after January 1, 2022, but before January 1, 2023" (123.5).
- Open-ended start: "with respect to taxable years commencing on or after January 1, 2022" (104); "For income tax years beginning on and after January 1, 2026" (HB24-1134, child care credit).
- Open-ended end: "For an income tax year commencing prior to January 1, 2022" (123.5); "for income tax years commencing before January 1, 2024" (HB23-1112).
- Single year: "For the income tax year commencing on January 1, 2024" (123.5); "For the income tax year beginning on January 1, 2024" (SB24-228).
- Disjoint union in one sentence: "For income tax years commencing on or after January 1, 2023, but before January 1, 2024, and for the income tax year commencing on January 1, 2025" (123.5).
- "In any income tax year commencing on or after ..., but before ..., if ..." introducing a contingency (HB23-1112).
- Vocabulary varies with no change of meaning: "taxable years" / "income tax years"; "commencing" / "beginning"; "on or after" / "on and after"; "prior to" / "before".

**B. Other periods and dates**
- State fiscal years: "for any state fiscal year commencing on or after July 1, 2024, but before July 1, 2034"; "For the 2023-24 state fiscal year and state fiscal years thereafter"; "state fiscal year 2024-25" (SB24-228, HB24-1311).
- Mapping one period to another: "the income tax year commencing during the calendar year in which the state fiscal year ended" (SB24-228); "the fiscal year that begins in the income tax year for which the credit is allowed" (HB24-1311); "during the fiscal year ending during the taxable year" (39-22-2003).
- Deadlines for an official: "no later than October 1, 2024, and no later than each October 1 thereafter" (SB24-228).
- Point-in-time tests on a person: "at the close of the income tax year", "at the end of the taxable year for which the credit is claimed" (HB24-1311, HB23-1112).
- Before-and-after definitions tied to a date: "'BV' means, on or before December 31, 2024, the estimate of ... and after December 31, 2024, the amount of ..." (HB24-1311).
- Event dates that are not tax years (agency wording): bonds "issued ... on or after May 1, 1980"; contributions "between July 1, 1984, and December 31, 1986"; investments placed in service "after January 1, 2015, but before January 1, 2021". [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)

**C. Numbers**
- Rate as mixed number of hundredths: "four and forty one-hundredths percent"; "four and fifty-five one-hundredths percent"; unhyphenated variant in the measure: "FOUR AND FORTY ONE-HUNDREDTHS PERCENT", "TWENTY FIVE THOUSAND DOLLARS".
- Rate as mixed number of thousandths: "six and eight hundred seventy-five one-thousandths percent".
- Rate as a simple fraction: "four and one-half percent" (old text in SB24-228); "four and three-quarters percent" (corporate text in HB24-1134).
- Whole percentages: "twenty-five percent", "thirty-eight percent", "seventy percent".
- Change in a rate, in hundredths of a point: "reduced by four one-hundredths of one percent".
- Change in a percentage, in points: "increased by fifteen percentage points"; "increased by one-tenth of one percentage point".
- Replacement of one rate by another: "from four and forty one-hundredths percent ... to four and twenty-five one-hundredths percent".
- Reference to an unstated number: "from ... its current percentage of the federal taxable income".
- Dollar amounts in words: "one thousand two hundred dollars", "three thousand two hundred dollars", "one billion five hundred million dollars"; off-by-one band edges in older text: "between twenty-five thousand one dollars and thirty-five thousand dollars".
- Digits appear only in appropriation clauses and declarations: "$178,494 is appropriated"; "1.2 FTE"; "those making over $850,000 per year"; "46 percent of early childhood workers".
- Counts and durations in words: "one hundred eighty days or more"; "twelve equal monthly refunds"; "ninety-day period".
- Ages in words with a comparator: "five years of age or younger"; "six years of age or older but less than seventeen years of age"; "under six years of age".

**D. Comparators and bands**
- "less than or equal to", "greater than ... but less than or equal to", "greater than or equal to ... but less than", "or less", "not more than", "exceeds", "equal to or greater than", "reaches".
- Marginal-bracket wording: "ON THE AMOUNT UP TO AND INCLUDING TWENTY FIVE THOUSAND DOLLARS"; "ON THE AMOUNT GREATER THAN ... BUT LESS THAN OR EQUAL TO ..."; with drift inside one provision ("ON THE AMOUNT OVER FIVE HUNDRED THOUSAND DOLLARS"). Each item restates every lower bracket.
- Cliff wording: addback of "the entire deduction regardless of the extent to which your adjusted gross income exceeds the threshold" (agency paraphrase). [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)

**E. Allowance, denial and base**
- Imposition: "a tax of ... is imposed on ..."; "A GRADUATED TAX IS IMPOSED ON ... AS FOLLOWS:".
- Credit: "is allowed a[n] ... credit against the taxes due under this article 22 that is equal to ..."; "for each eligible child ... in the following amounts:".
- Denial: "is not allowed a credit under this section"; "no credit is allowed pursuant to this section"; "shall not be allowed".
- Modification: "There shall be added to the federal taxable income:".
- Base by federal reference: "as determined pursuant to section 63 of the internal revenue code"; "as defined in section 152 (c) of the internal revenue code".
- Counterfactual base: "would have been allowed, but for the fact that ..."; "could have claimed ... had section 24 (h)(7) of the internal revenue code not applied"; "calculated without regard to the limitation imposed by section 26 of the internal revenue code"; "notwithstanding the date limitation set forth in section 32 (n)".
- Same-year tie: "for the same tax year".
- Derived amount: "an amount that is seventy-five percent of the amount allowed in subsection (3)(a)(I) of this section".
- Special rate for one kind of income: "SHALL BE SUBJECT TO TAX UNDER THIS SECTION AT THE RATE OF ...".

**F. Limits, floors and phase-outs**
- Floor: "reduced, but not below zero".
- Per-step phase-out: "by an amount equal to [rate] for each five thousand dollars by which ... adjusted gross income exceeds fifteen thousand dollars".
- Cap wording in agency text: "cannot exceed $150 per policy"; "limited to $100,000"; "whichever is smaller"; "the greater of $5 or 5%"; "up to the first $1,000 of costs". [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)
- Appropriation bounds: "an amount at least equal to ..., but not more than the amount required".

**G. Exceptions and cross-references**
- "Except as otherwise provided in section 39-22-627"; "subject to subsection (2) of this section"; "Except as provided in subsection (4) of this section"; "Except as otherwise provided in subsection (3.5) of this section"; "as modified by subsections (4), (5), and (6) of this section"; "; except that ..."; "In addition to the child tax credit allowed by section 39-22-129"; "notwithstanding any other limits in the state constitution or law".
- Self-reference style: "this subsection (2)(c)", "this article 22", "this title 39".

**H. Triggers and contingencies**
- Forecast trigger: "if the estimated adjustment factor is: (a) greater than or equal to two percent: ... or (b) less than two percent, no credit is allowed".
- Certified-revenue trigger: "if ... the amount of state revenues in excess of the limitation ... exceeds the amount specified in subsection (1)(b)".
- Level trigger on the rate itself: "if the permanent state income tax rate then in effect is four and twenty-five one-hundredths percent or less".
- External statistic: "if the Colorado unemployment rate, as calculated by the United States bureau of labor statistics, reaches five percent".
- Federal-law contingency: "if the changes specified in section 9611 of the 'American Rescue Plan Act of 2021' ... are no longer applicable".
- Program-repeal contingency with notice: "does not apply for an income tax year that commences after the ... program ... is repealed ... the commissioner of education shall promptly notify the executive director in writing".
- Contingent effect of the act: "Sections 1 and 12 of this act take effect only if Senate Bill 24-111 does not become law"; referendum petition clause "at 12:01 a.m. on the day following the expiration of the ninety-day period after final adjournment".

**I. Delegation to an official**
- "the executive director shall temporarily reduce"; "shall annually adjust"; "shall calculate the estimated adjustment factor"; "shall estimate the amount"; "the department of revenue shall adjust"; "is authorized and encouraged to develop".

**J. Inflation adjustment**
- "the department of revenue shall adjust the federal adjusted gross income amounts set forth in this section to reflect inflation for each income tax year in which the credit described in this section is allowed if cumulative inflation since the last adjustment, when applied to the current limits, results in an increase of at least one thousand dollars when the adjusted limits are rounded to the nearest one thousand dollars" (39-22-129(8), 39-22-130(7); same wording for the child care credit AGI limit from 2027).
- Index definition: "'Inflation' means the annual percentage change in the United States department of labor bureau of labor statistics consumer price index for Denver-Aurora-Lakewood for all items paid by all urban consumers, or its applicable successor index."
- Inline form on an amount: "three thousand two hundred dollars, adjusted for inflation".
- Indexing to something other than prices: thresholds adjusted "by a percentage equal to the percentage of allowable increase in state fiscal year spending calculated pursuant to section 24-77-103 (2)(a)(I)".
- Absence is also a fact: the Blue Book notes the Amendment 87 brackets "are not adjusted for inflation". [RD] — [2026 Blue Book, Amendment 87](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/blue-book)

**K. Repeal clauses**
- Of a paragraph: "This subsection (2)(c) is repealed, effective December 31, 2034."
- Of several subsections including the clause itself: "Subsections (3), (3.5), and (4) of this section and this subsection (9) are repealed, effective December 31, 2026."
- Of a section: "This section is repealed, effective December 31, 2037."
- Repealed placeholders survive in the numbering: (2.5)(c) and (3) of 123.5 are marked repealed in the stored copy.
- The repeal date trails the last tax year covered by years: the 2024-only 38 percent paragraph is repealed at the end of 2034; the family affordability credit covers years before 2034 and is repealed at the end of 2037.

**L. Definitions**
- "As used in this section, unless the context otherwise requires:" then "'X' means ...". Variants: "has the same meaning as set forth in section 39-22-2002 (3)"; "'Qualified individual' does not include: ..."; a definition that changes by period ("means for income tax years commencing before January 1, 2024, ..."); a definition by federal reference with a carve-out ("as defined in section 152 (c) ...; except that the age requirements are as set forth in ...").

**M. Declarations and performance statements**
- "The general assembly hereby finds and declares that:" followed by findings containing statistics ("Eighty-three percent of Colorado parents worry ...").
- Tax preference performance statement: "In accordance with section 39-21-304 (1), which requires each bill that creates a new tax expenditure to include a tax preference performance statement ..., the purposes of the tax expenditure ... are to ..." and a measurement duty: "The general assembly and the state auditor ... shall measure the effectiveness ... by determining the number of Colorado families who ... no longer fall below the federal poverty level".
- Initiative form: "The people of the state of Colorado find, determine, and declare that:".

**N. Amendment markup**
- New text is in capitals, deleted text struck through: "Capital letters or bold & italic numbers indicate new material added to existing law; dashes through words or numbers indicate deletions from existing law and such material is not part of the act." Amending clause: "In Colorado Revised Statutes, 39-22-104, amend (1.7)(c) and (2); and add (1.8) as follows:".
- Section headings are a dash-separated list of topics: "Earned income tax credit - not a refund of excess state revenues - trigger - legislative declaration - repeal".

### Inferences
- A normaliser for periods must handle at least: closed range, open start, open end, single year, union of ranges, fiscal-year ranges, and a rule that maps a fiscal year to a tax year. The repository's parser already covers the first five.
- A normaliser for numbers must distinguish a level ("four and forty one-hundredths percent") from a change to a level ("reduced by four one-hundredths of one percent", "increased by fifteen percentage points") from a replacement ("from ... to ..."). Reading "four one-hundredths of one percent" as 0.04 percent rather than 4 percent depends on the trailing "of one percent".
- Some numbers in a provision are not parameters of the tax (statistics in declarations, appropriations, head counts). They need a class of their own or an explicit "not a parameter" mark, or an extractor will mis-file them as values.

### Gaps
- Formulas were collected from six texts. Sections not read (39-22-104(3) and (4), 39-22-105, 39-22-108 to -110, the subtraction provisions for pensions and Social Security) may hold further formulas, in particular for age-based caps and for apportionment ratios in statutory words.
- No example was found of an inflation adjustment applied to the rate brackets, and none of a statutory rounding rule for the tax itself.

## 4. What parameter-like values do the Department's publications give by tax year?

### Takeaway
The Department publishes most parameters as small year-indexed tables or as dollar figures inside line instructions. Several published values differ from the stored statute copy (EITC 2023 to 2025) or exist only by agency computation (TABOR refund amounts, inflation-adjusted AGI limits), so the publication is sometimes the only place a usable number appears.

### Cited Findings

**Income tax rate by tax year** [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide) (stored `sources/dor-individual-income-tax-guide.txt`)

| Tax year | Rate |
|---|---|
| 2019 | 4.5% |
| 2020 | 4.55% |
| 2021 | 4.5% |
| 2022 | 4.4% |
| 2023 | 4.4% |
| 2024 | 4.25% |
| 2025 | 4.4% |

- The 104 Books agree: tax table headings "with tax rate of 4.4%" (2022, 2023, 2025) and "4.25%" (2024). [RD] — [2024 Book](https://tax.colorado.gov/sites/tax/files/documents/DR0104_book_2024.pdf); [2025 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)
- AMT rate: 3.47% of Colorado alternative minimum taxable income. [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)

**Colorado EITC as a percentage of the federal credit** [RD] — [Income Tax Topics: Earned Income Tax Credit](https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit)

| Tax year(s) | Percentage |
|---|---|
| 2017-2021 | 10% |
| 2022 | 20% |
| 2023 | 50% |
| 2024 | 50% |
| 2025 | 50% |
| 2026 and later | 25% |

- The return forms agree: "multiply line 4 by 20% (0.20)" (2022), "50% (0.50)" (2023, 2024, 2025). [RD] — 104 Books 2022 to 2025
- The stored statute copy says 25 percent for 2023, 38 percent for 2024 and 25 percent for 2025. HB24-1134 explains 2024 (fifty percent) and 2025 (thirty-five percent plus fifteen points if the adjustment factor is at least two percent) and 2026 (twenty-five percent plus trigger points). [RD] — [39-22-123.5 mirror](https://colorado.public.law/statutes/crs_39-22-123.5); [HB24-1134](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf)
- Under-25 eligibility ages: 24 if a specified student; 19 to 24 otherwise; 18 to 24 if a qualified former foster youth or homeless youth. [RD] — [EITC topics page](https://tax.colorado.gov/income-tax-topics-earned-income-tax-credit)
- "The credit was 50% of the federal EITC amount for Tax Years 2024 and 2025, but will be reduced to 25% in Tax Year 2026." [RD] — [CTC and EITC page](https://tax.colorado.gov/CTC-EITC)

**Child tax credit** [RD] — [Income Tax Topics: Child Tax Credit](https://tax.colorado.gov/income-tax-topics-child-tax-credit)

AGI limits:

| Tax year | Single filers | Joint filers |
|---|---|---|
| 2022 | $75,000 | $85,000 |
| 2023 | $75,000 | $85,000 |
| 2024 | $75,000 | $85,000 |
| 2025 | $77,000 | $87,000 |

Credit per eligible child (under age 6), tax year 2025:

| Single filers, AGI | Credit | Joint filers, AGI | Credit |
|---|---|---|---|
| $26,000 or less | $1,200 | $36,000 or less | $1,200 |
| $26,001 to $51,000 | $600 | $36,001 to $61,000 | $600 |
| $51,001 to $77,000 | $200 | $61,001 to $87,000 | $200 |

- Statutory amounts for 2024 (before inflation adjustment): the same credit amounts at $25,000 / $50,000 / $75,000 (single) and $35,000 / $60,000 / $85,000 (joint). [RD] — [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf)
- For 2022 and 2023 the credit "is based on the federal child tax credit a taxpayer claimed or could have claimed"; percentages by income band are on form DR 0104CN, which was not read. "Any taxpayer whose federal filing status is single, head of household, or married filing separately is considered a single filer for the purpose of the credit." Part-year residents: "the percentage on line 34 of their Colorado Form 104PN or 100%, whichever is less". [RD] — [CTC topic](https://tax.colorado.gov/income-tax-topics-child-tax-credit)

**Family affordability credit**
- "Applicable tax years: 2024 and 2025; and 2027 through 2033, subject to availability"; eligible child under 17; "Availability of the credit for tax years 2025 and later depends on the applicable revenue forecast." [RD] — [Income Tax Credits](https://tax.colorado.gov/income-tax-credits)
- "The State must temporarily pause the Family Affordability Tax Credit for tax year 2026 (filed in 2027). The tax credit is turned off in years where revenue projections fall below a threshold growth rate". [RD] — [CTC and EITC page](https://tax.colorado.gov/CTC-EITC)
- Statutory base: $3,200 per child aged 5 or younger, 75 percent of that for ages 6 to 16, phase-out 6.875 percent per $5,000 of AGI over $15,000 (single) or $25,000 (joint). [RD] — [HB24-1311](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_293.pdf)
- By adjustment factor (2026 to 2033): "3.75% and up", maximum credit $3,200 and "50% of federal EITC"; "3.56% to 3.75%", maximum $3,200 with "phaseout accelerated by 32%" and "45% of federal EITC"; below 3.00 percent the credits are not available. [RD] — [LCS memorandum, 13 January 2026](https://content.leg.colorado.gov/sites/default/files/r26-27-treatment-of-tax-credit-triggers-in-fiscal-notes-accessible.pdf)

**Pension and annuity subtraction, by age at 31 December** [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf); [Income Tax Topics: Social Security, Pensions and Annuities](https://tax.colorado.gov/income-tax-topics-social-security-pensions-and-annuities)

| Age at end of tax year | Limit |
|---|---|
| 65 or older | $24,000 minus the Social Security subtraction, or taxable pension income if smaller |
| 55 to 64 | $20,000 minus the Social Security subtraction, or taxable pension income if smaller |
| Under 55 | $20,000, only for income received as a death benefit |

- Computed separately for each spouse; unused room cannot be shared.
- Premature IRA distributions are excluded ("has not yet reached age 59½").

**Social Security subtraction** [RD] — same two sources
- Age 65 or older: the entire amount included in federal taxable income ("For income tax years beginning January 1, 2022, and after").
- Age 55 to 64: the entire amount if AGI does not exceed $75,000 (single) or $95,000 (joint) ("For income tax years beginning January 1, 2025, and after"); otherwise "the cap remains at $20,000".
- Under 55: only benefits received due to the death of the person entitled; limited to $20,000.
- Joint returns split taxable benefits "in a ratio of the gross Social Security benefits of each taxpayer to the total gross Social Security benefits of both taxpayers".

**Military retirement subtraction (under age 55)** [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)

| Tax year | Limit |
|---|---|
| 2019 | $4,500 |
| 2020 | $7,500 |
| 2021 | $10,000 |
| 2022-2028 | $15,000 |

**Federal deduction addback** [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)

| Tax years | AGI above which it applies | Limit, single | Limit, joint | Applies to |
|---|---|---|---|---|
| 2022 | $400,000 | $30,000 | $60,000 | itemized deductions only |
| 2023-2025 | $300,000 | $12,000 | $16,000 | itemized or standard deduction |
| 2026 and later | $300,000 | $1,000 | $2,000 | itemized or standard deduction |

**Other addition and subtraction values** [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide); [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)
- QBI deduction addback: AGI over $500,000 (single) or $1,000,000 (joint), tax years 2021 and later; SALT Parity owners from 2018.
- Overtime deduction addback: "For tax years 2026 and later", full amount; no addback for qualified tips.
- Business meals addback: "For tax years 2024 through 2030"; food and beverage addback for 2022 only, the amount above 50 percent of the expense.
- ABLE contribution subtraction: "tax years 2023 through 2030"; home savings account subtraction: "tax years 2024 through 2026".
- CollegeInvest and ABLE per-beneficiary limit, 2025: "Single Filers: $25,400, Joint Filers: $38,100".
- Charitable contribution subtraction: amount "in excess of $500"; receipts required "for claims greater than $5,000".
- Agricultural land capital gain subtraction: limited to $100,000.
- Olympic medal subtraction: AGI not over "$1 million ($500,000 if married filing separately)".
- Unauthorized alien labor addback not required if the worker "was paid less than $600" or "was hired ... prior to December 31, 2006".

**TABOR state sales tax refund amounts** [RD] — 104 Books [2022](https://tax.colorado.gov/sites/tax/files/documents/DR_104_Book_2022.pdf), [2023](https://tax.colorado.gov/sites/tax/files/documents/Book0104_2023.pdf), [2024](https://tax.colorado.gov/sites/tax/files/documents/DR0104_book_2024.pdf), [2025](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)

| Tax year | Tier 1 | Tier 2 | Tier 3 | Tier 4 | Tier 5 | Tier 6 |
|---|---|---|---|---|---|---|
| 2022 upper bound of modified AGI | $48,000 | $95,000 | $151,000 | $209,000 | $268,000 | above |
| 2022 single / joint | $153 / $306 | $208 / $416 | $234 / $468 | $285 / $570 | $300 / $600 | $486 / $972 |
| 2023 | flat: "$800 for one qualifying taxpayer or $1,600 for two qualifying taxpayers filing jointly" | | | | | |
| 2024 upper bound | $53,000 | $105,000 | $166,000 | $233,000 | $302,000 | above |
| 2024 single / joint | $177 / $354 | $240 / $480 | $277 / $554 | $323 / $646 | $350 / $700 | $565 / $1,130 |
| 2025 upper bound | $52,000 | $105,000 | $168,000 | $233,000 | $299,000 | above |
| 2025 single / joint | $19 / $38 | $25 / $50 | $29 / $58 | $35 / $70 | $37 / $74 | $59 / $118 |

- Refund mechanisms used by state fiscal year: FY2024 property tax reimbursement, income tax rate reduction and sales tax refund; FY2023 property tax reimbursement and sales tax refund; FY2022 those two plus Colorado Cash Back (Senate Bill 22-233); FY2021 property tax reimbursement, rate reduction and sales tax refund. [RD] — [TABOR Sales Tax Refund page](https://tax.colorado.gov/TABOR)

**Credit values stated in the 2025 Book and the credit index** [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf); [Income Tax Credits](https://tax.colorado.gov/income-tax-credits)
- Disability assistance credit, by federal AGI. Single: up to $10,000, $1,200; $10,001 to $12,500, $1,000; $12,501 to $15,000, $800; $15,001 to $17,500, $600; $17,501 to $20,000, $400. Joint: up to $16,000, $1,200; $16,001 to $20,000, $1,000; $20,001 to $24,000, $800; $24,001 to $28,000, $600; $28,001 to $32,000, $400.
- Child and dependent care expenses credit: AGI $60,000 or less. Low-income child care expenses credit: AGI $25,000 or less, 25% of expenses, at most $500 for one dependent or $1,000 for two or more, child under 13, tax years 2014 to 2025.
- Early childhood educator credit: AGI not over $75,000 (single) or $150,000 (joint); "a fixed amount that increased annually for inflation based on the credential level"; 2022 through 2025.
- Qualified care worker credit: $1,200; AGI not over $75,000 (single) or $100,000 (joint); 2025 through 2028.
- Colorado Promise tuition credit: family income of $90,000 or less. Aircraft modification credit: 50% of expenses, at most $500 per aircraft. Business personal property credit: tax on up to $18,000 of actual value; assessment rates 26.4% and 27.9%.
- Wildfire mitigation credit: "nonrefundable for tax years 2023 through 2026 and refundable for tax years 2027 and later".
- Index totals: 37 entries begin "A refundable" and 44 "A nonrefundable"; carryforward periods given as five years (19 entries), three years (8), none (6), and also seven, eight, ten, 11 and 20 years, "No limit", and "Up to tax year 2033"; applicable years mostly "YYYY through YYYY" (63 entries) or "YYYY and later" (18).

**Payment, penalty and interest values** [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)
- Estimated tax: required if liability less withholding and credits exceeds $1,000; four payments each 25% of the required annual payment, which is the lesser of 70% of current-year liability or 100% of the preceding year's (110% if preceding-year AGI was more than $150,000, or $75,000 if married filing separately); farmers and fishermen (at least 2/3 of gross income) 50%, one payment.
- Interest rates by calendar year, discounted / regular: 2022 3% / 6%; 2023 5% / 8%; 2024 8% / 11%; 2025 9% / 12%; 2026 8% / 11%.
- Late payment penalty: the greater of five dollars or 5%, plus 0.5% per month, not over 12%; waived if 90% was paid by the original due date.
- Due dates: April 15; automatic six-month extension to file; estimated payments April 15, June 15, September 15, January 15; June 15 for persons abroad.

### Inferences
- Publication tables are keyed by tax year, and often by filing status and by an income or age band as well. A parameter store needs those three or four keys, plus a note on which key values the agency collapses ("single" includes head of household and married filing separately for the child tax credit, but the senior housing table had a separate married-filing-separately column).
- For inflation-indexed limits, statute gives a base-year number and a rule, and only the Department publishes the result ($77,000 and $87,000 for 2025 against $75,000 and $85,000 in the act). Such a parameter has two sources of different kinds, both correct.
- The Department's "applicable tax years" and "maximum carryforward period" fields are a ready-made list of two quantities the present span classes have no place for.

### Gaps
- Child tax credit percentages by income band for 2022 and 2023 are on form DR 0104CN, which is not in the stored copies and was not fetched.
- The Department's topic page for the family affordability credit exists (a search result gives its address) but two guessed addresses returned 404 and it was not read; the inflation-adjusted amounts and AGI limits it publishes for 2024 and 2025 are therefore missing.
- CollegeInvest and ABLE limits for years other than 2025, and the early childhood educator credit amounts by credential level, were not collected.
- The 2026 values (EITC 25%, deduction limits $1,000 and $2,000, interest 8% / 11%) are announced in publications; no 2026 104 Book exists in the stored copies.

## 5. Which values depend on something outside the statute?

### Takeaway
Very few Colorado numbers stand alone. The base and many credits are functions of federal amounts; the rate for a given year, the TABOR refund and four credits depend on certified or forecast state revenue; several limits depend on a price index applied by the Department; many business credits are whatever amount another agency certifies; and the rate structure from 2027 depends on a ballot measure whose result is reported but not yet certified.

### Cited Findings

**Federal amounts and federal definitions**
- The tax base is "the federal taxable income, as determined pursuant to section 63 of the internal revenue code". [RD] — [39-22-104 mirror](https://colorado.public.law/statutes/crs_39-22-104)
- Credits computed from a federal credit: EITC (IRC 32), child and dependent care (IRC 21), Colorado minimum tax credit ("12% of your federal minimum tax credit"), and the 2022 to 2023 child tax credit (IRC 24). [RD] — [HB24-1134](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf); [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf); [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf)
- Federal definitions imported: qualifying child (IRC 152(c)), AGI (IRC 62), filing status, dependents; AMT starts from federal alternative minimum taxable income and "the applicable federal exemption (please see IRS Form 6251 for the exemption amount)". [RD] — [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)
- Colorado amounts that are federal amounts by another route: nontaxable Social Security (Form 1040 line 6a minus 6b) in the TABOR modified AGI; deductions disallowed by IRC 280E; the IRC 199A deduction; the excess over the IRC 121 exclusion in Amendment 87. [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf); [Amendment 87 text](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure)
- Dependence on a federal law staying in force: the 2022 to 2023 child tax credit switched amounts "if the changes specified in section 9611 of the 'American Rescue Plan Act of 2021' ... are no longer applicable". [RD] — [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf)
- A federal change after filing changes the Colorado result: an amended return is due "within 180 days after a federal adjustment is finalized". [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf)

**State revenue, certified after the fact (TABOR)**
- Temporary rate reduction: depends on excess state revenues "as determined by the annual certification of excess state revenues required by section 24-77-106.5", net of property tax exemption reimbursements, with the executive director estimating the revenue effect by October 1. The 2024 rate of 4.25% came from this section. [RD] — [SB24-228 ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)
- TABOR sales tax refund: each tier's amount is a statutory share of the excess revenue "divided by the estimated number of said qualified individuals expected to claim the credit"; the published dollar amounts fell from $177 to $565 (2024) to $19 to $59 (2025). [RD] — [SB24-228 ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf); 104 Books 2024 and 2025
- The tier thresholds of 39-22-627 are themselves adjusted each year by the allowable growth in state fiscal year spending under 24-77-103(2)(a)(I). [RD] — same act

**State revenue, forecast in advance**
- Family affordability credit and the expanded EITC: the "estimated adjustment factor" is a compound annual growth rate of nonexempt (TABOR) revenue from a December forecast "prepared by legislative council staff or ... the office of state planning and budgeting ... as determined by which immediately preceding March forecast the joint budget committee ... used in the preparation of the state budget", nudged upward by the Colorado unemployment rate "as calculated by the United States bureau of labor statistics". [RD] — [HB24-1311 ch. 293](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_293.pdf)
- "There are four tax credits in current law, known as triggered tax credits, whose availability or amounts are dependent on state revenue conditions": the family affordability credit, the expanded EITC, the decarbonization credits (HB23-1272; halved when a June forecast expects TABOR revenue growth under 4 percent) and the workforce shortage credit (HB24-1365; maximum halved on a September forecast under 4 percent). [RD] — [LCS memorandum, 13 January 2026](https://content.leg.colorado.gov/sites/default/files/r26-27-treatment-of-tax-credit-triggers-in-fiscal-notes-accessible.pdf)
- Timing rule: "the availability and amount of the FATC and the expanded EITC for tax year 2027 will depend on the adjustment factor for FY 2027-28 ... calculated using the December 2026 forecast". [RD] — same memorandum
- Outcome for tax year 2026: EITC 25% and the family affordability credit paused. [RD] — [CTC and EITC page](https://tax.colorado.gov/CTC-EITC)
- A June 2026 news report said revenue would likely not rise enough to trigger the family affordability credit for the next two years. [SS] — [KUNC, 22 June 2026](https://www.kunc.org/news/2026-06-22/affordability-tax-credit-likely-not-available-for-colorado-families-in-next-two-years)

**Price index applied by the Department**
- AGI limits for the child tax credit, the family affordability credit and (from 2027) the child care credit, and the family affordability credit amount, follow the Denver-Aurora-Lakewood consumer price index, adjusted only when cumulative inflation moves a limit by at least $1,000 after rounding. Published result: child tax credit limits of $77,000 and $87,000 for 2025. [RD] — [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf); [CTC topic](https://tax.colorado.gov/income-tax-topics-child-tax-credit)

**Determinations by other agencies**
- Credit amounts fixed by a certificate: OEDIT (advanced industry, job growth incentive, employee ownership, film, rural jump-start, CHIPS), Colorado Energy Office (greenhouse gas avoidance credits, heat pump), CHFA (housing credits "in an amount determined by the Colorado Housing and Finance Authority"), Department of Agriculture, CDPHE (remediation), Division of Housing (visitability, homeless contribution), Apprenticeship Colorado, institutions of higher education (Colorado Promise). [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf); [Income Tax Credits](https://tax.colorado.gov/income-tax-credits)
- County assessor values and assessment rates feed the business personal property credit. Interest rates are set per calendar year. [RD] — [2025 104 Book](https://tax.colorado.gov/sites/tax/files/documents/Book104_2025.pdf); [Individual Income Tax Guide](https://tax.colorado.gov/individual-income-tax-guide)
- Whether an addition applies can depend on another program's existence: the (p.5) deduction addback ends when the healthy school meals program is repealed and the commissioner of education notifies the executive director. [RD] — [SB24-228 ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)

**Ballot measures**
- Amendment 87 (2026): amends article X, section 20(8)(a) of the constitution (striking the single-rate requirement), limits 39-22-104(1.7)(c) to years "BUT BEFORE JANUARY 1, 2027", and adds a six-bracket schedule in (1.8) with rates of 3.7, 4.2, 4.4, 7.4, 7.9 and 8.4 percent at $25,000, $100,000, $500,000, $750,000 and $1,000,000 (in words in the measure; digits in the Blue Book's Table 1). [RD] — [Amendment 87 text](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure); [2026 Blue Book](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/blue-book)
- Interaction with a rival measure: "If both Amendment 87 and Proposition 136 are approved by voters ... the exact outcome is unclear. The state legislature or a court will need to determine how to resolve any conflicts." [RD] — [2026 Blue Book](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/blue-book)
- Result as reported: news outlets reported between 6 and 9 November 2026 that Amendment 87 passed and Proposition 136 failed; the early count was close (one report: 50.49% to 49.51%); no certified Secretary of State totals were found. [SS] — [Colorado Politics, 6 November 2026](https://www.coloradopolitics.com/2026/11/06/colorado-passes-graduated-income-tax-eliminates-flat-rate/); [HPPR, 9 November 2026](https://www.hppr.org/hppr-news/2026-11-09/colorado-voters-approve-amendment-87-imposing-higher-income-taxes-on-top-earners)
- Proposition 121 (2022): lowered the individual and corporate rate from 4.55 percent to 4.40 percent for tax year 2022 and later; approved. [SS] — [Legislative Council packet for Proposition 121](https://content.leg.colorado.gov/sites/default/files/initiative%2520referendum_proposition%20121%20final%20lc%20packet.pdf); [Ballotpedia](https://ballotpedia.org/Colorado_State_Income_Tax_Rate_Reduction_Initiative_(2022))
- Proposition FF (2022): the deduction addback of 39-22-104(3)(p.5) is described in statute as "a voter-approved revenue change, approved by the voters at the statewide election in November of 2022". [RD] — [SB24-228 ch. 170](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)
- Constitutional constraint on all of the above: "Neither an income tax rate increase nor a new state definition of taxable income shall apply before the next tax year." [RD] — [Amendment 87 text](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure), quoting article X, section 20(8)(a)

### Inferences
- External dependencies fall into five kinds with different timing: (1) a federal figure known when the return is prepared; (2) a state figure certified after the fiscal year ends but before returns are filed (excess revenue); (3) a forecast made in the December before the tax year; (4) an index value applied once a year by the Department; (5) a legal event (election, repeal of a program, a companion bill becoming law). A parameter record needs a field saying which kind it is and who publishes the resolved value.
- For kinds 2 to 4 the statute never contains the operative number. The engine's rule "leave unknown values unrecorded" would therefore apply by default to every future year of the EITC percentage, the family affordability credit, the TABOR refund and any temporary rate.

### Gaps
- No certified result for Amendment 87 or Proposition 136 was found; treat the outcome as reported, not official.
- The Proposition 121 Blue Book and the Proposition FF text were not read directly.
- The controller's certification figures and the forecasts that produced the 2024 rate cut and the 2025 and 2026 trigger outcomes were not retrieved.

## 6. Which patterns in the wider law do the seven span classes (period, value, base, who, exception, effect, threshold) not cover?

### Takeaway
The seven classes fit a provision of the form "for years P, a rate V applies to base B of persons W, subject to exception E". They do not have a place for at least eighteen things that recur across the credit, TABOR and apportionment provisions: the main ones are repeal dates, non-income triggers, changes to a value as opposed to a value, caps and floors, per-step phase-outs, ages, per-unit multipliers, filing-status variants, definitions, formulas, inflation rules, the acting official, apportionment ratios, carryforward and recapture, and non-operative text.

### Cited Findings

**What the classes are and how they are used now** [RD] — `extractions/extractions.json` and `extractions/config.json` in this repository (no public URL; the provisions marked are from [39-22-104 mirror](https://colorado.public.law/statutes/crs_39-22-104), [39-22-123.5 mirror](https://colorado.public.law/statutes/crs_39-22-123.5) and the [Amendment 87 text](https://leg.colorado.gov/ballots/graduated-income-tax-2/files/text-of-measure))
- Definitions: period "The tax years the provision covers"; value "The number the provision sets"; base "What the number is applied to"; who "Who the provision applies to"; exception "A cross-reference that can displace the provision"; effect "A consequence other than a number"; threshold "An income amount where a rate starts or stops".
- Eleven provision groups are marked. `value` holds only percentages so far. `threshold` appears only in the Amendment 87 bracket list. `effect` appears once ("is refunded to the individual"). `base` is also used for an ordering rule ("the federal taxable income shall be modified as provided in subsections (3) and (4) of this section") and for a conditional amount ("The amount of the credit allowed under this section that exceeds the resident individual's income taxes due").
- Not marked although ingested: the repeal clauses ("This subsection (2)(c) is repealed, effective December 31, 2034"), the part-year apportionment subsection (5), the public-benefits subsection (6), and the (2.5) and (2.7) variants.

**Patterns with no class, each with a provision that shows it** (quotations are from the acts cited in sections 2 and 3, all [RD]: [HB24-1311](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_293.pdf), [SB24-228](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf), [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf), [HB24-1134](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf), and the Department sources in section 4)

1. **Repeal or sunset date of the text.** "This section is repealed, effective December 31, 2037." A date that bounds the provision's existence, not the tax years it covers; it usually falls years after the last covered tax year.
2. **Trigger on a quantity that is not the taxpayer's income.** "if the estimated adjustment factor is ... greater than or equal to two percent"; "if the amount of such excess state revenues is greater than three hundred million dollars". `threshold` is defined as an income amount; these are growth rates and aggregate state dollars, with their own comparators.
3. **Change to a value, as opposed to a value.** "the income tax rate is reduced by four one-hundredths of one percent"; "increased by fifteen percentage points"; "from four and forty one-hundredths percent ... to four and twenty-five one-hundredths percent". Needs a way to say delta, direction, unit (percentage points) and replacement.
4. **Fixed dollar amounts as the thing set.** "one thousand two hundred dollars"; "three thousand two hundred dollars". Could go in `value`, but `value` then needs a unit (rate, share of a federal amount, dollars) because the validator parses each differently.
5. **Caps, floors and min/max rules.** "reduced, but not below zero"; "cannot exceed $150 per policy"; "whichever is smaller"; "the greater of $5 or 5%"; "an amount at least equal to ..., but not more than ...".
6. **Phase-out by steps.** "six and eight hundred seventy-five one-thousandths percent for each five thousand dollars by which ... adjusted gross income exceeds fifteen thousand dollars": a reduction rate, a step size and a start point bound together. Marking them as one value and two thresholds loses the relation.
7. **Income gate on eligibility (as opposed to a bracket edge).** "whose federal adjusted gross income is greater than seventy-five thousand dollars is not allowed a credit"; "adjusted gross income is less than or equal to sixty thousand dollars". Also which income measure is meant (federal taxable income, federal AGI, modified AGI).
8. **Age and other personal attributes with a measurement date.** "five years of age or younger at the close of the income tax year"; "under six years of age at the end of the taxable year"; ages 55 and 65 "on December 31, 2025"; "18 or older as of January 1, 2025".
9. **Per-unit multiplier.** "for each eligible child"; "per policy"; per beneficiary; "for each qualifying aircraft".
10. **Filing-status variant.** "a resident individual who files a single return" against "two resident individuals who file a joint return", each with its own numbers. It can be forced into `who`, but it is a key that selects among parallel values, and the Department's tables use it as a column.
11. **Definitions.** "'Eligible child' means ..."; "'Inflation' means ..."; "'Qualified individual' does not include ..."; "has the same meaning as set forth in section 39-22-2002 (3)". Term, definiens, federal reference and carve-out are all unclassed.
12. **Formulas and their variables.** The CAGR formula with "BV", "EV", "N"; "multiplied by twenty-five percent, divided by the estimated number of said qualified individuals".
13. **Inflation or other indexing rule.** Actor, quantity adjusted, index, first year, rounding ("rounded to the nearest one thousand dollars") and a materiality test ("results in an increase of at least one thousand dollars"). Also "adjusted for inflation" as a two-word modifier on an amount.
14. **Actor and duty.** "the executive director shall temporarily reduce"; "shall calculate"; "the department of revenue shall adjust"; amounts set by another agency's certificate. Who resolves the number is not a `who` in the present sense (the taxpayer).
15. **Apportionment ratio.** "apportioned in the ratio determined under section 39-22-110 (1)"; the forms' numerator and denominator; the cap "If the percentage exceeds 100%, use 100%"; the day-count fraction for net operating losses; the benefit-share ratio between spouses.
16. **Refundability, carryforward, recapture, transfer.** "is not carried forward and must be refunded"; "carried forward up to five years but must be applied first to the earliest year possible"; "subject to recapture"; credits "duly transferred"; "nonrefundable for tax years 2023 through 2026 and refundable for tax years 2027 and later". `effect` can hold the words but not the count of years or the change by period.
17. **Stacking, ordering and anti-duplication.** "In addition to the child tax credit allowed by section 39-22-129"; "Prior to the application of the rate"; pension limit "minus any amount entered on line 3"; "Multiple subtractions may not be claimed for the same income"; no credit "except to the extent of the taxpayer's unreimbursed out-of-pocket expenses".
18. **Counterfactual or adjusted federal base.** "would have been allowed, but for the fact that ..."; "calculated without regard to the limitation imposed by section 26"; "notwithstanding the date limitation". Markable as `base`, but the override inside it is a separate fact the engine must act on.
19. **Non-tax-year periods.** State fiscal years; the rule mapping a fiscal year to a tax year; official deadlines ("no later than October 1"); event dates ("issued on or after May 1, 1980"); durations ("one hundred eighty days or more", "more than six months", 305 days).
20. **Contingency on a legal event.** Federal-law change; repeal of another program with written notice; "take effect only if Senate Bill 24-111 does not become law"; voter approval; referendum petition clause.
21. **Operation type.** Whether the provision imposes, adds, subtracts, credits, exempts, apportions, refunds or penalises. At present this is implicit in which parameter the group is attached to.
22. **Non-operative text.** Legislative declarations, tax preference performance statements, appropriation clauses, reporting and audit duties, authority to pay monthly. These contain numbers ("Eighty-three percent", "$178,494") that are not parameters.
23. **Amendment status of words.** New (capitals) against deleted (struck) text in an act; a `status` exists on provisions in `text/*.xml` but not on spans.

**Evidence that the gaps matter for the two sections already ingested**
- The heading of 39-22-123.5 as amended is "Earned income tax credit - not a refund of excess state revenues - trigger - legislative declaration - repeal", and the trigger now sits in (3.5); the stored copy's note says "no trigger provision appears in this snapshot's text". Marking the current section needs classes 1, 2, 3, 12 and 14 above. [RD] — [HB23-1112](https://leg.colorado.gov/sites/default/files/2023a_1112_signed.pdf) (heading); [HB24-1134](https://leg.colorado.gov/sites/default/files/2024a_1134_signed.pdf) (trigger); `text/crs-39-22-123.5.xml`
- 39-22-104's opening exception points to 39-22-627, whose content is entirely of kinds 2, 3, 13, 14 and 19. [RD] — [SB24-228](https://leg.colorado.gov/sites/default/files/documents/2024A/bills/sl/2024a_sl_170.pdf)

### Inferences
- Three of the seven classes are overloaded rather than wrong. `value` needs a unit and a role (level, delta, replacement, share, dollars); `threshold` needs the quantity it tests (taxpayer income measure, age, state revenue, growth rate) and a comparator; `effect` is carrying refundability, apportionment and benefit-disregard rules that each recur with their own numbers.
- A smaller core set with attributes may serve better than twenty flat classes: a number span (with unit and role), a condition span (with tested quantity and comparator), a time span (with kind: tax year, fiscal year, repeal date, deadline, event date, duration), a party span (taxpayer, official, agency), a reference span (internal, federal, other state law), a definition span, and an operation span. This is a design suggestion, not a finding.
- The bracket provision of Amendment 87 and the family affordability phase-out show that relations between spans (this rate applies between these two thresholds; this reduction rate goes with this step and this start) carry the meaning. The present `derive: schedule` note handles one such relation by position; the phase-out and trigger tiers need the same treatment.

### Gaps
- The list is drawn from the provisions read. Statutory wording for the pension, Social Security, capital gain and nonresident-source rules was seen only through Department paraphrase, so further uncovered patterns there (for example, a subtraction limited by another subtraction, in statutory words) are likely but unconfirmed.
- No count was made of how often each uncovered pattern occurs across Article 22; frequency would be needed to decide which classes earn a place.
- Corporate, fiduciary and pass-through provisions were out of scope and were not examined, though the same sections (39-22-627, the credit sections) apply to them.
