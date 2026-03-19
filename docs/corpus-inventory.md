# Inventario del Corpus — MVP 1

**Versión:** 0.1  
**Fecha:** 2026-03-18  
**Estado:** activo  
**Mantenido por:** equipo técnico del proyecto  

---

## Resumen

| Tipo           | Subtipo             | Cantidad |
|----------------|---------------------|----------|
| Jurisprudencia | Tesis / criterio    | 8        |
| Normativa      | Ley / Código / Rgto | 5        |
| **Total**      |                     | **13**   |

---

## Jurisprudencia

Ubicación: `data/raw/jurisprudencia/`  
Fuente: Tribunal Federal de Justicia Administrativa (TFJA) / Juicio Contencioso Administrativo Federal (JCAF)  
Materia: Administrativo-fiscal  

| id        | archivo                                                                            | tipo           | subtipo | tema_principal                                                        | materia              | fuente      | rubro_completo       | estatus |
|-----------|------------------------------------------------------------------------------------|----------------|---------|-----------------------------------------------------------------------|----------------------|-------------|----------------------|---------|
| juris_001 | juris_001_jcaf_autoridad_no_puede_exhibir_credito_fiscal.pdf                       | jurisprudencia | tesis   | Autoridad no puede exhibir crédito fiscal que no presentó oportunamente | Administrativo-fiscal | TFJA / JCAF | pendiente_confirmar  | activo  |
| juris_002 | juris_002_jcaf_duracion_visita_domiciliaria.pdf                                    | jurisprudencia | tesis   | Duración máxima de visita domiciliaria                                | Administrativo-fiscal | TFJA / JCAF | pendiente_confirmar  | activo  |
| juris_003 | juris_003_prescripcion_creditos_fiscales_multas_penales.pdf                        | jurisprudencia | tesis   | Prescripción de créditos fiscales y multas con carácter penal         | Administrativo-fiscal | pendiente   | pendiente_confirmar  | activo  |
| juris_004 | juris_004_revision_fiscal_dos_fechas_presentacion_oportunidad.pdf                 | jurisprudencia | tesis   | Revisión fiscal — presentación en dos fechas y oportunidad procesal   | Administrativo-fiscal | pendiente   | pendiente_confirmar  | activo  |
| juris_005 | juris_005_creditos_respaldados_efecto_fiscal_seguridad_juridica.pdf               | jurisprudencia | tesis   | Créditos respaldados — efecto fiscal y seguridad jurídica             | Administrativo-fiscal | pendiente   | pendiente_confirmar  | activo  |
| juris_006 | juris_006_prescripcion_facultades_cobro_revocacion_confirmativa_ficta.pdf         | jurisprudencia | tesis   | Prescripción de facultades de cobro — revocación confirmativa ficta   | Administrativo-fiscal | pendiente   | pendiente_confirmar  | activo  |
| juris_007 | juris_007_sobreseimiento_extemporaneidad_desconocimiento_notificacion_prescripcion.pdf | jurisprudencia | tesis | Sobreseimiento por extemporaneidad — desconocimiento de notificación y prescripción | Administrativo-fiscal | pendiente | pendiente_confirmar | activo |
| juris_008 | juris_008_visita_domiciliaria_extralimitacion_visitadores_nulidad.pdf             | jurisprudencia | tesis   | Extralimitación de visitadores en visita domiciliaria — nulidad       | Administrativo-fiscal | TFJA / JCAF | pendiente_confirmar  | activo  |

### Notas jurisprudencia
- El campo `rubro_completo` se completará en Bloque 3 abriendo cada PDF y extrayendo el rubro oficial.
- El campo `fuente` se completará confirmando sala, época y número de tesis en cada documento.
- Todos los documentos son públicos y de uso permitido para investigación jurídica.

---

## Normativa

Ubicación: `data/raw/normativa/`  
Fuente: Diario Oficial de la Federación (DOF) / SAT  
Materia: Fiscal / Administrativo / Procesal  

| id       | archivo                                                          | tipo      | subtipo    | tema_principal                                      | materia               | fuente   | estatus |
|----------|------------------------------------------------------------------|-----------|------------|-----------------------------------------------------|-----------------------|----------|---------|
| norm_001 | norm_001_cff_codigo_fiscal_federacion.pdf                        | normativa | código     | Código Fiscal de la Federación                      | Fiscal                | DOF      | activo  |
| norm_002 | norm_002_lfpca_procedimiento_contencioso_administrativo.pdf      | normativa | ley        | Ley Federal del Procedimiento Contencioso Administrativo | Administrativo   | DOF      | activo  |
| norm_003 | norm_003_lfpa_procedimiento_administrativo.pdf                   | normativa | ley        | Ley Federal del Procedimiento Administrativo        | Administrativo        | DOF      | activo  |
| norm_004 | norm_004_risat_reglamento_interior_sat.pdf                       | normativa | reglamento | Reglamento Interior del SAT                         | Fiscal / Organizativo | DOF      | activo  |
| norm_005 | norm_005_cfpc_codigo_federal_procedimientos_civiles.pdf          | normativa | código     | Código Federal de Procedimientos Civiles            | Procesal civil        | DOF      | activo  |

### Notas normativa
- La normativa funciona como contexto de apoyo, no como núcleo del retrieval.
- En el Bloque 4 se decidirá si se indexa completa o solo por capítulos relevantes.
- El CFF y la LFPCA tienen prioridad de indexación por su uso directo en litigio fiscal.

---

## Criterios de inclusión del corpus

- Tamaño controlado: máximo 15 documentos en esta fase
- Enfoque temático: fundamentación y motivación, nulidad del acto administrativo, créditos fiscales, recurso de revocación, legalidad formal del acto de autoridad
- Documentos públicos, legibles digitalmente (no OCR en esta fase)
- Sin datos reales del despacho

---

## Pendientes antes del Bloque 4

- [ ] Completar `rubro_completo` de cada tesis abriendo los PDFs
- [ ] Confirmar fuente exacta (sala, época, número) de juris_003 a juris_007
- [ ] Decidir estrategia de indexación para normativa (completa vs. por capítulos)
- [ ] Verificar que todos los PDFs son texto digital (no escaneos) con script de validación
