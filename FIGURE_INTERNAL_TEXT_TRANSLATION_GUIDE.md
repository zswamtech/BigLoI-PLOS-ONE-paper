# Figure Internal Text Translation Guide

This guide defines the exact English replacements for internal text embedded in Figures 1-6 of the PLOS ONE submission package. It is intended for rebuilding the master figures without ad hoc wording changes.

## Scope

- Applies to internal figure text only: panel titles, axis labels, legends, annotations, callout boxes, headers, and embedded notes.
- Does not replace the already translated main manuscript or figure legends.
- Use title case for figure and panel headers.
- Use sentence case for explanatory notes and callout text.
- Keep abbreviations already used in the manuscript: COP, Z-score, RAG, API, TF-IDF, PCA.
- Keep decimal punctuation in English style inside figures: `56.3%`, not `56,3%`.
- Keep thousands separators in English style inside figures when manually typesetting text.

## Figure 1

Working title in source:

- Spanish: `Evolución anual de la contratación farmacéutica pública en Colombia (cohorte cerrada 2020–2025): número de contratos y valor total`
- English: `Annual Evolution of Public Pharmaceutical Procurement in Colombia (Closed Cohort, 2020-2025): Number of Contracts and Total Value`

Internal text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `A. Número de contratos firmados por año (vigencias del cohorte cerrado)` | `A. Number of Contracts Signed per Year (Closed Cohort Fiscal Years)` |
| `Contratos` | `Contracts` |
| `Pico 2021: respuesta COVID-19 (vacunas + equipos hospitalarios)` | `2021 peak: COVID-19 response (vaccines + hospital equipment)` |
| `B. Valor total contratado por año (billones COP)` | `B. Total Contracted Value per Year (COP trillions)` |
| `Valor (B COP)` | `Value (COP trillions)` |
| `Pico valor 2025: $5,52 B COP (oncológicos alto costo + reactivación posreforma)` | `2025 value peak: COP 5.52 trillion (high-cost oncology products + post-reform reactivation)` |

Operational notes:

- If the chart retains short numeric axis formatting, use `k` for thousands and `COP T` only if space is too constrained; otherwise prefer `COP trillions`.
- Replace `BD` with `Database`; do not leave the Spanish abbreviation.

## Figure 2

Working title in source:

- Spanish: `Distribución geográfica del valor de contratación farmacéutica pública por departamento — cohorte cerrada Colombia 2020–2025 (top 9 de 36)`
- English: `Geographic Distribution of Public Pharmaceutical Procurement Value by Department, Colombia (Closed Cohort, 2020-2025; Top 9 of 36)`

Internal text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `Valor (MM COP)` | `Value (COP billions)` |
| `Participación en el valor total nacional` | `Share of Total National Value` |
| `Bogotá D.C. concentra el 56,3% del valor. Los 9 departamentos mostrados = 90,8% del total nacional.` | `Bogota, D.C. accounts for 56.3% of total value. The 9 departments shown represent 90.8% of the national total.` |

Department labels:

- Keep official proper names in Spanish where they are geographic names, except normalize typography if needed for English layout.
- Use `Bogota, D.C.` in figure text for typographic simplicity if the master is already accent-free; if accents are retained consistently across all labels, `Bogotá, D.C.` is acceptable.

Operational notes:

- `MM COP` in the current figure visually means thousands of millions of COP. For an English-language scientific figure, `COP billions` is the clearest replacement.
- Do not translate department proper names such as `Antioquia`, `Valle del Cauca`, or `Cundinamarca`.

## Figure 3

Working title in source:

- Spanish: `Distribución de anomalías estadísticas de valor detectadas por el motor Z-score, por categoría terapéutica — Colombia 2020–2025`
- English: `Distribution of Statistical Value Anomalies Detected by the Z-score Engine, by Therapeutic Category, Colombia 2020-2025`

Internal text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `A. Porcentaje de contratos con alerta estadística (\|Z\|≥1,5σ) por categoría` | `A. Percentage of Contracts with Statistical Alert (\|Z\| >= 1.5 sigma) by Category` |
| `% con alerta` | `% with alert` |
| `B. Evolución anual de la tasa de alertas (% contratos con \|Z\|≥1,5σ)` | `B. Annual Evolution of the Alert Rate (% of Contracts with \|Z\| >= 1.5 sigma)` |
| `Tasa alertas (%)` | `Alert rate (%)` |
| `Incremento +345% (2021→2025): de 0,31% a 1,38%` | `Increase +345% (2021 to 2025): from 0.31% to 1.38%` |
| `Hallazgos destacados:` | `Key findings:` |
| `Antibióticos: Z_max = 8,32σ (valor máximo 24× la media de categoría)` | `Antibiotics: Z_max = 8.32 sigma (maximum value 24x the category mean)` |
| `Diabetes: mayor proporción con alerta (8,2%)` | `Diabetes: highest proportion with alert (8.2%)` |
| `Oncológicos: Z_max = 19,34σ (ratio 139× la media) — alta varianza intrínseca en biológicos de alto costo` | `Oncology: Z_max = 19.34 sigma (139x the mean) - high intrinsic variance in high-cost biologics` |
| `307 contratos en nivel CRÍTICO (\|Z\|≥3,0σ)` | `307 contracts at CRITICAL level (\|Z\| >= 3.0 sigma)` |

Category labels to standardize in English:

| Spanish category label | Approved English label |
| --- | --- |
| `Antibióticos` | `Antibiotics` |
| `Diabetes` | `Diabetes` |
| `Oncológicos` | `Oncology` |
| `Analgésicos` or `Analgesicos` | `Analgesics` |
| `Cardiovasculares` | `Cardiovascular` |
| `Vacunas` | `Vaccines` |
| `Dispositivos` | `Medical devices` |

Operational notes:

- Prefer `sigma` instead of the Greek symbol only if font rendering becomes inconsistent; otherwise the current sigma symbol can be retained.
- Keep `CRITICAL` in all caps only if the master currently uses emphasis in all caps.

## Figure 4

Working title in source:

- Spanish: `Concentración de mercado en la contratación farmacéutica pública colombiana (cohorte cerrada 2020–2025): curva de Lorenz y top 10 proveedores`
- English: `Market Concentration in Colombian Public Pharmaceutical Procurement (Closed Cohort, 2020-2025): Lorenz Curve and Top 10 Suppliers`

Internal text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `Curva de Lorenz — concentración del valor contratado (escala log en eje X)` | `Lorenz Curve - Concentration of Contracted Value (Log Scale on X-axis)` |
| `Top 10 = 28,7%` or figure-specific value | `Top 10 = 28.7%` |
| `Top 3% = 85,9%` | `Top 3% = 85.9%` |
| `% acumulado de proveedores (escala logarítmica)` | `Cumulative % of Suppliers (Log Scale)` |
| `% acumulado del valor` | `Cumulative % of Value` |
| `Top 10 proveedores por valor total contratado — participación individual y acumulada` | `Top 10 Suppliers by Total Contracted Value - Individual and Cumulative Share` |
| `% del valor total` | `% of total value` |
| `50.577 proveedores activos · top 3% (1.518 proveedores) = 85,9% del valor total · IHH estimado: mercado oligopolístico` | `50,577 active suppliers - top 3% (1,518 suppliers) = 85.9% of total value - estimated HHI: oligopolistic market` |

Operational notes:

- Replace `IHH` with `HHI`, which is the English acronym for Herfindahl-Hirschman Index.
- Keep supplier names unchanged; they are proper legal names.
- Use hyphen `-` or en dash consistently, but avoid mixed punctuation inside the same figure.

## Figure 5

Working title in source:

- Spanish: `Esquema conceptual del ciclo de pago farmacéutico: flujo actual institucional versus estados digitales del prototipo (prueba de concepto en red Sepolia)`
- English: `Conceptual Diagram of the Pharmaceutical Payment Cycle: Current Institutional Workflow versus Prototype Digital States (Proof of Concept on the Sepolia Network)`

Header and explanatory text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `Comparación referencial entre ciclo actual documentado y prototipo digital BigLoI` | `Reference Comparison between the Documented Current Cycle and the BigLoI Digital Prototype` |
| `La columna izquierda integra evidencia operativa local del abastecimiento farmaceutico y un tramo administrativo-financiero general; la derecha muestra estados digitales del prototipo.` | `The left column combines local operational evidence from pharmaceutical supply management with a general administrative-financial segment; the right column shows prototype digital states.` |
| `FLUJO ACTUAL INSTITUCIONAL` | `CURRENT INSTITUTIONAL WORKFLOW` |
| `evidencia local + tramo financiero general` | `local evidence + general financial segment` |
| `ESTADOS DIGITALES DEL PROTOTIPO` | `PROTOTYPE DIGITAL STATES` |
| `~30 horas referenciales` | `~30 reference hours` |
| `Ciclo actual agregado: mediana 90 días` | `Current aggregated cycle: median 90 days` |
| `Total digital referencial del prototipo: ~30 horas` | `Prototype reference digital total: ~30 hours` |
| `Ahorro financiero proyectado: $224.000 – $330.000 millones COP/año` | `Projected financial savings: COP 224-330 billion/year` |
| `Escenario teórico: costo financiero 2% mensual × flujo anual $3,7 billones COP` | `Theoretical scenario: 2% monthly financing cost x annual flow of COP 3.7 trillion` |
| `× reducción referencial del ciclo administrativo digital de 90 días a ~30 horas` | `x reference reduction of the digital administrative cycle from 90 days to ~30 hours` |

Step labels and node text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `Necesidad institucional` | `Institutional need` |
| `Pedido / orden` | `Order / request` |
| `Abastecimiento` | `Supply` |
| `Recepcion y registro` | `Receipt and registration` |
| `Revision documental` | `Document review` |
| `Tesoreria y pago` | `Treasury and payment` |
| `Solicitud interna y validacion` | `Internal request and validation` |
| `Purchase request / validation` | `Purchase request / validation` |
| `Cotizacion y orden de compra` | `Quotation and purchase order` |
| `Smart quote / purchase order` | `Smart quote / purchase order` |
| `Despacho del proveedor` | `Supplier dispatch` |
| `Dispatch confirmed` | `Dispatch confirmed` |
| `Recepcion tecnica y registro` | `Technical receipt and registration` |
| `Verified delivery ~4 hours` | `Verified delivery ~4 hours` |
| `Radicacion, revision y causacion` | `Invoice filing, review, and accrual` |
| `CRE / factura digital ~1 hora` | `CRE / digital invoice ~1 hour` |
| `Tesoreria y giro final` | `Treasury and final payment` |
| `Pago liberado ~1 hora` | `Payment released ~1 hour` |

Operational notes:

- Some node labels may already exist in partially English form in the source array; keep the approved wording above for the rebuilt master so both columns follow one style.
- Use `workflow` rather than `flow` in English headers.
- Do not portray the right column as an observed real-world hospital timeline; keep `reference` wording.

## Figure 6

Working title in source:

- Spanish: `Arquitectura técnica simplificada de la plataforma BigLoI: siete capas de procesamiento de datos farmacéuticos públicos`
- English: `Simplified Technical Architecture of the BigLoI Platform: Seven Layers of Public Pharmaceutical Data Processing`

Internal text replacements:

| Spanish source/master text | Approved English replacement |
| --- | --- |
| `CAPAS DE LA PLATAFORMA (flujo de datos: capa 1 → capa 7)` | `PLATFORM LAYERS (data flow: layer 1 -> layer 7)` |
| `Visualización` | `Visualization` |
| `React / TypeScript · Observatorio público · Series temporales · Mapas · Alertas` | `React / TypeScript - Public observatory - Time series - Maps - Alerts` |
| `Contratos inteligentes` | `Smart contracts` |
| `Solidity · Chainlink CRE · Sepolia · PaymentEscrow.sol · InvoiceNFT.sol` | `Solidity - Chainlink CRE - Sepolia - PaymentEscrow.sol - InvoiceNFT.sol` |
| `Aprendizaje automático` | `Machine learning` |
| `scikit-learn · Predicción demanda (R²>0.85) · k-means 6 grupos · PCA` | `scikit-learn - Demand prediction (R^2 > 0.85) - k-means (6 clusters) - PCA` |
| `IA generativa (RAG)` | `Generative AI (RAG)` |
| `Claude 3.5 Sonnet · GPT-4o · Pinecone (9.336 docs) · Búsqueda semántica + TF-IDF` | `Claude 3.5 Sonnet - GPT-4o - Pinecone (9,336 docs) - Semantic search + TF-IDF` |
| `Procesamiento / API` | `Processing / API` |
| `FastAPI · Python · pandas · Limpieza · Clasificación · Motor Z-score` | `FastAPI - Python - pandas - Cleaning - Classification - Z-score engine` |
| `Almacenamiento` | `Storage` |
| `PostgreSQL (339K contratos) · Pinecone (vectorial) · MongoDB (no estructurado)` | `PostgreSQL (339K contracts) - Pinecone (vector) - MongoDB (unstructured)` |
| `Recolección de datos` | `Data collection` |
| `API Socrata · SECOP-II · INVIMA · SISMED · datos.gov.co · Ingesta incremental` | `Socrata API - SECOP-II - INVIMA - SISMED - datos.gov.co - Incremental ingestion` |

Operational notes:

- Use `R^2` if the font or export workflow does not preserve superscripts reliably.
- `Vector` is preferable to `vectorial` in English.
- `Public observatory` is the correct replacement for `Observatorio público`; do not use `public observer`.

## Cross-Figure Consistency Rules

- Use `Z-score` consistently with a hyphen.
- Use `suppliers`, not `providers`, for market-concentration figures unless a legal entity label specifically requires `provider`.
- Use `contracted value` for procurement totals and `total value` for summary bars or shares where space is limited.
- Use `Bogota, D.C.` or `Bogotá, D.C.` consistently across all assets; do not mix both.
- Keep `COP` as the currency code; do not alternate with `Col$` or `$COP` inside the same figure set.

## Master Rebuild Sequence

1. Replace all Spanish text in the editable master source for each figure.
2. Export updated English masters as PNG for visual QA.
3. Verify that decimal punctuation, acronym usage, and title case are consistent across the six figures.
4. Export final TIFF submission files from the corrected English masters.
5. Recheck that figure legends in the manuscript still match the final panel wording.
