# Colorado tax parameters and sales tax jurisdiction data as open, machine-readable data (state of play, November 2026)

Research date: 11 November 2026. Older figures are dated inline. Where a number comes from a search-result summary rather than a page I read in full, it is marked "(snippet)".

## 1. How is Colorado sales and use tax structured? Jurisdiction counts, self-collecting home-rule cities, base differences

### Takeaway
Colorado runs two parallel sales tax systems: a state-administered one (state 2.9% plus counties, statutory cities and special districts, which may still deviate from the state base on a fixed list of exemptions) and roughly 66 to 74 self-collecting home-rule municipalities that write, administer and audit their own tax codes. Overlaps produce 400+ unique taxing areas, and counts differ by source and by what is being counted.

### Cited Findings
- As of October 2025, the Department of Revenue (DOR) "collects, administers, and enforces the sales taxes of 52 counties, 166 cities, and 33 special districts. Another 66 home rule municipalities collect their own sales and use taxes pursuant to their local ordinances." The overlap "yields over 400 unique taxing areas", and DOR processes more than 48 million returns per year. — [CDOR SUTS Functionality Study, Oct 2025 (hosted by MTC)](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- DOR makes monthly distributions to more than 250 jurisdictions totalling $2.8 billion (the study does not state the period for the $2.8 billion). — [CDOR SUTS Functionality Study, Oct 2025](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- A different DOR figure: SUTS "covers 600 taxing entities" (DOR announcement, 25 Sept 2026). — [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause)
- Older count (Tax Foundation, published Apr 2019, updated July 2023): 271 municipalities, nearly 100 with home-rule charters; 72 home-rule cities and towns plus 2 counties self-administer (74 self-collecting jurisdictions); about 68% of Colorado's population lives in self-administered home-rule municipalities. — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/)
- 2020 snapshot: 96 home-rule jurisdictions, 72 of which independently administer their own sales and use tax (snippet). — [Holland & Hart, JSTA Spring 2020](https://www.HollAndHart.com/webfiles/JSTA_Colorado_Sales_and_Use_Tax_Changes_Kozik_Nelson_Spring2020.pdf)
- History of the base split: counties and statutory cities shared the state base until 1979, when the General Assembly created exemptions (food for home consumption, residential energy, manufacturing machinery) that apply locally only if the local ordinance or resolution expressly adopts them. Eleven further types of special district have gained sales tax powers since 1997. — [CDOR SUTS Functionality Study, Oct 2025](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Up to 15 goods are exempt from state sales tax but can be taxed by state-administered local jurisdictions (groceries, residential energy, machinery, farm equipment, pesticides among them). — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/)
- Home-rule charters give localities authority over rates, bases, licences, fees, audits and collection procedures, with little state limitation; Denver was the first home-rule city to impose a sales tax (1948), Pueblo followed in 1956. — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/); [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Local use taxes are narrower than sales taxes for state-administered jurisdictions: limited to building materials (collected locally, mostly via building permits) and motor vehicles (collected with county clerks at titling). — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- State rate 2.9%; combined rates range from 2.9% to about 11.2% (third-party figure, snippet). — [TaxCloud Colorado guide](https://taxcloud.com/sales-tax/colorado/)
- Home-rule cities differ on newer categories such as software-as-a-service, which is taxed differently by city (vendor blog, snippet). — [Zamp](https://zamp.com/blog/colorado-taxes-saas-differently-by-city)
- The retail delivery fee is a further per-transaction parameter: $0.31 per delivery as of 1 July 2026 (third-party figure, snippet). — [USgeocoder blog](https://blog.usgeocoder.com/2026-colorado-sales-tax-rate-changes/)

### Inferences
- "How many jurisdictions" has no single answer: 251 state-collected entities plus 66 self-collectors is about 317 taxing entities (Oct 2025 study), versus "600 taxing entities" in DOR's Sept 2026 release and "400+ unique taxing areas" for rate combinations. An open dataset would have to define its unit (taxing entity, location code, or rate area) explicitly.
- The self-collector count appears to have fallen from 72 to 74 (2019 to 2020 sources) to 66 (2025), consistent with some cities handing collection to the state, but the sources count slightly different things (the Tax Foundation figure includes 2 counties).
- A rates-only dataset is insufficient for Colorado. Correct tax requires three layers: boundaries (address to jurisdictions), rates, and per-jurisdiction taxability (the 15 optional state exemptions plus each home-rule code).

### Gaps
- No official 2026 count of special districts by type or of total location codes was retrieved (the DR 0800 2026 PDF exists but was not parsed).
- No quantified, sourced comparison of how each home-rule base differs from the state base beyond the examples above.

## 2. What is SUTS? Vendor, coverage, GIS lookup, API, terms, hold-harmless, bulk data

### Takeaway
SUTS is a state-run, vendor-built pair of tools: a GIS-based Colorado Sales Tax Lookup (rates, jurisdictions, rate history, a 350+ item taxability matrix, an API and a bulk lookup) and a single filing portal run by GovOS that now reaches all but two self-collecting home-rule cities. It carries a statutory-style hold-harmless for sellers, but it is a lookup service, not an open dataset, and the free bulk lookup was paused on 29 September 2026 after usage ran at nearly double its funded volume.

### Cited Findings
- SUTS "has two components that are managed by different vendors": the Colorado Sales Tax Lookup (GIS) and the filing portal. The filing portal vendor is GovOS. — [CDOR SUTS Functionality Study, Oct 2025](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- SUTS "is a filing portal ... It is not, however, a centralized system of record." DOR (GenTax) and each home-rule city keep separate systems of record. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Lookup features: search by address, latitude/longitude or map click; returns the taxing jurisdictions and current general sales tax rates; rate histories; export of search results; bulk address lookup; an API; and a taxability matrix covering "over 350 products and services" showing state and local treatment. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Coverage: retailers can file and pay in one place for all state-administered jurisdictions "and all but two self-collecting home rule municipalities" (Oct 2025). — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- DOR, Sept 2026: SUTS launched November 2020; "over 90%" of home-rule jurisdictions participate. — [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause)
- The DOR participating-jurisdictions page marks roughly 60 home-rule self-collecting municipalities as participating (my fetch tool's count of asterisked entries, undated page; Denver and Broomfield are listed separately; Merino and Pagosa Springs shown as coming 1 Jan 2026). Treat the exact count as approximate. — [CDOR SUTS Participating Jurisdictions](https://tax.colorado.gov/SUTS-Jurisdictions)
- Early uptake: 50 to 51 participating home-rule self-collectors by December 2020 (snippet of secondary summaries of DOR tracking reports). — [CDOR report on home rules joining SUTS, Jan 2021](https://Tax.colorado.gov/sites/tax/files/Report_on_Home_Rule_Municipalities_Joining_SUTS_1-20-2021.pdf)
- API: intended to let a point-of-sale system pull current rates per transaction. A key is generated inside a SUTS account (registration required), per business; aimed at custom in-house POS systems. Method documentation sits behind login on the key screen; DOR will not advise on programming. The public page states no rate limits, cost or licence. — [CDOR GIS API](https://tax.colorado.gov/GIS-API)
- Hold-harmless: a vendor that uses the GIS data to determine rate and jurisdiction is held harmless in an audit by DOR or any local jurisdiction for tax owed solely because of an error or omission in the GIS data. Conditions: the vendor must keep and produce documentation showing proper use and reliance; a query with an incomplete or erroneous address is not protected. It applies to home-rule self-collectors only if they participate in SUTS. — [CDOR GIS hold harmless provision](https://tax.colorado.gov/gis-hold-harmless-provision)
- Bulk lookup: added January 2024 under HB23-1017; users upload a spreadsheet of addresses or coordinates with an optional record ID. Almost 99 million addresses were searched in FY 2024-25. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Bulk lookup pause: announced 25 Sept 2026, effective 29 Sept 2026, with a "managed" return planned for 1 Jan 2027. Funding under HB23-1017 was $1.275 million per year for up to 75 million lookups; FY 2025-26 usage was 136.5 million lookups (requiring extra General Fund money) and the first three months of FY 2026-27 exceeded 50 million. Single-address lookup and the filing portal remain free. — [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause); [Sales Tax Institute](https://www.salestaxinstitute.com/resources/colorado-suts-bulk-address-lookup-paused)
- Filing portal performance after the HB23-1017 rebuild (new UI January 2025): spreadsheet-filing completion rate rose from 40% (Jan 2024, median just over 14 minutes) to 71% (Jan 2025, median just under 5 minutes); direct-entry filing had a 55% completion rate. The rebuild drew on 52 interviews and over 1,000 survey responses. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- The 2025 workgroup produced 20 recommended improvements costing an estimated $624,720 plus $37,500 a year in maintenance. Requests ruled out of scope included free state-provided calculation and filing software, and requiring home-rule cities to use the state account number or a common system of record. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- A barrier for large filing services: ACH credit payments must match the amount due exactly so SUTS can allocate among jurisdictions. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- DOR's general open-data terms (updated 14 Nov 2024) cover data published on its website: "as is", no warranty of accuracy or timeliness, the user must indemnify the State, redistributors must carry a State disclaimer that the data may have been modified, and the State may change or discontinue any feed at any time. No explicit open licence is granted. — [CDOR Open Data Use Terms](https://cdor.colorado.gov/department-of-revenue-open-data-use-terms)

### Inferences
- The implied unit cost of the bulk lookup is about 1.7 cents per address ($1.275 million / 75 million). At 136.5 million lookups, usage ran at 182% of the funded cap. A per-query service scales cost with demand; a published boundary and rate file would not, which is a direct argument for bulk open data. The counter-argument is that DOR pays a vendor for the GIS product and may not own redistribution rights (unverified, see Gaps).
- There are two opposite "hold harmless" regimes: sellers relying on the GIS lookup are protected by the State, whereas users of DOR's downloadable open data must indemnify the State. A third-party open dataset derived from DOR files would inherit the second, not the first. That is the central liability asymmetry.
- The hold-harmless requires address-level queries with documentation, so a ZIP-level or static rate table cannot qualify even if accurate.
- Participation is near-universal for filing (all but two self-collectors), but SUTS does not harmonize bases, licences or audits. It is plumbing, not simplification of law.

### Gaps
- The name of the GIS lookup vendor, contract values and contract terms for either vendor were not confirmed in sources I read. (The SUTS site historically ran on colorado.munirevs.com and now appears at colorado.blt.govos.com, suggesting MuniRevs became GovOS, but I did not verify the corporate history or the GIS vendor.)
- Which two self-collecting home-rule municipalities remain outside SUTS was not stated in the sources read.
- I could not confirm whether DOR publishes jurisdiction boundary polygons (shapefile or GeoJSON) for download; none was found. The API's response schema, rate limits and terms are behind login.
- The "alternative data options" FAQ that DOR points to (Tax.Colorado.gov/SUTS-info) was not read.

## 3. Legislation and the status of home-rule simplification through 2026

### Takeaway
The path ran from the 2017 task force, through 2018 to 2019 bills that funded SUTS and adopted economic nexus and destination sourcing, to 2023 to 2024 bills that upgraded the system and penalized non-participation. Simplification remains voluntary for home-rule cities, and the task force appears to have gone quiet: it did not meet in the 2025 interim and its statutory life ran to 1 July 2026.

### Cited Findings
- HB17-1216 created the Sales and Use Tax Simplification Task Force, charged with revenue-neutral solutions not requiring constitutional amendment or voter approval. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- HB18-1022 required DOR to issue a request for information for an electronic system providing address-level jurisdiction data, a single licence application, a uniform remittance form, a single point of remittance and a taxability matrix. SB19-006 appropriated funds and required DOR to procure it. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Remote-seller collection began 1 Dec 2018 with a grace period to 31 May 2019. HB19-1240 codified the $100,000 threshold (dropping the 200-transaction test), barred retroactive collection and required marketplace facilitators to collect. — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/)
- HB20-1022 extended the task force five years, to 1 July 2026 (snippet). — [Colorado General Assembly, task force final report page](https://leg.colorado.gov/publications/sales-and-use-tax-simplification-task-force-final-report-3)
- HB23-1017 (a task force bill) funded SUTS improvements due by 1 Jan 2025, including the bulk lookup and the new filing interface. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- HB24-1041 (signed 4 Apr 2024): home-rule localities not using SUTS cannot collect from retailers without in-state physical presence unless the retailer opts in or signs a voluntary collection agreement; quarterly filing threshold raised from $300 to $600 a month from 1 Jan 2025. — [Sales Tax Institute](https://www.salestaxinstitute.com/resources/colorado-changes-requirements-for-home-rule-jurisdictions-not-using-suts)
- HB24-1050 widened the task force's scope to local lodging taxes and restricted certain practices of self-collecting home-rule jurisdictions that do not use SUTS, for returns filed on or after 1 Jan 2026 (snippet). — [Legislative Council memo on 2024 session legislation](https://leg.colorado.gov/sites/default/files/images/committees/final_sutstf_memo_re_2024_session_legislation.pdf)
- The task force's last full report found is November 2024 (Research Publication 817). It did not meet in the 2025 interim, and the 2026 interim page lists no hearings (snippet). — [2025 interim page](https://leg.colorado.gov/committees/2025B/interim/SalesandUseTaxSimplificationTaskForce); [2026 interim page](https://leg.colorado.gov/committees/2026A/interim/SalesandUseTaxSimplificationTaskForce)
- CML economic nexus and marketplace facilitator model ordinance: released 29 May 2020 for self-collecting home-rule municipalities joining SUTS, using a $100,000 threshold; adoption is a two-step process (adopt the ordinance, then sign the SUTS agreement with the State). — [CML model ordinance page](https://www.cml.org/home/advocacy-legal/Members39-Guide-to-Legal-Consulting-Services-and-Amicus-Briefs/cml-model-ordinance---economic-nexus-marketplace-facilitators); [EY Tax News, Aug 2020](https://taxnews.ey.com/news/2020-1989-colorado-home-rule-self-collected-municipalities-begin-adopting-economic-nexus-and-marketplace-facilitator-collection-laws-after-launch-of-online-centralized-filing-portal); [Accounting Today](https://www.accountingtoday.com/news/colorado-model-ordinance-aims-to-simplify-online-sales-tax)
- CML Sales Tax Standard Definitions Project: traces to a 2014 legislative resolution asking CML to develop standardized definitions; CML provides a template ordinance, an Excel matrix comparing existing with standard definitions and fiscal impacts, and a list of adopting self-collecting municipalities as of 1 Jan 2025. — [CML Standard Definitions Project](https://www.cml.org/home/advocacy-legal/Members39-Guide-to-Legal-Consulting-Services-and-Amicus-Briefs/Sales-Tax-Standard-Definitions-Project); [Grand Junction Ordinance 4892](https://trim22-web.gjcity.org/GJ_WebDrawer/Record/1023830/File/document)
- Some home-rule jurisdictions began enforcing nexus provisions without formal notice (2021 observation). — [Grant Thornton, Mar 2021](https://www.grantthornton.com/insights/alerts/tax/2021/salt/a-e/co-home-rule-jurisdictions-enact-new-taxes-03-16)
- Tax Foundation's legal view (2019, updated 2023): self-collecting localities cannot be forced to follow the State's remote-seller rules, and local collection duties on remote sellers raise dormant Commerce Clause risk. — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/)

### Inferences
- The State's lever is conditional: it cannot mandate a uniform base on home-rule cities without constitutional change, so it ties remote-seller collection rights and the hold-harmless to SUTS participation. That explains near-universal portal participation alongside persistent base differences.
- Standard definitions standardize vocabulary, not taxability: a city can adopt the CML definition of an item and still choose to tax or exempt it. A machine-readable taxability matrix therefore remains necessary even with full adoption.
- If the task force lapsed on 1 July 2026 without extension, there is no standing legislative venue for the next round of simplification. This needs verification.

### Gaps
- Whether the task force was extended, repealed or replaced in the 2026 session was not confirmed. No 2026 final report was found.
- The number of municipalities that have adopted the CML standard definitions (the 1 Jan 2025 list) was not retrieved.
- HB19-1240's destination-sourcing provisions and the small-retailer exception dates were not confirmed from a primary source in this pass.
- No Colorado Sun, CPR or Denver Post coverage was retrieved in this pass.

## 4. What does the Department of Revenue already publish as data, and in what formats?

### Takeaway
DOR publishes rates and codes twice a year as PDFs (DR 1002, DR 0800) plus a combined downloadable spreadsheet, and exposes address-level answers through the GIS lookup and a login-gated API. This is machine-readable in part, but it is not versioned open data with a licence, boundaries or home-rule taxability rules in bulk.

### Cited Findings
- DR 1002 (Colorado Sales/Use Tax Rates) is updated on 1 January and 1 July each year. — [CDOR DR 1002 form updates](https://tax.colorado.gov/dr-1002-form-updates); [CDOR DR 1002](https://tax.colorado.gov/DR1002)
- DOR's lookup page offers a downloadable spreadsheet combining DR 1002 rates with DR 0800 location and jurisdiction codes, issued per half-year (the indexed list ran to January to June 2026 at time of search; a July to December 2026 file is referenced by third parties). — [CDOR How to Look Up Location Codes & Tax Rates](https://tax.colorado.gov/how-to-look-up-sales-use-tax-rates); [ustax.tools citing the July to Dec 2026 spreadsheet](https://ustax.tools/colorado-sales-tax-rates/)
- DR 0800 (location/jurisdiction codes) is published annually as a PDF; the 2026 edition notes that the SUTS portal can file for most self-collected home-rule cities in a single return (snippet). — [DR 0800 2026](https://tax.colorado.gov/sites/default/files/documents/DR0800_2026_0.pdf)
- DOR published local rate changes effective 1 July 2026 (rate increases, newly adopted exemptions, newly imposed taxes). — [Sovos](https://sovos.com/regulatory-updates/sut/colorado-releases-local-sales-use-tax-changes-effective-july-1-2026/); [CDOR sales tax rate changes](https://tax.colorado.gov/sales-tax-rate-changes)
- Historical DR 1002 editions are archived as PDFs by the State Publications Library (e.g. July 2020, July 2025, January 2026). — [State Publications Library, DR 1002 Jan 2026](https://spl.cde.state.co.us/artemis/revserials/rev914internet/rev914202601internet.pdf)
- The GIS lookup shows rate histories and lets users export search results; the taxability matrix is an interactive tool covering 350+ items. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- DOR also publishes retail sales statistics. — [CDOR Sales Data](https://cdor.colorado.gov/sales-data)
- Terms for all DOR web data: "as is", indemnity owed to the State, mandatory disclaimer on redistribution, feeds may change or stop at any time (updated 14 Nov 2024). — [CDOR Open Data Use Terms](https://cdor.colorado.gov/department-of-revenue-open-data-use-terms)

### Inferences
- Rate changes take effect on a predictable semi-annual cycle (1 January, 1 July), which makes a versioned open dataset tractable: two scheduled releases a year plus corrections.
- The existing spreadsheet is the natural seed for an open dataset, but it gives rates by named jurisdiction and code, not geometry. Mapping an address to jurisdictions still requires the GIS service.
- The archive of semi-annual PDFs means a historical rate series could be reconstructed, but only by PDF extraction.

### Gaps
- I found no sales tax rate or boundary dataset on the Colorado Information Marketplace (data.colorado.gov); the search surfaced none, but I did not query the portal's catalogue directly, so absence is not confirmed.
- Whether the taxability matrix can be exported in bulk is unknown.
- Whether self-collecting home-rule rates and exemptions appear in the combined spreadsheet with the same detail as state-collected jurisdictions was not verified.

## 5. How are income tax parameters set and published?

### Takeaway
Colorado's headline parameters are simple (a flat 4.4% rate) but several are contingent: the rate can be cut temporarily by a TABOR surplus formula, and the EITC percentage and Family Affordability Tax Credit switch on revenue-growth triggers. The authoritative values emerge late, from Legislative Council forecasts, the State Controller's certification and DOR forms and guidance, not from one data file.

### Cited Findings
- The individual and corporate income tax rate is a flat 4.4%, "with the possibility of a reduction to a rate as low as 4.25 percent retroactively, subject to revenues hitting certain targets". — [Tax Foundation State Tax Index, Colorado](https://taxfoundation.org/statetaxindex/states/Colorado/)
- TABOR requires income to be taxed at a single rate. Proposition MM (2025) raised income tax revenue for school meals and food assistance and exempted it from the TABOR limit. — [Legislative Council Staff memo, "A Brief Overview of the TABOR Revenue Limit", 6 Aug 2026](https://content.leg.colorado.gov/sites/default/files/r26-757-the-tabor-limit-accessible.pdf)
- Four refund mechanisms apply in order: (1) reimbursing local governments for homestead property tax exemptions (seniors, disabled veterans, Gold Star spouses) and the qualified-senior primary residence benefit; (2) a temporary income tax rate reduction if the remaining surplus is large enough, sized as a percentage-point cut scaled to the surplus; (3) a temporary sales and use tax rate reduction if the surplus exceeds $1.5 billion above the first two mechanisms; (4) the six-tier sales tax refund, scaled by adjusted gross income and claimed on the income tax return. — [Legislative Council Staff memo, 6 Aug 2026](https://content.leg.colorado.gov/sites/default/files/r26-757-the-tabor-limit-accessible.pdf)
- Forecast in that memo: refunds in tax year 2028 of between $150 million and $200 million through each of the property tax, income tax rate and six-tier mechanisms, not enough to trigger the sales tax rate cut; "actual refund amounts may vary considerably from the forecast". (Figures read from a text-extracted PDF; verify the tax year against the original.) — [Legislative Council Staff memo, 6 Aug 2026](https://content.leg.colorado.gov/sites/default/files/r26-757-the-tabor-limit-accessible.pdf)
- Tax year 2024: SB24-228 delivered the refund as a temporary rate cut from 4.40% to 4.25% plus a sales tax refund (snippet). — [Post Independent](https://www.postindependent.com/news/colorado-tabor-refund-taxpayers-bill-of-rights-legislative-council)
- Refunds are smaller in 2026 and were forecast to be zero in 2027 (snippet). — [Post Independent](https://www.postindependent.com/news/colorado-tabor-refund-taxpayers-bill-of-rights-legislative-council)
- One secondary source reports a 2026 refund via a rate cut from 4.40% to 4.36%; I could not confirm this against any official source. — [Kim Monson Show podcast summary](https://the-kim-monson-show-2.castos.com/episodes/colorado-tabor-refunds-shrink-to-under-100-as-lawmakers-redirect-the-surplus)
- Third-party sites disagree on basics: some say 4.25% applied to 2025, most say 4.4%; some date the 4.55% to 4.4% cut to 2023 and others to 2024; some still list 2026 Family Affordability amounts although the credit is paused. — [TaxAct](https://blog.taxact.com/what-is-colorado-state-income-tax/); [Reed Corp](https://reedcorp.tax/helpful-guides/colorado-state-income-tax/); [NerdWallet](https://www.nerdwallet.com/taxes/learn/colorado-state-income-tax-rates)
- State EITC: 50% of the federal credit for tax years 2024 and 2025, falling to 25% for tax year 2026 (filed in 2027). — [CDOR CTC and EITC page](https://tax.colorado.gov/CTC-EITC)
- Family Affordability Tax Credit: created by HB24-1311 for tax years 2024 to 2033; paused for tax year 2026 because it switches off when revenue projections fall below a threshold growth rate and resumes when they exceed it. — [CDOR CTC and EITC page](https://tax.colorado.gov/CTC-EITC); [Common Sense Institute](https://www.commonsenseinstituteus.org/colorado/research/taxes-and-fees/colorados-expanded-tax-credits-targeting-lower-income-families); [CDOR Income Tax Topics: Family Affordability Tax Credit, Jan 2026](https://tax.colorado.gov/sites/tax/files/documents/ITT_Family_Affordability_Tax_Credit_Jan_2026.pdf)
- Colorado Child Tax Credit: for children under 6 with income at or under an annual threshold; refundable. The DOR page gives no amounts. — [CDOR CTC and EITC page](https://tax.colorado.gov/CTC-EITC)
- Two competing income tax measures were on the 3 November 2026 ballot: Initiative 232 (cap rates at 4.4%) and Initiative 195 (replace the flat rate with six tiers from 3.7% to 8.4%). — [Ballotpedia News, 24 Aug 2026](https://news.ballotpedia.org/2026/08/24/colorado-voters-to-decide-on-income-tax-cap-measure-that-competes-with-proposed-graduated-income-tax-initiative/); [Ballotpedia News, 3 Sept 2026](https://news.ballotpedia.org/2026/09/03/colorado-voters-will-decide-on-a-graduated-income-tax-initiative-that-competes-with-an-income-tax-cap-measure-in-november/)

### Inferences
- Income tax parameters are few but conditional and late-binding. The rate for a tax year can change after the year has started (the Tax Foundation describes the cut as retroactive), and credits switch on forecasts. An open parameter file would need effective dates, a status field (forecast, certified, enacted) and provenance for each value.
- The visible disagreement among calculator and guide sites on the 2025 rate, the date of the 4.4% cut and the paused credit is direct evidence of the cost of having no single authoritative machine-readable source.
- Authority is split: statute and ballot measures set base values, Legislative Council and the Governor's budget office forecast triggers, the State Controller certifies the surplus (the LCS memo's revenue chart cites the Office of the State Controller), and DOR publishes the operative numbers in forms and Income Tax Topics. No single body publishes a consolidated table.

### Gaps
- The results of the 3 November 2026 votes on Initiatives 232 and 195 were not retrieved. If Initiative 195 passed, the "single flat rate" structure described here changes fundamentally. This must be checked before the report is finalized.
- The certified income tax rate for tax years 2025 and 2026, and the six-tier sales tax refund amounts, were not confirmed from DOR or the State Controller.
- The exact surplus thresholds for the income tax rate cut, the trigger growth rates for the EITC and Family Affordability Tax Credit, child tax credit amounts and income bands, and the calendar on which each number is certified were not retrieved.
- Any 2025 special-session or 2026-session changes to credits beyond what the DOR page shows were not researched.

## 6. Commercial providers and the Streamlined Sales Tax (SST) rate and boundary files

### Takeaway
SST member states must publish free, standardized rate and boundary files and give sellers and certified service providers liability relief for relying on them. Colorado is not a member, largely because home rule and TABOR block the uniformity SST requires, so Colorado offers a lookup service with a hold-harmless instead of downloadable files, and commercial engines fill the gap.

### Cited Findings
- Colorado is not a Streamlined member state. — [Streamlined Sales Tax Governing Board, Colorado](https://www.streamlinedsalestax.org/state-details/colorado)
- At a 2017 legislative hearing, a Streamlined presenter cited Colorado's "unique challenges due to TABOR and home rule constitutional issues" (snippet). — [Colorado General Assembly hearing summary, 15 Sept 2017](https://leg.colorado.gov/content/itaxtask2017a2017-09-15t090253z1-hearing-summary)
- The SST Agreement requires each member state to provide and maintain a boundary database at five- and nine-digit ZIP level; rate and boundary files are downloadable from the Governing Board site. Five-digit-only matching often returns the state rate alone, omitting local tax. — [NC DOR, Rate and Boundary Database Information](https://www.ncdor.gov/taxes-forms/sales-and-use-tax/other-sales-and-use-tax-resources/streamlined-sales-tax-information/rate-and-boundary-database-information); [TaxJar](https://www.taxjar.com/blog/streamlined-sales-tax-benefits-and-risks)
- SST liability relief: states hold a seller harmless for over- or under-collecting where it relied on the state's rate and boundary files; sellers using a certified service provider (CSP) with correct inputs get relief from audit liability for calculation errors. — [TaxJar](https://www.taxjar.com/blog/streamlined-sales-tax-benefits-and-risks); [SST Agreement Appendix E, CSP certification](https://www.streamlinedsalestax.org/docs/default-source/agreement/appendixes/appendix-e-csp-cas-certification-process.pdf)
- CSPs advertise free calculation and filing in SST states; member-state counts are quoted as 24 (TaxCloud) or 25 (Avalara) (snippet). — [TaxCloud](https://taxcloud.com/?p=13956); [Avalara](https://www.avalara.com/us/en/products/sales-and-use-tax/streamlined-sales-tax/videos/video-avalara-is-streamlined-sales-tax-right-for-your-business.html)
- Before SUTS, retailers had to navigate five databases to determine Colorado tax owed (2019). — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/)
- DOR's own description of who was hitting the bulk lookup in 2026: it notified "high-volume users, municipal partners, and commercial entities" of the pause. — [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause)
- Software providers and filing services sat on the 2025 SUTS workgroup (14 members drawn from 42 applicants). — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)

### Inferences
- Non-membership has three practical effects: no free CSP services funded by the State for Colorado sales, no SST-format rate and boundary files, and no SST taxability matrix or uniform definitions. Colorado's GIS lookup, hold-harmless and 350-item matrix are home-grown substitutes for each.
- Colorado's address-point GIS approach is technically more precise than SST's ZIP+4 boundary files, but it is delivered as a metered service. SST shows that a state can publish boundaries and rates as flat files with liability relief attached; Colorado attaches relief only to its own lookup.
- The volume that overwhelmed the bulk lookup (136.5 million in FY 2025-26) plausibly came in large part from commercial engines and large sellers refreshing address data, meaning the State is partly subsidizing commercial products. I found no breakdown to confirm this.

### Gaps
- No vendor documentation (Avalara, Vertex, TaxJar) describing how each sources Colorado home-rule boundaries and taxability, pricing, or accuracy guarantees was retrieved.
- No independent accuracy comparison between SUTS GIS and commercial engines was found.
- The current SST member count and the exact SST file formats were not verified on the Governing Board site.

## 7. Pros and cons of an open parameter dataset

### Takeaway
The case for open data is strongest for bulk rate and boundary data (demand is proven, and metered delivery has already broken the State's budget) and for income tax parameters (third-party sites visibly disagree). The case against is mostly about authority and liability: only the State's own GIS lookup carries audit protection, home-rule taxability is controlled by about 66 separate councils, and an unofficial dataset shifts error risk onto its users and publisher.

### Cited Findings
Evidence supporting an open dataset:
- Demand for bulk data is large and growing: about 99 million bulk lookups in FY 2024-25, 136.5 million in FY 2025-26, over 50 million in the first quarter of FY 2026-27, against a budget for 75 million a year at $1.275 million. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf); [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause)
- The free bulk channel can be withdrawn at short notice: four days between announcement (25 Sept 2026) and pause (29 Sept 2026), with a three-month outage. — [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause)
- Users asked the State for free calculation, reporting and remittance software; DOR treated it as out of scope. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Rate data already changes on a fixed semi-annual schedule and is already issued as a spreadsheet. — [CDOR DR 1002 form updates](https://tax.colorado.gov/dr-1002-form-updates); [CDOR How to Look Up Location Codes & Tax Rates](https://tax.colorado.gov/how-to-look-up-sales-use-tax-rates)
- Public information on income tax parameters is inconsistent across third-party sites (2025 rate, paused credit). — [Reed Corp](https://reedcorp.tax/helpful-guides/colorado-state-income-tax/); [TaxAct](https://blog.taxact.com/what-is-colorado-state-income-tax/); [CDOR CTC and EITC page](https://tax.colorado.gov/CTC-EITC)
- SST states demonstrate that free rate and boundary files with liability relief are workable at scale. — [NC DOR](https://www.ncdor.gov/taxes-forms/sales-and-use-tax/other-sales-and-use-tax-resources/streamlined-sales-tax-information/rate-and-boundary-database-information)

Evidence against, or complicating:
- Audit protection attaches only to documented, address-level use of the State GIS database, and for home-rule cities only where they participate in SUTS. — [CDOR GIS hold harmless provision](https://tax.colorado.gov/gis-hold-harmless-provision)
- DOR's open-data terms disclaim accuracy and timeliness, require users to indemnify the State, and reserve the right to change or stop feeds. — [CDOR Open Data Use Terms](https://cdor.colorado.gov/department-of-revenue-open-data-use-terms)
- DOR "has a history of registering businesses in the wrong taxing jurisdiction" (Tax Foundation, 2019/2023), showing that even the authoritative source has had boundary errors. — [Tax Foundation](https://taxfoundation.org/blog/colorado-wayfair-complexity-legal/)
- SUTS is not a system of record; DOR and each home-rule city maintain separate systems, so there is no single upstream database to export. — [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)
- Home-rule taxability is set by local ordinance, and some cities have enforced new provisions without formal notice. — [Grant Thornton, Mar 2021](https://www.grantthornton.com/insights/alerts/tax/2021/salt/a-e/co-home-rule-jurisdictions-enact-new-taxes-03-16)
- Coarse data gives wrong answers: five-digit ZIP matching often drops local tax entirely. — [TaxJar](https://www.taxjar.com/blog/streamlined-sales-tax-benefits-and-risks)
- Income tax values are forecast-dependent and can change retroactively; LCS warns actual refunds "may vary considerably from the forecast". — [Legislative Council Staff memo, 6 Aug 2026](https://content.leg.colorado.gov/sites/default/files/r26-757-the-tabor-limit-accessible.pdf); [Tax Foundation State Tax Index](https://taxfoundation.org/statetaxindex/states/Colorado/)
- The State is already spending on the existing system: $1.275 million a year for bulk lookup alone, plus an estimated $624,720 for the 2025 workgroup's portal improvements. — [CDOR Bulk Address Lookup Pause](https://tax.colorado.gov/Bulk-Address-Lookup-Pause); [CDOR SUTS Functionality Study](https://mtc.gov/wp-content/uploads/2025/11/SUTS-Functionality-Study-CDOR-October-2025.pdf)

### Inferences
- Liability: a state-published file could carry the hold-harmless (as SST files do); a third-party open dataset cannot, and under DOR's terms its publisher indemnifies the State. The policy question is therefore less "open or not" than "who publishes, and does the hold-harmless extend to file-based use".
- Cost: marginal cost of a published file is near zero per use, against about 1.7 cents per bulk lookup under the current contract. Offsetting this, publishing geometry may require renegotiating vendor rights (unverified) and the State loses usage telemetry.
- Update cadence: sales tax rates suit two releases a year; boundaries (annexations) and home-rule ordinance changes do not follow that calendar, and income tax triggers resolve on the forecast and certification calendar. A dataset needs effective-dated records, not snapshots.
- Authority: for state-collected jurisdictions DOR is the single authority. For the roughly 66 self-collectors the authority is each municipal code, so an open taxability dataset would be a secondary compilation unless cities certify their entries.
- Beneficiaries: small and remote sellers who cannot afford commercial engines and whose volumes exceed single-address lookup; researchers and fiscal analysts needing historical rate series (currently PDF archives); developers of calculators and rules-as-code models; and the State itself if open files divert bulk traffic. Commercial providers benefit too, which weakens the argument that open data displaces them: their value lies in taxability content, filing and indemnity, not in raw rates.
- Risk of false confidence: an open rates file without taxability rules could lead small sellers to believe they are compliant in home-rule cities when the base, not the rate, is where they err.

### Gaps
- No Colorado source was found that directly debates publishing tax parameters as open data, so the pros and cons above are assembled from adjacent evidence rather than from stakeholder positions.
- No data on error rates in SUTS GIS data, hold-harmless claims made, or audit assessments avoided.
- No estimate of the cost to build and maintain an open dataset, and no confirmation of who owns the GIS boundary layer.
- No evidence on small-seller compliance costs in Colorado specifically (surveys, studies) was retrieved in this pass.
