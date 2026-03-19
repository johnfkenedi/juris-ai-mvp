"""
chunk_documents.py
Bloque 4 — Chunking del corpus jurídico (fase 1: solo jurisprudencia).
Lee los .txt procesados de jurisprudencia y produce chunks con metadatos
en data/processed/chunks/ como archivos JSON.
"""

import json
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
CHUNKS_DIR = Path("data/processed/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

# Solo jurisprudencia en esta fase
JURIS_IDS = [
    "juris_001_jcaf_autoridad_no_puede_exhibir_credito_fiscal",
    "juris_002_jcaf_duracion_visita_domiciliaria",
    "juris_003_prescripcion_creditos_fiscales_multas_penales",
    "juris_004_revision_fiscal_dos_fechas_presentacion_oportunidad",
    "juris_005_creditos_respaldados_efecto_fiscal_seguridad_juridica",
    "juris_006_prescripcion_facultades_cobro_revocacion_confirmativa_ficta",
    "juris_007_sobreseimiento_extemporaneidad_desconocimiento_notificacion_prescripcion",
    "juris_008_visita_domiciliaria_extralimitacion_visitadores_nulidad",
]


def build_chunk(doc_id: str, text: str, chunk_index: int = 0) -> dict:
    """Construye un chunk con metadatos mínimos para el retrieval."""
    return {
        "chunk_id": f"{doc_id}_chunk_{chunk_index:03d}",
        "doc_id": doc_id,
        "tipo": "jurisprudencia",
        "subtipo": "tesis",
        "materia": "administrativo-fiscal",
        "chunk_index": chunk_index,
        "texto": text.strip(),
        "chars": len(text.strip()),
    }


def main():
    print("=" * 60)
    print("CHUNKING — JURISPRUDENCIA MVP 1")
    print("=" * 60)

    chunks_totales = []

    for doc_id in JURIS_IDS:
        txt_path = PROCESSED_DIR / f"{doc_id}.txt"

        if not txt_path.exists():
            print(f"  [FALTA] {txt_path.name}")
            continue

        texto = txt_path.read_text(encoding="utf-8").strip()

        if not texto:
            print(f"  [VACÍO] {txt_path.name}")
            continue

        # Cada tesis jurisprudencial = 1 chunk completo
        chunk = build_chunk(doc_id, texto, chunk_index=0)
        chunks_totales.append(chunk)

        # Guardar chunk individual como JSON
        chunk_path = CHUNKS_DIR / f"{chunk['chunk_id']}.json"
        chunk_path.write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

        print(f"  [OK] {chunk['chunk_id']}  ({chunk['chars']:,} chars)")

    # Guardar también un archivo consolidado con todos los chunks
    consolidated_path = CHUNKS_DIR / "jurisprudencia_chunks.json"
    consolidated_path.write_text(
        json.dumps(chunks_totales, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("\n" + "=" * 60)
    print(f"RESUMEN: {len(chunks_totales)} chunks generados")
    print(f"Chunks individuales: {CHUNKS_DIR}")
    print(f"Consolidado: {consolidated_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
