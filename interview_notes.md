# 📝 Notas de Entrevista — Data Engineering

> Conceptos clave para repasar antes de entrevistas técnicas.
> Explica siempre con tus propias palabras, no memorices definiciones.

---

## 1. ETL vs ELT

### ETL (Extract, Transform, Load)
- Transformas los datos **antes** de cargarlos en el warehouse
- Usas Python/Pandas para limpiar
- El warehouse solo recibe datos limpios
- **Cuándo usarlo:** datos sensibles (GDPR, médicos, financieros), transformaciones complejas que SQL no puede hacer

### ELT (Extract, Load, Transform)
- Cargas los datos crudos **primero** en el warehouse
- Transformas **dentro** del warehouse con SQL (dbt)
- **Cuándo usarlo:** datos masivos, warehouses cloud modernos (Snowflake, BigQuery, Redshift)

### ¿Por qué ELT ganó?
- Los warehouses modernos son baratos y potentes
- Si la lógica de negocio cambia, solo re-ejecutas las transformaciones
- Los datos originales nunca se pierden

### Pregunta típica
> *"¿Cuándo usarías ETL vs ELT?"*
> "Depende del caso de uso. Para datos sensibles o transformaciones complejas en Python, ETL. Para stacks modernos con warehouses cloud, ELT con dbt es el estándar."

---

## 2. Arquitectura Medallion (Bronze / Silver / Gold)

Forma de organizar datos en capas dentro de un warehouse. Cada capa tiene un nivel de calidad mayor.

```
FUENTES          BRONZE            SILVER              GOLD
(CSVs, APIs) →  datos crudos  →  datos limpios  →  datos listos
                sin tocar         validados           para negocio
```

### 🥉 Bronze (raw)
- Datos exactamente como llegaron de la fuente
- Sin transformar, sin limpiar
- Pueden tener nulos, duplicados, tipos incorrectos
- **Objetivo:** copia fiel del origen, nunca se modifica

### 🥈 Silver (staging)
- Datos limpios y validados
- Fechas convertidas, nulos tratados, duplicados eliminados
- Tipos de datos correctos
- **Objetivo:** datos confiables para trabajar

### 🥇 Gold (mart)
- Datos listos para análisis de negocio
- JOINs hechos, métricas calculadas, agregaciones
- Lo que consume analytics o dashboards
- **Objetivo:** responder preguntas de negocio directamente

### En nuestro proyecto
```
Airflow carga CSVs → PostgreSQL (Bronze)
                           ↓
                    dbt staging/ (Silver)
                           ↓
                    dbt mart/ (Gold)
```

### Preguntas típicas
> *"¿Qué es la arquitectura medallion?"*
> "Es una forma de organizar datos en tres capas: bronze con datos crudos, silver con datos limpios, y gold con datos listos para negocio."

> *"¿Por qué no transformar directamente los datos crudos?"*
> "Porque si la lógica de negocio cambia necesitas el histórico original. Con bronze siempre tienes los datos tal como llegaron."

---

## 3. Data Pipeline / ETL

### ¿Qué es un pipeline de datos?
Conjunto de pasos automatizados que mueven y transforman datos de una fuente a un destino.

### Componentes típicos
- **Fuente:** CSV, API, base de datos, Kafka...
- **Orquestador:** Airflow (ejecuta los pasos en orden)
- **Transformación:** Python/Pandas o dbt
- **Destino:** PostgreSQL, Snowflake, BigQuery...

### Idempotencia
Un pipeline es idempotente si ejecutarlo varias veces produce el mismo resultado.
- `if_exists='replace'` en Pandas es idempotente
- `if_exists='append'` NO es idempotente (duplica datos)

### Pregunta típica
> *"¿Qué pasa si el pipeline falla?"*
> "Depende de la herramienta. En Airflow puedes configurar reintentos automáticos, alertas por email, y el pipeline se marca como fallido para investigar. Lo importante es que el pipeline sea idempotente para poder re-ejecutarlo sin duplicar datos."

---

## 4. Batch vs Streaming

### Batch
- Procesa datos en bloques, a intervalos regulares
- Ejemplo: pipeline que corre cada noche a las 2am
- **Herramientas:** Airflow, Spark batch

### Streaming
- Procesa datos en tiempo real, evento por evento
- Ejemplo: detección de fraude en tiempo real
- **Herramientas:** Kafka, Spark Streaming, Flink

### ¿Cuándo usar cada uno?
- **Batch:** análisis de negocio, reportes, dashboards. No necesitas tiempo real.
- **Streaming:** alertas, detección de fraude, métricas en vivo.

### Pregunta típica
> *"¿Cuándo usarías streaming en vez de batch?"*
> "Cuando el negocio necesita actuar sobre los datos en segundos o minutos. Por ejemplo, detección de fraude o monitorización de sistemas. Para análisis de negocio y reportes, batch es suficiente y más simple."

---

## 5. Data Warehouse vs Data Lake vs Data Lakehouse

### Data Warehouse
- Datos estructurados y limpios
- Optimizado para queries analíticas (OLAP)
- Ejemplos: Snowflake, BigQuery, Redshift
- **Cuándo:** análisis de negocio, BI, dashboards

### Data Lake
- Datos crudos de cualquier tipo (estructurados, semiestructurados, no estructurados)
- Storage barato (S3, GCS)
- **Cuándo:** almacenar todo antes de saber cómo usarlo, ML, logs

### Data Lakehouse
- Combina lo mejor de ambos: storage barato + capacidad analítica
- Ejemplos: Delta Lake, Apache Iceberg, Databricks
- **Cuándo:** quieres el coste de un lake con la potencia de un warehouse

### Pregunta típica
> *"¿Qué diferencia hay entre un data lake y un data warehouse?"*
> "Un warehouse almacena datos estructurados y limpios optimizados para análisis. Un lake almacena cualquier tipo de dato en crudo de forma barata. El lakehouse intenta combinar ambos."

---

## 6. Conceptos SQL importantes

### Window Functions
Calculan valores sobre un conjunto de filas sin colapsar el resultado.
- `ROW_NUMBER()` → número único por fila
- `RANK()` → ranking con huecos en empates
- `DENSE_RANK()` → ranking sin huecos en empates
- `LAG()` → valor de la fila anterior
- `LEAD()` → valor de la fila siguiente

### CTEs (Common Table Expressions)
Query temporal con nombre que se puede referenciar después.
```sql
WITH nombre AS (
    SELECT ...
)
SELECT * FROM nombre;
```

### HAVING vs WHERE
- `WHERE` filtra filas **antes** de agrupar
- `HAVING` filtra grupos **después** de agrupar
- Regla: si la condición usa una función de agregación → `HAVING`

### NULL en ORDER BY (PostgreSQL)
- `ORDER BY col DESC` → NULLs aparecen primero por defecto
- Solución: `ORDER BY col DESC NULLS LAST`

---

## 7. dbt

### ¿Qué es dbt?
Herramienta para hacer transformaciones SQL en producción. Es la **T del ELT**.
- Se conecta al warehouse directamente
- Cada modelo es un fichero `.sql` con un `SELECT`
- dbt crea las tablas/vistas automáticamente
- Incluye tests de calidad de datos y documentación

### Modelo dbt
Fichero `.sql` con un `SELECT`. dbt lo ejecuta y crea una tabla o vista.
```sql
-- models/staging/stg_orders.sql
SELECT
    order_id,
    customer_id,
    order_status
FROM orders
WHERE order_status = 'delivered'
```

### Comandos básicos
- `dbt run` → ejecuta todos los modelos
- `dbt test` → ejecuta los tests
- `dbt docs generate` → genera documentación

### Pregunta típica
> *"¿Qué es dbt y para qué sirve?"*
> "dbt es la herramienta estándar para hacer transformaciones SQL en producción. En vez de escribir CREATE TABLE manualmente, defines modelos SQL con SELECT y dbt gestiona la creación de tablas, dependencias entre modelos, tests de calidad y documentación."

---

## 8. Apache Airflow

### ¿Qué es Airflow?
Orquestador de pipelines. Ejecuta tareas en el orden correcto, a la hora correcta, y avisa si algo falla.

### DAG
Directed Acyclic Graph. Un pipeline en Airflow.
- **Directed:** las tareas tienen dirección
- **Acyclic:** no hay ciclos
- **Graph:** grafo de tareas conectadas

### Operador `>>`
Define dependencias entre tareas:
```python
tarea_1 >> tarea_2 >> tarea_3
```

### XComs
Mecanismo para pasar datos entre tareas:
- `ti.xcom_push(key, value)` → guarda un valor
- `ti.xcom_pull(key, task_ids)` → recupera un valor

### Pregunta típica
> *"¿Qué pasa si una tarea falla en Airflow?"*
> "Airflow marca la tarea como fallida, para la ejecución de las tareas downstream, y puede configurarse para reintentos automáticos y alertas. El DAG queda en estado fallido para investigar."

---

## 9. Preguntas de diseño de sistemas

### "¿Cómo diseñarías un pipeline para millones de registros?"
1. ELT en vez de ETL para aprovechar el warehouse
2. Procesamiento incremental (solo datos nuevos, no todo)
3. Particionado por fecha para queries eficientes
4. Spark o BigQuery para procesamiento distribuido
5. Monitorización y alertas

### "¿Cómo evitarías duplicados en un pipeline?"
1. Pipeline idempotente (`if_exists='replace'`)
2. Clave primaria única en la tabla destino
3. Deduplicación con `ROW_NUMBER() OVER (PARTITION BY id ORDER BY updated_at DESC)`

### "¿Qué es particionamiento?"
Dividir una tabla grande en partes más pequeñas por una columna (normalmente fecha).
- Mejora el rendimiento de queries que filtran por esa columna
- Ejemplo: tabla de eventos particionada por mes

---

*Actualiza este fichero cada vez que aprendas un concepto nuevo.*
