"""
retrieval_bm25.py
Bloque 4 — Retrieval por BM25 sobre el corpus de jurisprudencia.
Carga los chunks, indexa con BM25, recibe una consulta y devuelve
los fragmentos más relevantes con su score.
"""

import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi

CHUNKS_FILE = Path("data/processed/chunks/jurisprudencia_chunks.json")


def tokenize(text: str) -> list[str]:
    """Tokenización simple: minúsculas, solo palabras, sin stopwords básicas."""
    stopwords = {
        "de", "la", "el", "en", "y", "a", "los", "las", "del", "un", "una",
        "con", "por", "que", "se", "no", "es", "al", "su", "lo", "le", "o",
        "para", "como", "pero", "si", "son", "has", "fue", "ser", "esta",
        "este", "esto", "entre", "sobre", "ante", "dicho", "dicha", "mismo",
    }
    tokens = re.findall(r"[a-záéíóúüñ]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]


def cargar_chunks(path: Path) -> list[dict]:
    """Carga el archivo consolidado de chunks."""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def construir_indice(chunks: list[dict]) -> BM25Okapi:
    """Construye el índice BM25 a partir de los chunks."""
    corpus_tokens = [tokenize(chunk["texto"]) for chunk in chunks]
    return BM25Okapi(corpus_tokens)


def buscar(consulta: str, chunks: list[dict], indice: BM25Okapi, top_k: int = 3) -> list[dict]:
    """Busca los top_k chunks más relevantes para la consulta."""
    tokens_consulta = tokenize(consulta)
    scores = indice.get_scores(tokens_consulta)

    resultados = []
    for i, score in enumerate(scores):
        resultados.append({
            "chunk_id": chunks[i]["chunk_id"],
            "doc_id": chunks[i]["doc_id"],
            "score": round(float(score), 4),
            "chars": chunks[i]["chars"],
            "texto_preview": chunks[i]["texto"][:300] + "...",
        })

    resultados.sort(key=lambda x: x["score"], reverse=True)
    return resultados[:top_k]


def main():
    print("=" * 60)
    print("RETRIEVAL BM25 — JURISPRUDENCIA MVP 1")
    print("=" * 60)

    chunks = cargar_chunks(CHUNKS_FILE)
    indice = construir_indice(chunks)
    print(f"Índice construido: {len(chunks)} chunks\n")

    # Consultas de prueba representativas del despacho
    consultas_prueba = [
        "prescripción de créditos fiscales",
        "visita domiciliaria extralimitación nulidad",
        "recurso de revocación confirmativa ficta",
        "duración máxima de la visita domiciliaria",
        "autoridad no puede exhibir documentos que no presentó",
    ]

    for consulta in consultas_prueba:
        print(f"CONSULTA: {consulta}")
        print("-" * 40)
        resultados = buscar(consulta, chunks, indice, top_k=3)
        for i, r in enumerate(resultados, 1):
            print(f"  #{i} score={r['score']:>7.4f}  {r['doc_id']}")
            print(f"       {r['texto_preview'][:120]}...")
        print()

    print("=" * 60)
    print("Retrieval operativo. Listo para integrarse al motor.")
    print("=" * 60)


if __name__ == "__main__":
    main()
