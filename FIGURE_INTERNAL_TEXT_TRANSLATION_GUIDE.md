# Figure Internal Text Specification

This document defines the approved English wording for the internal text embedded in Figures 1-6 of the PLOS ONE submission package. It is the canonical reference for rebuilding the master figures without introducing wording drift.

## General Rules

- Use title case for figure and panel headers.
- Use sentence case for explanatory notes and callouts.
- Keep abbreviations already used in the manuscript: COP, Z-score, RAG, API, TF-IDF, PCA, HHI.
- Use English decimal punctuation inside figures: `56.3%`, not `56,3%`.
- Keep thousands separators in English style when manually typesetting text.
- Use `Bogota, D.C.` consistently across figure assets.

## Figure 1

Approved wording:

- `Annual Evolution of Public Pharmaceutical Procurement in Colombia (Closed Cohort, 2020-2025): Number of Contracts and Total Value`
- `A. Number of Contracts Signed per Year (Closed Cohort Fiscal Years)`
- `Contracts`
- `2021 peak: COVID-19 response (vaccines + hospital equipment)`
- `B. Total Contracted Value per Year (COP trillions)`
- `Value (COP trillions)`
- `2025 value peak: COP 5.52 trillion (high-cost oncology products + post-reform reactivation)`

## Figure 2

Approved wording:

- `Geographic Distribution of Public Pharmaceutical Procurement Value by Department, Colombia (Closed Cohort, 2020-2025; Top 9 of 36)`
- `Value (COP billions)`
- `Share of Total National Value`
- `Bogota, D.C. accounts for 56.3% of total value. The 9 departments shown represent 90.8% of the national total.`

Department labels remain in their official geographic names.

## Figure 3

Approved wording:

- `Distribution of Statistical Value Anomalies Detected by the Z-score Engine, by Therapeutic Category, Colombia 2020-2025`
- `A. Percentage of Contracts with Statistical Alert (|Z| >= 1.5 sigma) by Category`
- `% with alert`
- `B. Annual Evolution of the Alert Rate (% of Contracts with |Z| >= 1.5 sigma)`
- `Alert rate (%)`
- `Increase +345% (2021 to 2025): from 0.31% to 1.38%`
- `Key findings:`
- `Antibiotics: Z_max = 8.32 sigma (maximum value 24x the category mean)`
- `Diabetes: highest proportion with alert (8.2%)`
- `Oncology: Z_max = 19.34 sigma (139x the mean) - high intrinsic variance in high-cost biologics`
- `307 contracts at CRITICAL level (|Z| >= 3.0 sigma)`

Category labels:

- `Antibiotics`
- `Diabetes`
- `Oncology`
- `Analgesics`
- `Cardiovascular`
- `Vaccines`
- `Medical devices`

## Figure 4

Approved wording:

- `Market Concentration in Colombian Public Pharmaceutical Procurement (Closed Cohort, 2020-2025): Lorenz Curve and Top 10 Suppliers`
- `Lorenz Curve - Concentration of Contracted Value (Log Scale on X-axis)`
- `Top 10 = 28.7%`
- `Top 3% = 85.9%`
- `Cumulative % of Suppliers (Log Scale)`
- `Cumulative % of Value`
- `Top 10 Suppliers by Total Contracted Value - Individual and Cumulative Share`
- `% of total value`
- `50,577 active suppliers - top 3% (1,518 suppliers) = 85.9% of total value - estimated HHI: oligopolistic market`

Use `HHI` consistently in figure text.

## Figure 5

Approved wording:

- `Conceptual Diagram of the Pharmaceutical Payment Cycle: Current Institutional Workflow versus Prototype Digital States (Proof of Concept on the Sepolia Network)`
- `Reference Comparison between the Documented Current Cycle and the BigLoI Digital Prototype`
- `The left column combines local operational evidence from pharmaceutical supply management with a general administrative-financial segment; the right column shows prototype digital states.`
- `CURRENT INSTITUTIONAL WORKFLOW`
- `local evidence + general financial segment`
- `PROTOTYPE DIGITAL STATES`
- `~30 reference hours`
- `Current aggregated cycle: median 90 days`
- `Prototype reference digital total: ~30 hours`
- `Projected financial savings: COP 224-330 billion/year`
- `Theoretical scenario: 2% monthly financing cost x annual flow of COP 3.7 trillion`
- `x reference reduction of the digital administrative cycle from 90 days to ~30 hours`
- `Institutional need`
- `Order / request`
- `Supply`
- `Receipt and registration`
- `Document review`
- `Treasury and payment`
- `Internal request and validation`
- `Purchase request / validation`
- `Quotation and purchase order`
- `Smart quote / purchase order`
- `Supplier dispatch`
- `Dispatch confirmed`
- `Technical receipt and registration`
- `Verified delivery ~4 hours`
- `Invoice filing, review, and accrual`
- `CRE / digital invoice ~1 hour`
- `Treasury and final payment`
- `Payment released ~1 hour`

## Figure 6

Approved wording:

- `Simplified Technical Architecture of the BigLoI Platform: Seven Layers of Public Pharmaceutical Data Processing`
- `PLATFORM LAYERS (data flow: layer 1 -> layer 7)`
- `Visualization`
- `React / TypeScript - Public observatory - Time series - Maps - Alerts`
- `Smart contracts`
- `Solidity - Chainlink CRE - Sepolia - PaymentEscrow.sol - InvoiceNFT.sol`
- `Machine learning`
- `scikit-learn - Demand prediction (R^2 > 0.85) - k-means (6 clusters) - PCA`
- `Generative AI (RAG)`
- `Claude 3.5 Sonnet - GPT-4o - Pinecone (9,336 docs) - Semantic search + TF-IDF`
- `Processing / API`
- `FastAPI - Python - pandas - Cleaning - Classification - Z-score engine`
- `Storage`
- `PostgreSQL (339K contracts) - Pinecone (vector) - MongoDB (unstructured)`
- `Data collection`
- `Socrata API - SECOP-II - INVIMA - SISMED - datos.gov.co - Incremental ingestion`

## Cross-Figure Consistency

- Use `Z-score` consistently with a hyphen.
- Use `suppliers`, not `providers`, for market-concentration figures.
- Use `contracted value` for procurement totals and `total value` for summary bars or shares where space is limited.
- Keep `COP` as the currency code; do not alternate with `Col$` or `$COP` inside the same figure set.
- Keep punctuation and capitalization aligned across the six figures.

## Rebuild Order

1. Replace all figure text with the approved English wording above.
2. Export updated master figures as PNG for QA.
3. Verify decimal punctuation, acronym usage, and title case consistency.
4. Export final TIFF submission files from the corrected masters.
5. Recheck that manuscript figure legends match the final panel wording.
