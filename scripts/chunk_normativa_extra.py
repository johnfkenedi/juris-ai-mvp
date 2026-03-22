"""
scripts/chunk_normativa_extra.py
Bloque 11 — Chunking de LFPA y CFPC.
"""

import json
import re
from pathlib import Path

PROCESSED_DIR = Path("data/processed")
CHUNKS_DIR = Path("data/processed/chunks")
CHUNKS_DIR.mkdir(parents=True, exist_ok=True)

DOCUMENTOS = [
    {
        "doc_id": "norm_003_lfpa_procedimiento_administrativo",
        "tipo": "normativa",
        "subtipo": "ley",
        "materia": "administrativo",
        "patron": r"^Artículo\s+\d+",
    },
    {
        "doc_id": "norm_005_cfpc_codigo_federal_procedimientos_civiles",
        "tipo": "normativa",
        "subtipo": "codigo",
        "materia": "procesal-civil",
        "patron": r"^ARTICULO\s+\d",
    },
]


def extraer_numero_articulo(titulo: str) -> str:
    match = re.search(r"\d+", titulo)
    return match.group(0) if match else "?"


def extraer_articulos(texto: str, patron: str) -> list[dict]:
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


def main():
    print("=" * 60)
    print("CHUNKING NORMATIVA EXTRA — LFPA + CFPC")
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
            chunk_id = f"{doc['doc_id']}_art_{num}"

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
    print(f"TOTAL: {len(todos_chunks)} chunks adicionales generados")
    print("=" * 60)


if __name__ == "__main__":
    main()
