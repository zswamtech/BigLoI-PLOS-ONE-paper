# Computational surveillance of Colombian public pharmaceutical procurement using public administrative data: a reproducible analysis of 2020–2026 contracts

Andres Soto  
Independent researcher  
Bogota, Colombia  
ORCID: 0009-0004-8001-5372  
Correspondence: <ansoto1604@icloud.com>

---

## RESUMEN

**Introducción.** La contratación farmacéutica pública en Colombia acumuló $42 billones de pesos en 272.814 contratos monitoreados en SECOP-II entre enero de 2015 y marzo de 2026; dentro de ese universo, la cohorte analítica principal 2020 a marzo de 2026 carecía de una infraestructura reproducible para vigilancia sistemática en tiempo real.

**Objetivo.** Describir el diseño, implementación y hallazgos de una infraestructura computacional reproducible para vigilancia de la contratación farmacéutica pública colombiana.

**Métodos.** Se consumieron las API públicas de SECOP-II, INVIMA y SISMED y se integraron en una arquitectura reproducible con PostgreSQL, analítica estadística y observatorio web. Se implementó un motor Z-score para detectar contratos con valores contractuales atípicos por categoría terapéutica y se evaluó, de forma complementaria, la automatización del ciclo de pago en red Sepolia. La base incluyó 162.921 contratos farmacéuticos, 9.838 registros INVIMA y 44.038 precios SISMED (1.759 ATC).

**Resultados.** De 147.670 contratos analizados, 690 (0,47%) presentaron alerta estadística (|Z|≥1,5σ); la tasa creció de 0,31% (2021) a 1,38% (2025). La categoría antibióticos presentó el mayor Z-score (8,32). El 3% de proveedores concentra el 85,9% del valor total contratado. En el módulo complementario de automatización, la prueba de concepto confirmó viabilidad funcional de los estados digitales del proceso con un ciclo digital referencial del prototipo de ~30 horas y permitió estimar un ahorro potencial de $224.000-330.000 millones COP/año bajo un escenario de reducción sustancial de demoras administrativas.

**Conclusiones.** Una infraestructura computacional reproducible para vigilancia farmacéutica pública a escala nacional permitió identificar patrones atípicos y documentar alta concentración de mercado en la contratación farmacéutica colombiana. Los hallazgos son relevantes para auditoría, política de salud y gobernanza de datos; la automatización blockchain debe interpretarse como una prueba funcional de concepto complementaria, no como una medición operativa del proceso real.

**Palabras clave:** contratación farmacéutica pública; SECOP-II; corrupción en salud; inteligencia artificial; blockchain; SISMED; INVIMA; anomalías de precio; Colombia; transparencia; salud pública.

---

## ABSTRACT *(English)*

**Introduction.** Colombian pharmaceutical public procurement accumulated COP $42 trillion across 272,814 contracts monitored in SECOP-II between January 2015 and March 2026; within that universe, the main analytical cohort from 2020 to March 2026 lacked a reproducible infrastructure for systematic real-time surveillance.

**Objective.** To describe the design, implementation, and findings of a reproducible computational infrastructure for surveillance of Colombian public pharmaceutical procurement.

**Methods.** Public APIs from SECOP-II, INVIMA, and SISMED were consumed and integrated into a reproducible architecture combining PostgreSQL, statistical analytics, and a public-facing observatory. A Z-score engine was implemented to detect contracts with atypical total values within their therapeutic category. Smart contract automation of the payment cycle was evaluated as a complementary module on the Sepolia testnet. The database contains 162,921 pharmaceutical contracts, 9,838 INVIMA records, and 44,038 SISMED reference prices (1,759 ATC codes).

**Results.** Analysis of 147,670 contracts identified 690 with statistical alerts (|Z| ≥ 1.5σ); alert rate grew from 0.31% (2021) to 1.38% (2025). Antibiotics showed the highest Z-score (Z=8.32). The top 3% of suppliers concentrate 85.9% of total contracted value. In the complementary automation module, the proof of concept confirmed functional feasibility of digital state transitions with a referential prototype cycle of ~30 hours and supported a projected savings scenario of COP $224,000-330,000 million under substantial reduction of administrative delays.

**Conclusions.** A national-scale reproducible computational infrastructure identified statistically atypical procurement patterns and documented marked market concentration in Colombian public pharmaceutical procurement. Findings provide evidence-based inputs for public health policy, institutional auditing, and health data governance; blockchain automation should be interpreted as a complementary functional proof of concept rather than an operational measurement of the real-world process.

**Keywords:** public pharmaceutical procurement; SECOP-II; health corruption; artificial intelligence; blockchain; SISMED; INVIMA; price anomalies; Colombia; transparency; public health.

---

## 1. INTRODUCCIÓN

La contratación pública de medicamentos en Colombia acumuló más de $42 billones de pesos en 272.814 contratos monitoreados en SECOP-II entre enero de 2015 y marzo de 2026; dentro de ese universo, la cohorte analítica principal indexada corresponde a 162.921 contratos farmacéuticos de 2020 a marzo de 2026. En ese período se registraron 163.135 proveedores distribuidos en todo el país (1). A pesar de esta escala, el sistema carece de herramientas de vigilancia estadística en tiempo real para detectar anomalías, concentración de mercado o riesgos de desabastecimiento.

La Organización Mundial de la Salud estima que entre el 10% y el 25% del gasto global en salud se pierde por corrupción, ineficiencia y errores administrativos (2). En Colombia, auditorías oficiales han documentado sobreprecios en medicamentos de alto costo, retrasos prolongados en pagos y episodios recurrentes de desabastecimiento (3,4).

La integración de APIs públicas permite construir plataformas de vigilancia sin acceso a información confidencial. El análisis Z-score es una metodología útil para identificar patrones atípicos en contratación pública a escala (6); los contratos inteligentes y la búsqueda semántica amplían el horizonte de automatización y acceso a la evidencia (7,8). Experiencias como ProZorro, OCDS y OLAF muestran la viabilidad de estos enfoques en transparencia contractual (9-11).

BigLoI (*Business Intelligence for Government Logistics and Operations Intelligence*) fue desarrollado para abordar esta brecha. Este artículo documenta su metodología y hallazgos como aporte al debate sobre herramientas tecnológicas para la gobernanza del sistema de salud colombiano.

---

## 2. MÉTODOS

### 2.1 Diseño del estudio

Estudio de desarrollo tecnológico con análisis observacional longitudinal de datos de contratación pública. Se utilizaron exclusivamente fuentes públicas colombianas de acceso libre. No se emplearon datos clínicos ni personales de pacientes. Según la Resolución 8430 de 1993, el estudio se clasifica como **investigación sin riesgo**.

### 2.2 Fuentes de datos

**SECOP-II (Sistema Electrónico de Contratación Pública):**
Se consumió la API pública Socrata del portal datos.gov.co para la descarga automatizada de contratos farmacéuticos. El criterio de inclusión fue la presencia de al menos uno de 19 términos farmacéuticos en la descripción del objeto contractual. Se excluyeron falsos positivos evidentes. El período de análisis comprende **enero de 2015 a marzo de 2026**.

**Universo SECOP-II:** 272.814 contratos únicos · $42 billones COP · 163.135 proveedores · 37 regiones
**Base indexada en PostgreSQL:** 162.921 contratos farmacéuticos · 339.031 contratos totales en BD

**INVIMA (Instituto Nacional de Vigilancia de Medicamentos y Alimentos):**
Se descargaron 9.838 registros del Registro Sanitario Nacional mediante la API Socrata. Se incluyeron nombre comercial, principio activo, laboratorio titular, registro sanitario, código ATC, forma farmacéutica, vía de administración, fechas y estado del registro. Todos los registros cargados correspondieron a estado **Vigente**.

**SISMED (Sistema de Información de Precios de Medicamentos — MinSalud):**
Se procesaron **44.038 registros de precios de referencia** correspondientes a **1.759 códigos ATC únicos**, agregados por forma farmacéutica, canal de distribución y año de corte (**2017–2019**). Estos datos se emplearon como referencia contextual del mercado farmacéutico y como insumo complementario para interpretar hallazgos de valor contractual atípico.

### 2.3 Arquitectura técnica de BigLoI

La plataforma fue implementada como monorepo con arquitectura de siete capas (Tabla 2).

### Tabla 2. Arquitectura técnica de la plataforma BigLoI para vigilancia de contratación farmacéutica pública

| Capa | Tecnología principal | Función |
| --- | --------------------- | --- |
| Recolección | Python · API Socrata | Ingesta incremental de SECOP-II, INVIMA, SISMED |
| Almacenamiento | PostgreSQL · Pinecone · MongoDB | Datos relacionales · vectorial (9.336 docs) · no estructurados |
| Procesamiento | FastAPI · pandas | Limpieza, normalización, clasificación ABC, motor Z-score |
| IA generativa | Claude 3.5 Sonnet · GPT-4o | RAG con búsqueda híbrida semántica + TF-IDF |
| Aprendizaje automático | scikit-learn | Predicción de demanda (R²>0,85), k-means (6 grupos), PCA |
| Contratos inteligentes | Solidity · Chainlink CRE · Sepolia | Automatización de pagos en 5 estados; NFT de facturas |
| Visualización | React/TypeScript | Observatorio público: series temporales, mapas, alertas |

### 2.4 Motor de detección de anomalías de precio (Z-score)

Para cada contrato farmacéutico clasificado en una categoría terapéutica, se calculó la desviación estandarizada de su **valor total contractual** con respecto a la distribución de valores observada en contratos de la misma categoría. El análisis se restringió a categorías con al menos 10 contratos para evitar estimaciones inestables:

$$Z_i = \frac{V_i - \bar{V}_{cat}}{\sigma_{cat}}$$

donde $Z_i$ es la puntuación de anomalía del contrato $i$, $V_i$ es el valor total del contrato, $\bar{V}_{cat}$ es el valor promedio de los contratos en la misma categoría terapéutica y $\sigma_{cat}$ es la desviación estándar de esa distribución. Esta aproximación identifica contratos con valores atípicos dentro de su categoría, sin interpretar por sí sola sobreprecio unitario frente a una referencia regulatoria.

Los resultados se clasificaron en cuatro niveles de alerta basados en la magnitud de la desviación estándar:

| Nivel | Criterio | Interpretación |
| --- | --- | --- |
| CRÍTICO | \|Z\| ≥ 3,0σ | Valor contractual extremadamente atípico en su categoría |
| ALTO | 2,0σ ≤ \|Z\| < 3,0σ | Valor contractual claramente atípico |
| MEDIO | 1,5σ ≤ \|Z\| < 2,0σ | Valor contractual moderadamente atípico |
| NORMAL | \|Z\| < 1,5σ | Dentro del rango esperado de la categoría |

### 2.5 Análisis de concentración de mercado

Para caracterizar la estructura competitiva del mercado de contratación farmacéutica, se calcularon indicadores de concentración y se estimó el porcentaje del valor total acumulado en los principales proveedores. Se construyeron grafos bipartitos (entidades ↔ proveedores) para identificar patrones de recurrencia contractual.

### 2.6 Análisis de viabilidad del ciclo de pago mediante contratos inteligentes

Se implementó un simulador de cinco estados en red Sepolia para verificar transiciones funcionales entre etapas digitales del ciclo de pago farmacéutico. El contraste con el ciclo actual se realizó a nivel de orden de magnitud temporal, usando como referencia un flujo institucional agregado: para el tramo operativo se consideró evidencia local del Servicio Farmacéutico sobre necesidad, pedido, abastecimiento, recepción, registro y control, y para el tramo administrativo-financiero se utilizó una secuencia general de radicación, causación y pago compatible con hospitales públicos. La mediana de 90 días y el rango de 60–180 días se mantuvieron como referencias institucionales agregadas y no como una equivalencia operativa paso a paso entre el proceso hospitalario integral y los estados digitales del prototipo. El escenario referencial del prototipo fue de aproximadamente 30 horas. El ahorro proyectado se calculó aplicando el costo financiero promedio del sector (2% mensual) al valor total contratado ($42 billones COP) bajo un escenario de reducción sustancial de demoras administrativas digitales:

$$\text{Ahorro anual} = V_{total} \times r_{mensual} \times \frac{\Delta t_{días}}{30}$$

donde $V_{anual} \approx \$3{,}7$ billones COP (flujo anual promedio del período enero de 2015 a marzo de 2026; $V_{2025} = \$5{,}5$ billones COP), $r_{mensual} = 2\%$, y $\Delta t$ representa la reducción teórica del componente administrativo digital del ciclo de pago.

### 2.7 Análisis estadístico

Se utilizaron estadísticas descriptivas y se verificó la distribución log-normal del valor contractual (Kolmogorov-Smirnov). Para concentración de mercado se calcularon indicadores descriptivos de participación y acumulación. El umbral de significancia fue α = 0,05.

---

## 3. RESULTADOS

### 3.1 Características del corpus de datos

### Tabla 1. Resumen del corpus de contratación farmacéutica pública monitoreada en SECOP-II (enero de 2015 a marzo de 2026)

| Variable | Valor |
| --- | --- |
| Total contratos SECOP-II (universo API) | 272.814 |
| Contratos farmacéuticos indexados en BD PostgreSQL | 162.921 |
| Total contratos en BD PostgreSQL (todos los sectores) | 339.031 |
| Valor total contratado (farmacéutico — BD) | $17,16 billones COP |
| Valor total contratado (todos los sectores — BD) | $238,2 billones COP |
| Valor total contratado (universo API) | $42,00 billones COP |
| Valor promedio por contrato farmacéutico (BD) | $105 millones COP |
| Proveedores farmacéuticos únicos (BD) | 50.577 |
| Regiones cubiertas | 36–37 |
| Período (BD farmacéutico, vigencias activas) | 2020 a marzo de 2026 |
| Período (API SECOP-II monitoreado) | enero de 2015 a marzo de 2026 |
| Registros INVIMA procesados | 9.838 (todos vigentes) |
| Precios de referencia SISMED | 44.038 registros · 1.759 ATC únicos (2017–2019) |
| Documentos indexados (vector RAG) | 9.336 |

El valor contractual farmacéutico mostró distribución log-normal (Kolmogorov-Smirnov D = 0,04; p < 0,001). El 10% de los contratos de mayor valor concentra el 78% del valor total contratado.

**Evolución anual de contratos farmacéuticos indexados (vigencias 2020 a marzo de 2026):**

| Vigencia | Contratos | Valor (miles de millones COP) |
| --- | --- | --- |
| 2020 | 35.330 | 3.302,6 |
| 2021 | 53.832 | 2.856,7 |
| 2022 | 30.991 | 2.648,4 |
| 2023 | 10.705 | 1.603,1 |
| 2024 | 9.380 | 1.137,5 |
| 2025 | 22.033 | **5.519,3** |
| 2026 (parcial) | 650 | 90,5 |

El pico de contratos en 2021 refleja la respuesta pandémica COVID-19; el pico de valor en 2025 coincide con el aumento de oncológicos de alto costo.

**Distribución por categoría terapéutica:**

| Categoría | Contratos | Valor (MM COP) | Valor promedio (M COP) |
| --- | --- | --- | --- |
| Farmacéutico general | 82.303 | 9.990,3 | 121,4 |
| Dispositivo médico | 15.943 | 2.957,0 | 185,5 |
| Vacuna | 46.130 | 905,3 | 19,6 |
| **Oncológico** | 403 | 422,8 | **1.049,2** |
| Insumo médico | 2.312 | 201,6 | 87,2 |
| Antibiótico | 219 | 21,7 | 98,9 |
| Diabetes | 281 | 20,8 | 74,0 |
| Analgésico | 42 | 8,5 | 203,0 |
| Antiviral | 37 | 0,9 | 24,6 |

Los contratos oncológicos tienen el valor promedio más alto ($1.049 M COP/contrato).

### 3.2 Distribución geográfica

Las principales regiones por valor de contratación farmacéutica fueron:

| Región | Contratos | Valor (MM COP) | % del total |
| --- | --- | --- | --- |
| Bogotá D.C. (código SECOP 1) | 6.223 | 4.877,2 | 28,4% |
| Bogotá D.C. (código SECOP 2) | 12.093 | 4.788,4 | 27,9% |
| **Bogotá D.C. (combinado)** | **18.316** | **9.665,6** | **56,3%** |
| Antioquia | 48.039 | 1.316,2 | 7,7% |
| Valle del Cauca | 5.888 | 706,7 | 4,1% |
| Boyacá | 9.195 | 633,0 | 3,7% |
| Huila | 4.212 | 472,8 | 2,8% |
| Tolima | 3.816 | 431,6 | 2,5% |
| Santander | 4.319 | 418,8 | 2,4% |
| Cauca | 2.023 | 395,6 | 2,3% |
| Atlántico | 5.087 | 351,4 | 2,0% |

Bogotá D.C. concentra el **56,3%** del valor total nacional, seguida por Antioquia (7,7%) y Valle del Cauca (4,1%).

**Nota metodológica:** Bogotá D.C. aparece con dos códigos regionales distintos en SECOP-II. La cobertura de 36–37 regiones supera los 32 departamentos oficiales por codificaciones diferenciadas de distritos y otras entidades territoriales.

### 3.3 Anomalías de valor detectadas por el motor Z-score

**Nota metodológica:** El motor Z-score implementado calcula la desviación del valor total de cada contrato respecto a la distribución de su categoría terapéutica. Un cruce con precios unitarios SISMED requeriría desglose estructurado de ítems, no disponible de forma consistente en SECOP-II.

De los **147.670 contratos analizados** (en categorías con ≥10 contratos), el motor identificó:

| Nivel de alerta | Criterio | Contratos | % del total |
| --- | --- | --- | --- |
| CRÍTICO | \|Z\| ≥ 3,0σ | 307 | 0,21% |
| ALTO | 2,0σ ≤ \|Z\| < 3,0σ | 225 | 0,15% |
| MEDIO | 1,5σ ≤ \|Z\| < 2,0σ | 158 | 0,11% |
| **Total con alerta** | \|Z\| ≥ 1,5σ | **690** | **0,47%** |

**Resultados por categoría terapéutica:**

| Categoría | Contratos | % con alerta | Z_max | Ratio max/media |
| --- | --- | --- | --- | --- |
| Analgésico | 42 | 9,5% | 4,22 | 9,3× |
| Diabetes | 281 | **8,2%** | 6,58 | 15,3× |
| Antiviral | 37 | 5,4% | 4,83 | 14,2× |
| **Antibiótico** | 219 | 3,7% | **8,32** | **24,1×** |
| Insumo médico | 2.312 | 2,6% | 22,45 | 86,6× |
| Oncológico | 403 | 0,7% | 19,34 | 139,0× |

La categoría de **antibióticos** presentó el Z-score máximo más elevado (Z=8,32), mientras **diabetes** registró la mayor proporción de contratos con alerta (8,2%).

**Evolución temporal de la tasa de anomalías (2020–2025):**

| Año | Contratos | Contratos con alerta | Tasa (%) |
| --- | --- | --- | --- |
| 2020 | 35.326 | 120 | 0,34% |
| 2021 | 53.827 | 165 | 0,31% |
| 2022 | 30.990 | 129 | 0,42% |
| 2023 | 10.705 | 89 | 0,83% |
| 2024 | 9.380 | 86 | 0,92% |
| 2025 | 6.792 | 94 | **1,38%** |

La tasa de contratos con alerta estadística creció de **0,31% en 2021 a 1,38% en 2025**, un incremento del 345% en el período analizado. La interpretación causal de esta tendencia requiere análisis adicionales.

**Distribución geográfica de anomalías:**

Los departamentos con mayor tasa de contratos con alerta estadística fueron Bogotá D.C. (3,80%), Norte de Santander (1,92%), Valle del Cauca (1,21%) y Tolima (1,00%). Esta distribución sugiere mayor heterogeneidad de valores contratados, no evidencia causal de corrupción.

### 3.4 Concentración de mercado

El análisis de concentración del mercado de contratación farmacéutica colombiana (162.921 contratos, 50.577 proveedores) mostró:

El top 10 de proveedores concentró el 28,7% del valor total contratado y el top 3% de proveedores (1.518 de 50.577) concentró el 85,9%. El proveedor líder, VECOL SA, concentró el 5,58% del valor total. La distribución detallada se presenta en la Figura 4.

El patrón de concentración (top 3% = 85,9% del valor) es consistente con mercados oligopolísticos en contratación farmacéutica pública (16). El grafo bipartito identificó 847 pares de relaciones recurrentes entre la misma entidad y el mismo proveedor en al menos 5 contratos consecutivos.

### 3.5 Ciclo de pago mediante contratos inteligentes — prueba funcional de concepto

Las pruebas en red Sepolia del simulador BigLoI + Chainlink CRE verificaron la transición funcional entre estados digitales del proceso. Los tiempos reportados a continuación son **tiempos referenciales del prototipo** definidos para validación funcional por el investigador y **no** corresponden a mediciones observadas del proceso logístico y administrativo real. En particular, SECOP-II se utilizó como referencia contractual de origen, pero no representa una etapa operativa del flujo hospitalario en sí mismo.

| Etapa funcional | Tiempo del prototipo (referencial) |
| --- | --- |
| Contrato validado / orden habilitada → Medicamentos despachados | ~24 horas |
| Medicamentos despachados → Entrega verificada | ~4 horas |
| Entrega verificada → CRE registrado | ~1 hora |
| CRE registrado → Pago liberado | ~1 hora |
| **Ciclo digital completo del prototipo** | **~30 horas** |

Ciclo actual documentado en la literatura y en informes institucionales: 60–180 días (mediana 90 días). La comparación debe interpretarse como un escenario conceptual de reducción de demoras administrativas digitales, no como equivalencia directa con el proceso hospitalario integral.

**Ahorro proyectado en costo financiero:**

El flujo anual promedio de contratación farmacéutica es de $3,7 billones COP ($42 billones acumulados ÷ 11,25 años). Bajo un escenario teórico de reducción sustancial de demoras administrativas digitales, y aplicando un costo financiero del 2% mensual sobre el ciclo de pago evitable, se estimó:

$$\text{Ahorro anual} = \$3{,}7B \times 2\%/\text{mes} \times 3 \text{ meses} \approx \$224.000 \text{ millones COP/año}$$

Con la cifra de 2025, el ahorro potencial asciende a **$330.000 millones COP/año**.

### 3.6 Módulos complementarios: aprendizaje automático y búsqueda semántica

Los módulos complementarios de aprendizaje automático y búsqueda semántica mostraron factibilidad operativa, pero sus resultados deben interpretarse como exploratorios.

---

## 4. DISCUSIÓN

### 4.1 Escala e impacto del problema documentado

El corpus de 162.921 contratos farmacéuticos de 2020 a marzo de 2026 representa, hasta donde conocemos, la mayor serie longitudinal validada de contratación farmacéutica pública en Colombia. La distribución log-normal del valor contractual y la concentración del 78% del valor en el decil superior son consistentes con la literatura sobre mercados de contratación pública (14).

El incremento de la tasa de alertas estadísticas de 0,31% (2021) a 1,38% (2025) sugiere una mayor heterogeneidad en los valores contratados durante el período. Este fenómeno merece investigación específica con control de variables confusoras como inflación farmacéutica e incorporación de nuevas categorías de alto costo.

### 4.2 El Z-score como instrumento de vigilancia

La metodología Z-score presenta ventajas frente a la auditoría manual: opera sobre el universo completo de contratos, es reproducible y no requiere información confidencial. Un cruce futuro con precios unitarios SISMED y desagregación por ítems ampliaría la sensibilidad del detector (13,15). El incremento sostenido de la tasa de alertas entre 2021 y 2025 justifica evaluar su integración en procesos regulares de auditoría.

### 4.3 Contratos inteligentes aplicados al ciclo de pago farmacéutico: resultados de una prueba de concepto

La prueba funcional de concepto sugiere que la automatización condicionada podría reducir retrasos administrativos digitales y costos financieros asociados. Sin embargo, los tiempos reportados no representan mediciones reales del proceso completo, que también depende de transporte, embalaje, almacenamiento, validaciones institucionales y otros cuellos de botella no modelados. Una evaluación operativa más precisa requeriría integración con los sistemas de información de hospitales públicos y con flujos transaccionales de mayor granularidad. Su implementación a escala requeriría además integración con tesorería pública, validación regulatoria y auditoría independiente.

### 4.4 Contribución a la gobernanza de datos en salud

Colombia dispone de datos públicos para la vigilancia farmacéutica, pero carece de infraestructura analítica para convertirlos en evidencia accionable. BigLoI muestra que esta infraestructura puede construirse con tecnologías de código abierto, flujos reproducibles y consultas verificables sobre el corpus contractual.

### 4.5 Limitaciones

**Datos SECOP-II:** Las variables "entidad compradora" y "proveedor" muestran valores nulos o genéricos ("Desconocida"/"No especificado") en una proporción significativa de contratos en los archivos de muestra locales, lo que limita algunos análisis de red. Esta limitación refleja un problema de calidad en la fuente SECOP-II que ha sido documentado institucionalmente. Los 162.921 contratos farmacéuticos en la base PostgreSQL representan el subconjunto con mayor completitud de datos.

**Temporalidad y granularidad de SISMED:** La fuente SISMED disponible en datos abiertos cubre **2017–2019**, mientras que la cohorte principal de contratación farmacéutica analizada en PostgreSQL corresponde a **2020 a marzo de 2026**. En consecuencia, SISMED no se utilizó como comparador contemporáneo contrato a contrato, sino como referencia contextual del mercado. Además, la fuente SECOP-II consultada no proporciona de forma estructurada el desglose completo de ítems y precios unitarios para todos los contratos, lo que limita la validación directa de sobreprecio unitario.

**Red de prueba blockchain:** La validación del ciclo de pago se realizó en red Sepolia (testnet) como prueba funcional de transición entre estados digitales. Los tiempos del prototipo son referenciales y no corresponden a mediciones reales del proceso operativo integral. La implementación en mainnet requiere auditoría independiente de contratos inteligentes, validación regulatoria por la Superintendencia Financiera, coordinación con el sistema de tesorería pública e idealmente integración con sistemas hospitalarios para capturar eventos operativos de mayor detalle.

**Sesgo de selección en filtrado farmacéutico:** El uso de 19 palabras clave para identificar contratos farmacéuticos puede generar falsos negativos (contratos farmacéuticos con descripciones atípicas) y falsos positivos (contratos de otra naturaleza con términos farmacéuticos incidentales). Un estudio de validación de la taxonomía de clasificación sería necesario para estimar la precisión del universo.

**Alcance interpretativo:** El diseño observacional identifica patrones estadísticos pero no establece relaciones causales ni evalúa el impacto clínico de las anomalías detectadas. La interpretación de hallazgos como evidencia de corrupción requiere investigación complementaria con metodologías causales y participación de las instituciones competentes (Contraloría, Fiscalía).

### 4.6 Implicaciones para la política pública

Los hallazgos aportan insumos a tres debates de política pública: reforma del sistema de salud, transparencia en contratación y gobernanza de datos. La principal contribución del estudio es metodológica y reproducible: una infraestructura abierta capaz de transformar datos públicos dispersos en evidencia auditable. Los indicadores de concentración y recurrencia contractual pueden apoyar la priorización de auditorías, mientras la calidad desigual de SECOP-II merece atención institucional de Colombia Compra Eficiente.

---

## 5. CONCLUSIONES

Este estudio describe BigLoI, una plataforma computacional de vigilancia farmacéutica de cobertura nacional que monitorea 272.814 contratos en SECOP-II (enero de 2015 a marzo de 2026) y analiza empíricamente una cohorte principal indexada de 162.921 contratos farmacéuticos (2020 a marzo de 2026). Este análisis permite identificar tres hallazgos principales:

1. **Concentración de mercado:** El 3% de los proveedores (1.518 de 50.577) concentra el 85,9% del valor total; el top 10 concentra el 28,7%.

2. **Patrones estadísticos atípicos:** 690 contratos con alerta Z-score (|Z|≥1,5σ); antibióticos con Z_max=8,32; tasa de alertas que creció de 0,31% (2021) a 1,38% (2025).

3. **Infraestructura reproducible:** La integración de base de datos relacional, analítica reproducible y observatorio web permite convertir fuentes públicas dispersas en un instrumento auditable para vigilancia de contratación farmacéutica.

Como resultado complementario, la prueba funcional de concepto en red Sepolia sugiere que la automatización condicionada del pago podría reducir demoras administrativas digitales y generar ahorros financieros potenciales de $224.000–330.000 millones COP anuales bajo supuestos favorables. Esta línea requiere validación operativa, regulatoria y logística adicional.

BigLoI aporta evidencia sobre la viabilidad de una infraestructura abierta y reproducible de vigilancia para la contratación farmacéutica pública colombiana. En el marco editorial de PLOS ONE, su contribución principal es mostrar que una arquitectura computacional verificable puede generar hallazgos útiles sobre concentración de mercado, anomalías estadísticas y acceso auditable a la evidencia a partir de datos públicos.

---

## CONTRIBUCIÓN DEL AUTOR

Andrés Soto: concepción y diseño del estudio; desarrollo de la plataforma; adquisición, procesamiento y análisis de datos; redacción del manuscrito.

---

## FINANCIACIÓN

Este estudio fue financiado íntegramente con recursos propios del autor. No existió financiación externa.

---

## CONFLICTO DE INTERESES

El autor declara no tener conflicto de intereses.

---

## DISPONIBILIDAD DE DATOS Y CÓDIGO

- **Paquete de reproducibilidad del artículo:** Archivado en Zenodo con DOI <https://doi.org/10.5281/zenodo.19074137> y disponible en GitHub: <https://github.com/zswamtech/BigLoI-PLOS-ONE-paper>.
- **Código fuente ampliado de la plataforma BigLoI:** Disponible en GitHub: <https://github.com/zswamtech/BigLoI-PMV>.
- **Datos SECOP-II, INVIMA y SISMED:** Disponibles en datos.gov.co.
- **ORCID del autor principal:** <https://orcid.org/0009-0004-8001-5372>.
- **Observatorio Nacional de Medicamentos BigLoI:** La versión pública del observatorio se encuentra en finalización editorial y su URL se comunicará una vez se restablezca un despliegue productivo estable.

---

## REFERENCIAS

1. Departamento Nacional de Planeación. Sistema Electrónico de Contratación Pública SECOP-II: estadísticas de uso 2015–2026. Bogotá: Departamento Nacional de Planeación; 2026.

2. World Health Organization. Everybody's business: strengthening health systems to improve health outcomes: WHO's framework for action. Geneva: World Health Organization; 2007.

3. Contraloría General de la República de Colombia. Informe de auditoría al sistema de contratación farmacéutica pública 2023. Bogotá: Contraloría General de la República de Colombia; 2024.

4. Ministerio de Salud y Protección Social. SISMED: boletín de precios de medicamentos. Bogotá: Ministerio de Salud y Protección Social; 2025.

5. Defensoría del Pueblo de Colombia. Informe sobre desabastecimiento de medicamentos en el Eje Cafetero 2025. Bogotá: Defensoría del Pueblo de Colombia; 2025.

6. Transparency International. Monitoring the pharmaceutical sector: a practical guide. Berlin: Transparency International; 2016.

7. Kuo TT, Kim HE, Ohno-Machado L. Blockchain distributed ledger technologies for biomedical and health care applications. J Am Med Inform Assoc. 2017;24(6):1211-20. doi:10.1093/jamia/ocx068.

8. Lewis P, Perez E, Piktus A, Petroni F, Karpukhin V, Goyal N, et al. Retrieval-augmented generation for knowledge-intensive NLP tasks. Adv Neural Inf Process Syst. 2020;33:9459-74.

9. Habershon S, Habershon C. ProZorro: how Ukraine's e-procurement system is fighting corruption. OECD Observer. 2019;(318):23-4.

10. Open Contracting Partnership. Open Contracting Data Standard [Internet]. Washington (DC): Open Contracting Partnership; 2023 [citado 2026 Mar 16]. Disponible en: <https://standard.open-contracting.org/latest/en/>

11. European Anti-Fraud Office. The OLAF report 2023 [Internet]. Brussels: European Commission; 2024 [citado 2026 Mar 16]. Disponible en: <https://ec.europa.eu/olaf-report/2023/index_en.html>

12. Ferraz C, Finan F. Exposing corrupt politicians: the effects of Brazil's publicly released audits on electoral outcomes. Q J Econ. 2008;123(2):703-45.

13. Kanavos P, Vogler S. Pharmaceutical market monitoring, policies and pharmaceutical pricing. Geneva: World Health Organization; 2019.

14. Fazekas M, Tóth IJ, King LP. An objective corruption risk index using public procurement data. Eur J Crim Policy Res. 2016;22(3):369-97.

15. Management Sciences for Health. MDS-3: managing access to medicines and health technologies. Arlington (VA): Management Sciences for Health; 2012.

16. Vásquez MA, Sánchez C. Análisis de concentración en el mercado de medicamentos en Colombia. Rev Salud Pública. 2020;22(1):e185177.

---

## FIGURE LEGENDS

**Figura 1.** Evolución anual de la contratación farmacéutica pública monitoreada en SECOP-II (2020 a marzo de 2026): número de contratos y valor total.

**Figura 2.** Distribución geográfica del valor de la contratación farmacéutica pública monitoreada en SECOP-II por departamento (2020 a marzo de 2026).

**Figura 3.** Distribución de anomalías estadísticas de valor detectadas por el motor Z-score, por categoría terapéutica (2020–2025).

**Figura 4.** Concentración de mercado en la contratación farmacéutica pública monitoreada en SECOP-II (2020 a marzo de 2026): curva de Lorenz y top 10 proveedores.

**Figura 5.** Esquema conceptual del ciclo de pago farmacéutico: flujo actual institucional versus estados digitales del prototipo mediante contratos inteligentes (prueba de concepto en red Sepolia).

**Figura 6.** Arquitectura técnica simplificada de la plataforma BigLoI: siete capas de procesamiento de datos farmacéuticos públicos.

**Tabla 1.** Resumen del corpus de contratación farmacéutica pública monitoreada en SECOP-II (presentada en resultados).

**Tabla 2.** Arquitectura técnica de la plataforma BigLoI para vigilancia de contratación farmacéutica pública.

---

## APPENDICES

### Anexo 1. Taxonomía de filtrado farmacéutico SECOP-II

**Términos de inclusión (19):** medicamento, farmacéutico, farmacia, antibiótico, vacuna, insulina, quimioterapia, dispositivos médicos, insumo médico, suministro médico, biológico, antiviral, analgésico, anestesia, oncológico, hemodiálisis, hormonal, anticoagulante, inmunosupresor.

**Términos de exclusión (5):** obra civil, construcción, mantenimiento, tecnología de información, mobiliario.

### Anexo 2. Esquema simplificado de la base de datos

Tablas principales: `observatorio_nacional.contratos_secop` (339.031 registros totales; 162.921 farmacéuticos) · `observatorio_nacional.sismed_precios_referencia` (44.038 registros · 1.759 ATC únicos · años 2017–2019) · `observatorio_nacional.invima_medicamentos` (9.838 registros Vigentes) · `puntos_autorizados` (101 hospitales) · `medicamentos` (~10.000 registros del formulario) · `sim_hospitales_100` (100 hospitales de simulación).

### Anexo 3. Protocolo de contratos inteligentes

Contrato inteligente: `InvoiceRegistry.sol` (Solidity) · Red: Sepolia testnet (Ethereum) · Oráculo: Chainlink CRE · NFT: `InvoiceNFT.sol` para trazabilidad de facturas · Escrow: `PaymentEscrow.sol` para liberación condicional de pagos.
