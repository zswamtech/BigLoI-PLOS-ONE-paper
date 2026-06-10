# Computational surveillance of Colombian public pharmaceutical procurement using public administrative data: a reproducible analysis of a closed 2020-2025 cohort

Andres Soto  
Independent researcher  
Bogota, Colombia  
ORCID: 0009-0004-8001-5372  
Correspondence: <ansoto1604@icloud.com>

---

## Abstract

**Introduction.** BigLoI monitors Colombian public pharmaceutical procurement from 2015 onward. For this manuscript, the closed analytical cohort comprised 162,271 pharmaceutical contracts from 2020 to 2025, avoiding year-to-year comparisons with incomplete 2026 records.

**Objective.** To describe the design, implementation, and findings of a reproducible computational infrastructure for surveillance of Colombian public pharmaceutical procurement.

**Methods.** Public APIs from SECOP-II, INVIMA, and SISMED were integrated into a reproducible architecture combining PostgreSQL, statistical analysis, and a public-facing observatory. A Z-score engine was implemented to flag contracts with atypical total values within therapeutic categories. As a clearly secondary technical-feasibility module, smart-contract automation of a payment workflow was tested on the Sepolia testnet only to verify predefined digital state transitions under simulated conditions. The closed analytical cohort included 162,271 pharmaceutical contracts from 2020 to 2025, while post-2025 records remained available only for live platform monitoring. Monetary results were reported primarily in COP; secondary USD equivalents were included only as approximate interpretive references, with detailed conversions relegated to S1 Table.

**Results.** Among 147,020 contracts analyzed in categories with at least 10 observations, 685 contracts (0.47%) triggered a statistical alert with absolute Z-score greater than or equal to 1.5 sigma. The alert rate increased from 0.31% in 2021 to 1.38% in 2025. Antibiotics showed the highest category-level maximum Z-score (8.32). The top 3% of suppliers concentrated 85.9% of total contracted value. In the secondary automation module, the Sepolia prototype confirmed only that predefined digital state transitions could be executed under test conditions and supported only an illustrative financial-savings scenario of COP 224,000-330,000 million per year (approximately USD 56.0-82.5 million at a reference rate of COP 4,000/USD) under favorable assumptions about administrative-delay reduction; it did not measure real institutional processing times or realized savings.

**Conclusions.** A reproducible national-scale computational infrastructure identified atypical procurement patterns and documented marked market concentration in Colombian public pharmaceutical procurement. These findings are relevant for auditing, public health policy, and health data governance. The blockchain module should be interpreted strictly as a complementary technical proof of concept and not as operational evidence on real-world payment performance, savings, or implementation readiness.

**Keywords:** public pharmaceutical procurement; SECOP-II; procurement surveillance; market concentration; anomaly detection; retrieval-augmented generation; blockchain; SISMED; INVIMA; Colombia.

---

## 1. Introduction

Public procurement of medicines in Colombia is monitored in BigLoI through a broad SECOP-II universe that now exceeds 272,000 contracts from 2015 onward. For the purposes of this manuscript, the closed indexed analytical cohort corresponds to 162,271 pharmaceutical contracts from 2020 to 2025. Despite this scale, the system lacks reproducible real-time surveillance tools to detect atypical procurement patterns, market concentration, or potential supply risks.

The World Health Organization has estimated that 10% to 25% of global health expenditure is lost to corruption, inefficiency, and administrative errors (2). In Colombia, official audits have documented high-cost medicine overpricing, prolonged payment delays, and recurring episodes of shortages (3,4).

Integration of public APIs makes it possible to build procurement-surveillance platforms without access to confidential information. Z-score analysis is a practical approach for detecting atypical patterns in large procurement datasets (6), while smart contracts and semantic retrieval expand the range of possible automation and evidence-access tools (7,8). Initiatives such as ProZorro, OCDS, and OLAF illustrate the feasibility of these approaches in public-procurement transparency (9-11).

BigLoI (Business Intelligence for Government Logistics and Operations Intelligence) was developed to address this gap. This article documents its methodology and findings as a contribution to the debate on computational tools for governance of the Colombian health system.

---

## 2. Methods

### 2.1 Study design

This was a technological-development study with longitudinal observational analysis of public procurement data. Only openly accessible Colombian public data sources were used. No clinical data or patient-level personal data were included.

**Ethics statement.** This study used only publicly accessible administrative procurement records published by Colombian open-data sources (SECOP-II via datos.gov.co, INVIMA, and SISMED). It did not involve human participants, patient-level or clinical data, identifiable private information, biological samples, recruitment, intervention, or any contact with individuals. Accordingly, the study does not constitute human-subjects research and did not require review or approval by an institutional review board or research ethics committee. Under Colombian Resolution 8430 of 1993, analysis of public, non-identifiable administrative records corresponds to research without risk and falls outside the scope of human-subjects ethics review. Informed consent was not applicable because the study did not involve human participants or identifiable personal data. All analyzed data are publicly available and were used in aggregate for the surveillance of public procurement.

### 2.2 Data sources

**SECOP-II (Electronic Public Procurement System).** The public Socrata API from datos.gov.co was used for automated download of pharmaceutical procurement contracts. Inclusion required the presence of at least one of 19 pharmaceutical terms in the contract-object description. Obvious false positives were excluded. The platform monitoring window extends from January 2015 onward, but the closed analytical cohort used in this manuscript was restricted to complete calendar years 2020-2025.

**SECOP-II monitored universe available to the platform:** 272,814 unique contracts; COP 42 trillion; 163,135 suppliers; 37 regional codes  
**Recovered local PostgreSQL source used to reproduce the manuscript cohort:** 956,157 total SECOP-II records; 165,549 pharmaceutical records including live 2026 monitoring rows; 162,271 pharmaceutical contracts in the closed 2020-2025 analytical cohort

To avoid comparing incomplete calendar periods, all year-by-year descriptive analyses in the manuscript were closed at 31 December 2025. The platform continues to ingest newer records for operational monitoring, but post-2025 records were excluded from the formal analytical cohort reported here.

All primary monetary values are reported in COP. When approximate USD equivalents are provided in parentheses, they are secondary interpretive aids calculated using a round reference exchange rate of COP 4,000 per USD, close to late-2025 market levels. No analyses were performed in USD. Because a single round reference rate is applied across the entire 2020-2025 study period, the USD equivalents do not account for exchange-rate volatility and should be read as order-of-magnitude approximations only; the COP values are the analytical quantities. Detailed COP/USD reference conversions for the principal manuscript figures are provided in S1 Table.

**INVIMA (National Food and Drug Surveillance Institute).** A total of 9,838 records from the national sanitary registry were downloaded through the Socrata API. Variables included brand name, active ingredient, marketing authorization holder, sanitary registration number, ATC code, dosage form, route of administration, relevant dates, and registry status. All loaded records were current.

**SISMED (Medicine Price Information System, Ministry of Health).** We processed 44,038 reference-price records covering 1,759 unique ATC codes, aggregated by dosage form, distribution channel, and reference year (2017-2019). These data were used as contextual market references and as complementary input for interpreting atypical contract-value findings.

### 2.3 BigLoI technical architecture

The platform was implemented as a monorepo with a seven-layer architecture (Table 2). Figure 6 summarizes the seven-layer technical architecture of the platform.

### Table 2. Technical architecture of the BigLoI platform for surveillance of public pharmaceutical procurement

| Layer | Main technology | Function |
| --- | --- | --- |
| Collection | Python; Socrata API | Incremental ingestion of SECOP-II, INVIMA, and SISMED |
| Storage | PostgreSQL; Pinecone; MongoDB | Relational, vector, and unstructured data storage |
| Processing | FastAPI; pandas | Cleaning, normalization, ABC classification, Z-score engine |
| Generative AI | Claude 3.5 Sonnet; GPT-4o | Hybrid semantic plus TF-IDF retrieval-augmented generation |
| Machine learning | scikit-learn | Demand prediction ($R^2 > 0.85$), k-means (6 groups), PCA |
| Smart contracts (proof of concept) | Solidity; Chainlink CRE; Sepolia testnet | Simulated payment-state transitions across five digital states; invoice NFTs (secondary module) |
| Visualization | React/TypeScript | Public observatory with time series, maps, and alerts |

### 2.4 Anomaly-detection engine based on Z-scores

For each pharmaceutical contract classified into a therapeutic category, we calculated the standardized deviation of its total contract value relative to the distribution of observed values within the same category. The analysis was restricted to categories with at least 10 contracts to avoid unstable estimates:

$$
Z_i = \frac{V_i - \bar{V}_{cat}}{\sigma_{cat}}
$$

where $Z_i$ is the anomaly score for contract $i$, $V_i$ is the contract's total value, $\bar{V}_{cat}$ is the mean contract value within the same therapeutic category, and $\sigma_{cat}$ is the standard deviation of that category-specific distribution. This approach detects contracts with atypical total values relative to their category; by itself, it does not establish unit-price overpricing against a regulatory benchmark.

Alert levels were classified as follows:

| Level | Criterion | Interpretation |
| --- | --- | --- |
| Critical | Absolute Z-score greater than or equal to 3.0 sigma | Extremely atypical contract value within category |
| High | Absolute Z-score from 2.0 to less than 3.0 sigma | Clearly atypical contract value |
| Moderate | Absolute Z-score from 1.5 to less than 2.0 sigma | Moderately atypical contract value |
| Normal | Absolute Z-score below 1.5 sigma | Within the expected range for category |

### 2.5 Market-concentration analysis

To characterize the competitive structure of the pharmaceutical procurement market, we calculated descriptive concentration indicators and estimated the proportion of total contracted value accumulated by leading suppliers. Supplier concentration was calculated over positive-value contracts in the closed 2020-2025 pharmaceutical cohort. The Herfindahl-Hirschman Index (HHI) was calculated as the sum of squared supplier shares of total contracted value and is reported on the conventional 0-10,000 scale. Bipartite graphs of buyers and suppliers were constructed to identify recurrent contracting patterns.

### 2.6 Complementary technical-feasibility analysis of a payment workflow using smart contracts

As a clearly secondary module, we implemented a five-state simulator on the Sepolia testnet solely to verify that predefined digital states of a hypothetical payment workflow could be executed in sequence under controlled test conditions. It was not designed as an empirical time-and-motion study; comparison with current practice was made only at the level of temporal order of magnitude, using aggregated institutional references (90-day median; 60-180 day range) rather than a step-by-step operational equivalence between the full hospital workflow and the digital prototype states. The prototype reference scenario of approximately 30 hours should be read only as a test-condition benchmark for the simulator.

The illustrative projected savings were estimated as a scenario exercise, not as an empirical economic evaluation, by applying an average sector financial cost of 2% per month to annual contracted value under a hypothetical scenario of substantial reduction in administrative delays:

$$
Annual\ savings = V_{annual} \times r_{monthly} \times \frac{\Delta t_{days}}{30}
$$

where $V_{annual}$ is approximately COP 3.7 trillion, $r_{monthly} = 2\%$, and $\Delta t$ represents the theoretical reduction in the digital administrative component of the payment cycle.

### 2.7 Statistical analysis

Descriptive statistics were used throughout. Log-normality of contract values was assessed with the Kolmogorov-Smirnov test. Market concentration was described using participation and accumulation indicators. The significance threshold was set at $\alpha = 0.05$.

---

## 3. Results

### 3.1 Characteristics of the data corpus

The characteristics of the corpus and the closed 2020-2025 analytical cohort are summarized in Table 1.

### Table 1. Summary of the public pharmaceutical procurement corpus and the closed analytical cohort used in this manuscript

| Variable | Value |
| --- | --- |
| Total SECOP-II contracts (API universe) | 272,814 |
| Pharmaceutical contracts indexed in PostgreSQL (closed 2020-2025 cohort) | 162,271 |
| Total contracts in recovered local PostgreSQL source | 956,157 |
| Total contracted value (closed pharmaceutical cohort) | COP 17.07 trillion (approx. USD 4.27 billion) |
| Total contracted value (all sectors recovered local source) | COP 294.7 trillion |
| Total contracted value (API universe) | COP 42.00 trillion |
| Mean value per pharmaceutical contract | COP 105 million |
| Unique pharmaceutical suppliers in closed cohort | 50,460 |
| Regions covered | 36-37 |
| Period (closed pharmaceutical cohort) | 2020 to 2025 |
| Platform monitoring window | January 2015 onward |
| Processed INVIMA records | 9,838 (all current) |
| SISMED reference prices | 44,038 records; 1,759 unique ATC codes (2017-2019) |
| Indexed RAG documents | 9,336 |

Pharmaceutical contract value followed a log-normal distribution (Kolmogorov-Smirnov $D = 0.04$; $p < 0.001$). The top 10% of contracts by value accounted for 78% of total contracted value.

**Annual evolution of indexed pharmaceutical contracts (closed cohort, 2020-2025):**

| Year | Contracts | Value (COP billions) |
| --- | --- | --- |
| 2020 | 35,330 | 3,302.6 |
| 2021 | 53,832 | 2,856.7 |
| 2022 | 30,991 | 2,648.4 |
| 2023 | 10,705 | 1,603.1 |
| 2024 | 9,380 | 1,137.5 |
| 2025 | 22,033 | 5,519.3 |

Figure 1 shows the annual evolution of the number of contracts and total contracted value across the closed 2020-2025 cohort. The peak in contract counts in 2021 is consistent with the COVID-19 response period, whereas the value peak in 2025 coincided with increased participation of high-cost oncology procurement. Post-2025 records remain available in the live platform but were excluded from the closed annual comparisons reported here.

The pronounced decline in indexed contracts in 2023-2024 (from 30,991 in 2022 to 10,705 and 9,380, respectively) is reproduced in an independent reconstruction of the public SECOP-II API, which recovers 10,006 and 8,818 pharmaceutical contracts for those years (gaps of only 699 and 562 contracts relative to the manuscript counts). The decline is therefore present in the SECOP-II source under the inclusion taxonomy and is not an artifact of the local PostgreSQL snapshot. The available administrative data do not allow us to adjudicate whether it reflects procurement consolidation into fewer, higher-value contracts, changes in contract-object coding, or an actual reduction in pharmaceutical contracting volume; we therefore treat this pattern as a source-data and classification limitation requiring dedicated validation rather than assigning it a single causal explanation.

**Distribution by therapeutic category:**

| Category | Contracts | Value (COP billions) | Mean value (COP millions) |
| --- | --- | --- | --- |
| General pharmaceutical | 82,303 | 9,990.3 | 121.4 |
| Medical device | 15,943 | 2,957.0 | 185.5 |
| Vaccine | 46,130 | 905.3 | 19.6 |
| Oncology | 403 | 422.8 | 1,049.2 |
| Medical supply | 2,312 | 201.6 | 87.2 |
| Antibiotic | 219 | 21.7 | 98.9 |
| Diabetes | 281 | 20.8 | 74.0 |
| Analgesic | 42 | 8.5 | 203.0 |
| Antiviral | 37 | 0.9 | 24.6 |

Oncology contracts showed the highest mean contract value (COP 1,049.2 million per contract).

### 3.2 Geographic distribution

The leading regions by pharmaceutical procurement value were as follows:

| Region | Contracts | Value (COP billions) | Approx. value (USD millions) | % of total |
| --- | --- | --- | --- | --- |
| Bogota D.C. (SECOP code 1) | 6,223 | 4,877.2 | 1,219.3 | 28.4% |
| Bogota D.C. (SECOP code 2) | 12,093 | 4,788.4 | 1,197.1 | 27.9% |
| Bogota D.C. (combined) | 18,316 | 9,665.6 | 2,416.4 | 56.3% |
| Antioquia | 48,039 | 1,316.2 | 329.1 | 7.7% |
| Valle del Cauca | 5,888 | 706.7 | 176.7 | 4.1% |
| Boyaca | 9,195 | 633.0 | 158.3 | 3.7% |
| Huila | 4,212 | 472.8 | 118.2 | 2.8% |
| Tolima | 3,816 | 431.6 | 107.9 | 2.5% |
| Santander | 4,319 | 418.8 | 104.7 | 2.4% |
| Cauca | 2,023 | 395.6 | 98.9 | 2.3% |
| Atlantico | 5,087 | 351.4 | 87.9 | 2.0% |

Bogota D.C. accounted for 56.3% of national contracted value, equivalent to approximately USD 2.42 billion at the reference exchange rate, followed by Antioquia (7.7%) and Valle del Cauca (4.1%). Figure 2 maps the geographic distribution of total contracted value by department.

**Methodological note.** Bogota D.C. appears under two regional codes in SECOP-II. Coverage of 36-37 regions exceeds the 32 official departments because SECOP-II includes distinct codings for districts and other territorial entities.

### 3.3 Contract-value anomalies detected by the Z-score engine

**Methodological note.** The implemented Z-score engine measures deviation of total contract value relative to the distribution within each therapeutic category. Direct comparison against SISMED unit prices would require structured line-item detail, which is not consistently available in SECOP-II.

Among 147,020 analyzed contracts in categories with at least 10 observations, the engine identified the following:

| Alert level | Criterion | Contracts | % of total |
| --- | --- | --- | --- |
| Critical | Absolute Z-score greater than or equal to 3.0 sigma | 303 | 0.21% |
| High | Absolute Z-score from 2.0 to less than 3.0 sigma | 225 | 0.15% |
| Moderate | Absolute Z-score from 1.5 to less than 2.0 sigma | 157 | 0.11% |
| Total with alert | Absolute Z-score greater than or equal to 1.5 sigma | 685 | 0.47% |

These alerts flag contracts whose total value is atypical within their therapeutic category; they are intended for audit prioritization and do not, by themselves, constitute evidence of corruption, fraud, or unit-price overpricing.

**Results by therapeutic category:**

| Category | Contracts | % with alert | Zmax | Max/mean ratio |
| --- | --- | --- | --- | --- |
| Analgesic | 42 | 9.5% | 4.22 | 9.3x |
| Diabetes | 281 | 8.2% | 6.58 | 15.3x |
| Antiviral | 37 | 5.4% | 4.83 | 14.2x |
| Antibiotic | 219 | 3.7% | 8.32 | 24.1x |
| Medical supply | 2,312 | 2.6% | 22.45 | 86.6x |
| Oncology | 403 | 0.7% | 19.34 | 139.0x |

Antibiotics showed the highest category-level maximum Z-score, whereas analgesics showed the highest proportion of contracts with alerts among the categories displayed in Figure 3.

**Temporal evolution of anomaly rates (2020-2025):**

| Year | Contracts analyzed | Contracts with alert | Rate |
| --- | --- | --- | --- |
| 2020 | 35,326 | 121 | 0.34% |
| 2021 | 53,827 | 165 | 0.31% |
| 2022 | 30,990 | 130 | 0.42% |
| 2023 | 10,705 | 89 | 0.83% |
| 2024 | 9,380 | 86 | 0.92% |
| 2025 | 6,792 | 94 | 1.38% |

The statistical-alert rate increased from 0.31% in 2021 to 1.38% in 2025. Causal interpretation of this pattern requires additional analysis.

**Geographic distribution of anomalies.**

Departments with the highest rates of statistically flagged contracts were Bogota D.C. (3.80%), Norte de Santander (1.92%), Valle del Cauca (1.21%), and Tolima (1.00%). This distribution indicates heterogeneity in contract values, not causal evidence of corruption.

### 3.4 Market concentration

The concentration analysis of Colombian pharmaceutical procurement in the closed analytical cohort showed 50,460 unique supplier names. For value-share concentration metrics, 162,151 positive-value contracts and 50,355 suppliers with non-empty normalized labels were included. The top 10 suppliers concentrated 28.77% of total contracted value and the top 3% of suppliers (1,511 of 50,355) concentrated 85.87%. The leading supplier, VECOL SA, accounted for 5.61% of total value. The HHI was 119.26 on the 0-10,000 scale. The detailed distribution is shown in Figure 4.

This pattern indicates strong cumulative concentration among leading suppliers, while the HHI remains low under conventional market-concentration thresholds because the contracted value is distributed across a large long-tail supplier base. The bipartite graph identified 847 recurrent entity-supplier pairs with at least five consecutive contracts.

### 3.5 Smart-contract payment workflow: complementary technical proof of concept

Tests in the Sepolia-based BigLoI plus Chainlink CRE simulator verified that the prototype could execute predefined transitions between digital states. Figure 5 contrasts the current institutional payment flow with the digital states of the smart-contract prototype. Reported times are investigator-defined reference times used for functional validation of the prototype and do not represent observed measurements of the full real-world logistics and administrative process. SECOP-II was used as a contractual reference point rather than as an operational stage of hospital workflow, and no hospital payment system was instrumented or experimentally compared.

| Functional stage | Prototype time |
| --- | --- |
| Validated contract or enabled order to medicines dispatched | About 24 hours |
| Medicines dispatched to delivery verified | About 4 hours |
| Delivery verified to CRE registered | About 1 hour |
| CRE registered to payment released | About 1 hour |
| Full digital cycle of the prototype | About 30 hours |

The current institutional cycle reported in the literature is 60-180 days (90-day median). This contrast is heuristic and order-of-magnitude only for the digital administrative component; it is not a direct equivalence to the full hospital process, nor evidence that the prototype would reproduce such reductions in practice.

**Illustrative financial-savings scenario.**

Average annual pharmaceutical procurement flow across the closed 2020-2025 cohort was approximately COP 3.4 trillion (about USD 853 million at the reference exchange rate). Under a theoretical scenario of substantial reduction in digital administrative delays, and applying a monthly financial cost of 2% to the avoidable payment-cycle component, projected annual savings were estimated as COP 224,000 million per year (approximately USD 56.0 million). Using 2025 annual flow, the illustrative potential rises to COP 330,000 million per year (approximately USD 82.5 million). These values are scenario outputs only and should not be interpreted as observed savings, budget impact estimates, or implementation-ready business cases.

### 3.6 Complementary modules: machine learning and semantic retrieval

The complementary machine-learning and semantic-retrieval modules showed operational feasibility, but their outputs should be interpreted as exploratory within the scope of this paper.

---

## 4. Discussion

### 4.1 Scale and relevance of the documented problem

The corpus of 162,271 pharmaceutical contracts from 2020 to 2025 represents, to our knowledge, the largest validated closed longitudinal series of public pharmaceutical procurement described for Colombia. The log-normal distribution of contract values, the concentration of 78% of total value in the top decile, and the HHI of 119.26 are consistent with procurement markets characterized by a small group of high-value suppliers and a large long-tail supplier base (14).

The increase in statistical-alert rates from 0.31% in 2021 to 1.38% in 2025 suggests increasing heterogeneity in contracted values during the study period. This pattern warrants dedicated investigation with adjustment for potential confounders such as pharmaceutical inflation and the introduction of new high-cost categories.

### 4.2 Z-scores as a surveillance instrument

The Z-score methodology offers advantages over manual auditing: it operates on the full universe of contracts, is reproducible, and does not require confidential information. Future linkage with SISMED unit prices and item-level disaggregation would likely improve the sensitivity and interpretability of the detector (13,15). The sustained increase in alert rates from 2021 to 2025 supports evaluation of this approach for routine audit workflows.

### 4.3 Smart contracts applied to pharmaceutical payment workflows: interpretation of a complementary proof of concept

The proof of concept supports only a narrow technical claim: conditional digital state transitions can be encoded and executed in a prototype payment workflow under testnet conditions. It does not demonstrate real-world reduction of payment times, lower transaction costs, or institutional deployability. The reported times are not measurements of the full payment process, which also depends on transport, packaging, storage, institutional validation, treasury procedures, contracting rules, and other bottlenecks not modeled here. A defensible operational evaluation would require prospective integration with public hospital information systems, real transaction traces, explicit counterfactual design, and independent technical and regulatory review. Large-scale implementation would additionally require public-treasury integration, legal validation, cybersecurity controls, and external smart-contract auditing.

### 4.4 Contribution to health data governance

Colombia has public data sources that can support pharmaceutical surveillance, but it lacks analytical infrastructure that reliably converts those data into actionable evidence. BigLoI illustrates that such infrastructure can be built using open technologies, reproducible workflows, and auditable queries over a contractual corpus.

### 4.5 Limitations

**SECOP-II data quality.** Buyer and supplier variables include null, generic, or inconsistent values in a meaningful share of contracts in local sample files, which constrains some network analyses. This reflects source-data quality issues in SECOP-II. The closed 2020-2025 cohort included 162,271 pharmaceutical contracts, while the recovered local PostgreSQL source currently indexes 165,549 pharmaceutical records including live 2026 monitoring rows; both reflect the subset with the highest completeness available to the platform.

**SISMED temporal mismatch and granularity.** The openly available SISMED source covers 2017-2019, whereas the main PostgreSQL procurement cohort analyzed here covers 2020 to 2025. Accordingly, SISMED was not used as a contemporaneous contract-by-contract comparator but as contextual market reference. In addition, the SECOP-II source does not provide a fully structured breakdown of line items and unit prices for all contracts, limiting direct validation of unit-price overpricing.

**Blockchain test-network scope.** As detailed in Section 4.3, the payment-workflow validation on Sepolia was a functional test of digital state transitions only: prototype times are referential, the savings scenario is not an economic evaluation, and the prototype was not tested against live institutional payment data. Mainnet implementation would require independent smart-contract auditing, regulatory validation, public-treasury integration, and cybersecurity review.

**Selection bias in pharmaceutical filtering.** Use of 19 inclusion keywords may generate false negatives and false positives. A dedicated taxonomy-validation study would be needed to quantify classification performance.

**Interpretive scope.** The observational design identifies statistical patterns but does not establish causal relationships or measure clinical impact. Interpreting flagged contracts as evidence of corruption would require additional causal methods and involvement of competent institutions.

### 4.6 Implications for public policy

These findings contribute to three policy discussions: health-system reform, procurement transparency, and health-data governance. The principal contribution of the study is methodological and reproducible: an open infrastructure capable of transforming dispersed public data into auditable evidence. Concentration and recurrence indicators may support audit prioritization, while uneven SECOP-II data quality deserves institutional attention from Colombia Compra Eficiente.

---

## 5. Conclusions

This study describes BigLoI, a national-scale computational pharmaceutical-surveillance platform that monitors SECOP-II contracts from 2015 onward and empirically analyzes a closed indexed cohort of 162,271 pharmaceutical contracts from 2020 to 2025. Three main findings emerge.

1. **Market concentration.** The top 3% of suppliers concentrated 85.87% of total contracted value, the top 10 suppliers concentrated 28.77%, and the HHI was 119.26 on the 0-10,000 scale.

2. **Atypical statistical patterns.** A total of 685 contracts triggered Z-score alerts with absolute Z-score greater than or equal to 1.5 sigma, antibiotics showed Zmax of 8.32, and the alert rate increased from 0.31% in 2021 to 1.38% in 2025.

3. **Reproducible infrastructure.** Integration of relational data storage, reproducible analytics, and a public observatory makes it possible to convert dispersed public sources into an auditable surveillance instrument for pharmaceutical procurement.

As a complementary result, the Sepolia prototype shows that conditional payment logic can be represented and executed in a controlled testnet environment. Any inference about reduced payment delays or financial savings remains hypothetical and dependent on assumptions that were not empirically validated in this study. This line of work therefore remains exploratory and still requires operational, regulatory, technical, and logistical validation.

Overall, BigLoI provides evidence that an open and reproducible surveillance infrastructure can generate useful findings on market concentration, statistical anomalies, and auditable evidence access from public administrative data on Colombian pharmaceutical procurement.

---

## Author contributions

Andres Soto: study conception and design; platform development; data acquisition, processing, and analysis; manuscript writing.

---

## Funding

This study was fully funded with the author's own resources. No external funding was received.

---

## Competing interests

The author declares no competing interests.

---

## Data and code availability

- **Article reproducibility package:** Archived in Zenodo with DOI <https://doi.org/10.5281/zenodo.19074137> and available in GitHub at <https://github.com/zswamtech/BigLoI-PLOS-ONE-paper>.
- **Extended BigLoI platform source code:** Available in GitHub at <https://github.com/zswamtech/BigLoI-PMV>.
- **SECOP-II, INVIMA, and SISMED data:** Available through datos.gov.co.
- **Author ORCID:** <https://orcid.org/0009-0004-8001-5372>.
- **BigLoI National Medicines Observatory:** The public observatory is undergoing editorial finalization, and its URL will be provided once stable production deployment is restored.

---

## References

1. Departamento Nacional de Planeacion. Sistema Electronico de Contratacion Publica SECOP-II: estadisticas de uso 2015-2026. Bogota: Departamento Nacional de Planeacion; 2026.

2. World Health Organization. Everybody's business: strengthening health systems to improve health outcomes: WHO's framework for action. Geneva: World Health Organization; 2007.

3. Contraloria General de la Republica de Colombia. Informe de auditoria al sistema de contratacion farmaceutica publica 2023. Bogota: Contraloria General de la Republica de Colombia; 2024.

4. Ministerio de Salud y Proteccion Social. SISMED: boletin de precios de medicamentos. Bogota: Ministerio de Salud y Proteccion Social; 2025.

5. Defensoria del Pueblo de Colombia. Informe sobre desabastecimiento de medicamentos en el Eje Cafetero 2025. Bogota: Defensoria del Pueblo de Colombia; 2025.

6. Transparency International. Monitoring the pharmaceutical sector: a practical guide. Berlin: Transparency International; 2016.

7. Kuo TT, Kim HE, Ohno-Machado L. Blockchain distributed ledger technologies for biomedical and health care applications. J Am Med Inform Assoc. 2017;24(6):1211-20. doi:10.1093/jamia/ocx068.

8. Lewis P, Perez E, Piktus A, Petroni F, Karpukhin V, Goyal N, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. Adv Neural Inf Process Syst. 2020;33:9459-74.

9. Habershon S, Habershon C. ProZorro: how Ukraine's e-procurement system is fighting corruption. OECD Observer. 2019;(318):23-4.

10. Open Contracting Partnership. Open Contracting Data Standard [Internet]. Washington (DC): Open Contracting Partnership; 2023 [accessed 2026 Mar 16]. Available from: <https://standard.open-contracting.org/latest/en/>.

11. European Anti-Fraud Office. The OLAF report 2023 [Internet]. Brussels: European Commission; 2024 [accessed 2026 Mar 16]. Available from: <https://ec.europa.eu/olaf-report/2023/index_en.html>.

12. Ferraz C, Finan F. Exposing corrupt politicians: the effects of Brazil's publicly released audits on electoral outcomes. Q J Econ. 2008;123(2):703-45.

13. Kanavos P, Vogler S. Pharmaceutical market monitoring, policies and pharmaceutical pricing. Geneva: World Health Organization; 2019.

14. Fazekas M, Toth IJ, King LP. An objective corruption risk index using public procurement data. Eur J Crim Policy Res. 2016;22(3):369-97.

15. Management Sciences for Health. MDS-3: managing access to medicines and health technologies. Arlington (VA): Management Sciences for Health; 2012.

16. Vasquez MA, Sanchez C. Analisis de concentracion en el mercado de medicamentos en Colombia. Rev Salud Publica. 2020;22(1):e185177.

---

## Figure legends

**Figure 1.** Annual evolution of public pharmaceutical procurement monitored in SECOP-II (closed cohort, 2020-2025): number of contracts and total contracted value.

**Figure 2.** Geographic distribution of total value in public pharmaceutical procurement monitored in SECOP-II by department (closed cohort, 2020-2025).

**Figure 3.** Distribution of statistical contract-value anomalies detected by the Z-score engine, by therapeutic category and year (2020-2025).

**Figure 4.** Market concentration in public pharmaceutical procurement monitored in SECOP-II (closed cohort, 2020-2025): Lorenz curve and top 10 suppliers.

**Figure 5.** Conceptual scheme of the pharmaceutical payment workflow: current institutional flow versus digital states of the smart-contract prototype.

**Figure 6.** Simplified technical architecture of the BigLoI platform: seven layers for processing public pharmaceutical data.

**Table 1.** Summary of the corpus of public pharmaceutical procurement monitored in SECOP-II.

**Table 2.** Technical architecture of the BigLoI platform for surveillance of public pharmaceutical procurement.

---

## Supporting information

**S1 Table. Approximate COP/USD equivalents for the principal monetary values reported in the manuscript.** Conversions use a single round reference exchange rate of COP 4,000 per USD and are provided only as approximate interpretive aids; no analyses were performed in USD.

---

## Appendices

### Appendix 1. SECOP-II pharmaceutical filtering taxonomy

**Inclusion terms (19):** medicamento, farmaceutico, farmacia, antibiotico, vacuna, insulina, quimioterapia, dispositivos medicos, insumo medico, suministro medico, biologico, antiviral, analgesico, anestesia, oncologico, hemodialisis, hormonal, anticoagulante, inmunosupresor.

**Exclusion terms (5):** obra civil, construccion, mantenimiento, tecnologia de informacion, mobiliario.

### Appendix 2. Simplified database schema

Main tables: observatorio_nacional.contratos_secop (956,157 total records in the recovered local snapshot; 165,549 pharmaceutical records currently indexed, of which 162,271 belong to the closed 2020-2025 cohort); observatorio_nacional.sismed_precios_referencia (44,038 records; 1,759 unique ATC codes; years 2017-2019); observatorio_nacional.invima_medicamentos (9,838 current records); puntos_autorizados (101 hospitals); medicamentos (approximately 10,000 form records); sim_hospitales_100 (100 simulated hospitals).

### Appendix 3. Smart-contract protocol

Smart contracts: InvoiceRegistry.sol, InvoiceNFT.sol, and PaymentEscrow.sol; network: Ethereum Sepolia testnet; oracle layer: Chainlink CRE; invoice NFTs used for invoice traceability; escrow module used for conditional payment release.
