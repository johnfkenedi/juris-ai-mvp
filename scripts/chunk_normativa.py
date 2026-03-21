"""
scripts/chunk_normativa.py
Bloque 8 — Chunking de normativa por articulo.
Procesa CFF y LFPCA y genera chunks por articulo con metadatos.
"""

import json
import re
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
CHUNKS_DIR = Path("data/processed/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

DOCUMENTOS = [
    {
        "doc_id": "norm_001_cff_codigo_fiscal_federacion",
        "tipo": "normativa",
        "subtipo": "codigo",
        "materia": "fiscal",
        "patron": r"^Artículo\s+[\dA-Za-z]",
    },
    {
        "doc_id": "norm_002_lfpca_procedimiento_contencioso_administrativo",
        "tipo": "normativa",
        "subtipo": "ley",
        "materia": "administrativo-fiscal",
        "patron": r"^ARTÍCULO\s+[\dA-Za-z]|^Artículo\s+\d",
    },
]


def extraer_articulos(texto: str, patron: str) -> list[dict]:
    """Divide el texto en bloques por artículo."""
    lineas = texto.split("\n")
    articulos = []
    bloque_actual = []
    titulo_actual = None

    for linea in lineas:
        if re.match(patron, linea.strip()):
            if titulo_actual and bloque_actual:
                articulos.append({
                    "titulo": titulo_actual,
                    "texto": "\n".join(bloque_actual).strip(),
                })
            titulo_actual = linea.strip()
            bloque_actual = [linea]
        else:
            if titulo_actual:
                bloque_actual.append(linea)

    if titulo_actual and bloque_actual:
        articulos.append({
            "titulo": titulo_actual,
            "texto": "\n".join(bloque_actual).strip(),
        })

    return articulos


def extraer_numero_articulo(titulo: str) -> str:
    """Extrae el número de artículo del título."""
    match = re.search(r"[\dA-Za-z][\w\-]*", titulo.replace("ARTÍCULO", "").replace("Artículo", ""))
    return match.group(0).strip() if match else "?"


def main():
    print("=" * 60)
    print("CHUNKING DE NORMATIVA — MVP 1")
    print("=" * 60)

    todos_chunks = []

    for doc in DOCUMENTOS:
        txt_path = PROCESSED_DIR / f"{doc['doc_id']}.txt"

        if not txt_path.exists():
            print(f"  [FALTA] {txt_path.name}")
            continue

        texto = txt_path.read_text(encoding="utf-8")
        articulos = extraer_articulos(texto, doc["patron"])

        print(f"\n{doc['doc_id']}")
        print(f"  Artículos detectados: {len(articulos)}")

        chunks_doc = []
        for i, art in enumerate(articulos):
            num = extraer_numero_articulo(art["titulo"])
            chunk_id = f"{doc['doc_id']}_art_{num.lower()}"

            chunk = {
                "chunk_id": chunk_id,
                "doc_id": doc["doc_id"],
                "tipo": doc["tipo"],
                "subtipo": doc["subtipo"],
                "materia": doc["materia"],
                "articulo": num,
                "titulo": art["titulo"],
                "chunk_index": i,
                "texto": art["texto"],
                "chars": len(art["texto"]),
            }

            chunks_doc.append(chunk)
            todos_chunks.append(chunk)

            chunk_path = CHUNKS_DIR / f"{chunk_id}.json"
            chunk_path.write_text(
                json.dumps(chunk, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        consolidated_path = CHUNKS_DIR / f"{doc['doc_id']}_chunks.json"
        consolidated_path.write_text(
            json.dumps(chunks_doc, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"  Chunks guardados: {len(chunks_doc)}")
        print(f"  Consolidado: {consolidated_path.name}")

    print("\n" + "=" * 60)
    print(f"TOTAL: {len(todos_chunks)} chunks de normativa generados")
    print("=" * 60)


if __name__ == "__main__":
    main()
