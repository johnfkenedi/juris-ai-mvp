"""
tests/test_retrieval.py
Bloque 6 — Validación del retrieval BM25.
Verifica que cada consulta de prueba recupera el documento esperado.
Ejecutar con: python tests/test_retrieval.py
"""

import json
import re
import sys
from pathlib import Path
from rank_bm25 import BM25Okapi

CHUNKS_FILE = Path("data/processed/chunks/jurisprudencia_chunks.json")


def tokenize(text: str) -> list[str]:
    stopwords = {
        "de", "la", "el", "en", "y", "a", "los", "las", "del", "un", "una",
        "con", "por", "que", "se", "no", "es", "al", "su", "lo", "le", "o",
        "para", "como", "pero", "si", "son", "has", "fue", "ser", "esta",
        "este", "esto", "entre", "sobre", "ante", "dicho", "dicha", "mismo",
    }
    tokens = re.findall(r"[a-záéíóúüñ]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]


# Casos de prueba: (consulta, doc_id esperado en top 3)
CASOS = [
    (
        "prescripción de créditos fiscales",
        "juris_003_prescripcion_creditos_fiscales_multas_penales",
    ),
    (
        "visita domiciliaria extralimitación nulidad",
        "juris_008_visita_domiciliaria_extralimitacion_visitadores_nulidad",
    ),
    (
        "recurso de revocación confirmativa ficta",
        "juris_006_prescripcion_facultades_cobro_revocacion_confirmativa_ficta",
    ),
    (
        "duración máxima de la visita domiciliaria",
        "juris_002_jcaf_duracion_visita_domiciliaria",
    ),
    (
        "autoridad no puede exhibir documentos que no presentó",
        "juris_001_jcaf_autoridad_no_puede_exhibir_credito_fiscal",
    ),
    (
        "sobreseimiento extemporaneidad notificación",
        "juris_007_sobreseimiento_extemporaneidad_desconocimiento_notificacion_prescripcion",
    ),
    (
        "créditos respaldados seguridad jurídica",
        "juris_005_creditos_respaldados_efecto_fiscal_seguridad_juridica",
    ),
    (
        "revisión fiscal presentación dos fechas",
        "juris_004_revision_fiscal_dos_fechas_presentacion_oportunidad",
    ),
]


def main():
    print("=" * 60)
    print("VALIDACIÓN DE RETRIEVAL — MVP 1")
    print("=" * 60)

    with open(CHUNKS_FILE, encoding="utf-8") as f:
        chunks = json.load(f)

    corpus_tokens = [tokenize(c["texto"]) for c in chunks]
    indice = BM25Okapi(corpus_tokens)

    aprobados = 0
    fallidos = 0

    for consulta, doc_esperado in CASOS:
        tokens = tokenize(consulta)
        scores = indice.get_scores(tokens)
        ranking = sorted(
            [(chunks[i]["doc_id"], round(float(s), 4)) for i, s in enumerate(scores)],
            key=lambda x: x[1],
            reverse=True,
        )
        top3 = [doc_id for doc_id, _ in ranking[:3]]
        ok = doc_esperado in top3
        estado = "PASS" if ok else "FAIL"

        if ok:
            aprobados += 1
        else:
            fallidos += 1

        print(f"  [{estado}] {consulta}")
        if not ok:
            print(f"         esperado: {doc_esperado}")
            print(f"         top 3:    {top3}")

    print()
    print("=" * 60)
    print(f"RESULTADO: {aprobados}/{len(CASOS)} pruebas aprobadas")
    if fallidos == 0:
        print("Retrieval funcionando correctamente.")
    else:
        print(f"ATENCIÓN: {fallidos} prueba(s) fallida(s). Revisar corpus o tokenización.")
    print("=" * 60)

    sys.exit(0 if fallidos == 0 else 1)


if __name__ == "__main__":
    main()
