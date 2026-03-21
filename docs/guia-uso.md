# Guía de uso — Buscador de Jurisprudencia JFCN

**Versión:** 1.0  
**Fecha:** 2026-03-21  
**Dirigido a:** Equipo del despacho JFCN  

---

## ¿Qué es este sistema?

Es una herramienta de consulta jurídica con inteligencia artificial que permite buscar dentro del corpus de jurisprudencia y normativa fiscal del despacho. El sistema recupera los documentos más relevantes y genera una respuesta fundamentada en ellos.

---

## ¿Cómo acceder?

1. Abre el navegador y ve a `http://localhost:3000`
2. Ingresa la clave de acceso del despacho
3. Haz clic en **Ingresar**

---

## ¿Cómo hacer una consulta?

1. Escribe tu consulta en el cuadro de texto en lenguaje natural
2. Presiona **Enter** o haz clic en **Consultar**
3. Espera la respuesta — puede tardar entre 2 y 8 segundos
4. Lee la respuesta y revisa las fuentes citadas al final

### Ejemplos de consultas que funcionan bien

- ¿Cuándo prescribe la facultad de cobro del SAT?
- ¿Qué límites tiene una visita domiciliaria?
- ¿Qué dice el artículo 146 del CFF?
- ¿Qué ocurre si la autoridad no presentó el crédito fiscal a tiempo?
- ¿Cuándo procede el sobreseimiento por extemporaneidad?

---

## ¿Cómo interpretar los resultados?

### La respuesta
El sistema genera una respuesta basada únicamente en los documentos del corpus. Cada afirmación está fundamentada en los documentos recuperados.

### Las fuentes
Debajo de la respuesta aparecen las fuentes consultadas con tres niveles de relevancia:

| Indicador | Significado |
|---|---|
| 🟢 Alta relevancia | El documento es muy pertinente para la consulta |
| 🟡 Relevancia media | El documento tiene relación parcial con la consulta |
| 🔴 Relevancia baja | El documento fue recuperado pero su relación es débil |

Cuando el indicador es rojo, la respuesta puede ser menos confiable — se recomienda verificar directamente en la fuente.

---

## Corpus disponible

### Jurisprudencia (8 tesis)
- Autoridad no puede exhibir crédito fiscal que no presentó oportunamente
- Duración máxima de visita domiciliaria
- Prescripción de créditos fiscales y multas
- Revisión fiscal — presentación en dos fechas
- Créditos respaldados — efecto fiscal y seguridad jurídica
- Prescripción de facultades de cobro — revocación confirmativa ficta
- Sobreseimiento por extemporaneidad
- Extralimitación de visitadores — nulidad

### Normativa
- Código Fiscal de la Federación (506 artículos)
- Ley Federal del Procedimiento Contencioso Administrativo (136 artículos)

---

## Limitaciones importantes

- El sistema **no sustituye el criterio profesional del abogado**
- Las respuestas son orientativas y deben verificarse
- El corpus es controlado — no accede a internet ni a bases de datos externas
- No garantiza que la jurisprudencia citada esté vigente al momento de la consulta
- Cada consulta es independiente — el sistema no recuerda conversaciones anteriores

---

## Soporte técnico

Si el sistema no responde o aparece un error de conexión, verifica que el backend esté corriendo en la terminal. Si el problema persiste, contacta al equipo técnico.
