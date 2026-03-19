"""
scripts/generate_embeddings.py
Bloque 7 — Genera embeddings para los chunks de jurisprudencia.
Usa text-embedding-3-small de OpenAI.
Se ejecuta una sola vez y guarda los embeddings en disco.
"""

import json
from pathlib import Path
from openai import OpenAI
from backend.core.settings import settings

CHUNKS_FILE = Path("data/processed/chunks/jurisprudencia_chunks.json")
EMBEDDINGS_FILE = Path("data/processed/chunks/jurisprudencia_embeddings.json")
MODELO_EMBEDDING = "text-embedding-3-small"


def generar_embedding(client: OpenAI, texto: str) -> list[float]:
    """Genera un embedding para un texto dado."""
    response = client.embeddings.create(
        model=MODELO_EMBEDDING,
        input=texto,
    )
    return response.data[0].embedding


def main():
    print("=" * 60)
    print("GENERACIÓN DE EMBEDDINGS — JURISPRUDENCIA MVP 1")
    print("=" * 60)
    print(f"Modelo: {MODELO_EMBEDDING}")

    client = OpenAI(api_key=settings.openai_api_key)

    with open(CHUNKS_FILE, encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Chunks a procesar: {len(chunks)}\n")

    embeddings_data = []

    for chunk in chunks:
        doc_id = chunk["doc_id"]
        texto = chunk["texto"]

        print(f"  Procesando: {doc_id}...")
        vector = generar_embedding(client, texto)

        embeddings_data.append({
            "chunk_id": chunk["chunk_id"],
            "doc_id": doc_id,
            "embedding": vector,
            "dims": len(vector),
        })

        print(f"  OK — vector de {len(vector)} dimensiones")

    EMBEDDINGS_FILE.write_text(
        json.dumps(embeddings_data, ensure_ascii=False),
        encoding="utf-8",
    )

    print()
    print("=" * 60)
    print(f"RESUMEN: {len(embeddings_data)} embeddings generados")
    print(f"Guardados en: {EMBEDDINGS_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
