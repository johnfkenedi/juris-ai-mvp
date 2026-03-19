# Límites formales del MVP 1

**Versión:** 1.0  
**Fecha:** 2026-03-19  
**Estado:** vigente  

---

## Qué puede hacer este sistema

- Recibir una consulta en lenguaje natural en materia administrativo-fiscal
- Buscar dentro de un corpus de 8 tesis jurisprudenciales
- Recuperar los documentos más relevantes por similitud de términos (BM25)
- Generar una respuesta resumida fundamentada en los documentos recuperados
- Mostrar referencias con registro digital, instancia y época de cada tesis

---

## Qué NO puede hacer este sistema

- Analizar expedientes reales del despacho
- Redactar demandas, recursos o escritos jurídicos
- Emitir estrategia jurídica final ni opinión legal vinculante
- Buscar fuera del corpus cargado — no accede a internet ni a bases de datos externas
- Garantizar que la jurisprudencia citada esté vigente al momento de la consulta
- Detectar contradicciones de tesis ni jerarquía entre criterios
- Procesar preguntas fuera de materia administrativo-fiscal
- Sustituir el criterio profesional del abogado

---

## Restricciones técnicas actuales

- Corpus: 8 tesis jurisprudenciales únicamente
- Normativa indexada: ninguna en esta fase
- Retrieval: BM25 por palabras clave — no entiende sinónimos ni paráfrasis
- Sin memoria de conversación — cada consulta es independiente
- Sin autenticación de usuarios
- Sin historial de consultas
- Sin validación de vigencia de tesis

---

## Advertencias de uso

- Las respuestas son orientativas y deben ser verificadas por un profesional
- El sistema puede no encontrar documentos relevantes si la consulta usa términos muy distintos a los del corpus
- Un score bajo en las referencias indica recuperación débil — la respuesta puede ser menos confiable
- Este sistema es un prototipo en fase de prueba controlada

---

## Criterios mínimos de calidad validados

| Criterio | Resultado | Fecha |
|---|---|---|
| Retrieval 8/8 consultas de prueba | PASS | 2026-03-19 |
| Respuesta fundamentada en documentos recuperados | Verificado manualmente | 2026-03-19 |
| Referencias visibles con datos de tesis | Verificado manualmente | 2026-03-19 |
| Sin alucinaciones en consultas de prueba | Verificado manualmente | 2026-03-19 |

---

## Próximas mejoras planificadas

- Incorporar normativa al índice (CFF, LFPCA prioritarios)
- Agregar embeddings semánticos para retrieval híbrido
- Ampliar corpus con más tesis
- Agregar historial de consultas
- Validación de vigencia de tesis
