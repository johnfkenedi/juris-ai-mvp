"""
api/consulta.py
Endpoint POST /api/consulta — recibe una consulta jurídica y
devuelve respuesta + referencias usando el motor BM25.
"""

import json
import re
import sys
from pathlib import Path
from fastapi import APIRouter, HTTPException
from rank_bm25 import BM25Okapi

from backend.schemas.consulta import ConsultaRequest, ConsultaResponse, ReferenciaItem

router = APIRouter()

# --- Rutas del corpus ---
CHUNKS_FILE = Path("data/processed/chunks/jurisprudencia_chunks.json")
TOP_K = 3
MAX_CHARS_CONTEXTO = 12000


# --- Tokenización ---
def tokenize(text: str) -> list[str]:
    stopwords = {
        "de", "la", "el", "en", "y", "a", "los", "las", "del", "un", "una",
        "con", "por", "que", "se", "no", "es", "al", "su", "lo", "le", "o",
        "para", "como", "pero", "si", "son", "has", "fue", "ser", "esta",
        "este", "esto", "entre", "sobre", "ante", "dicho", "dicha", "mismo",
    }
    tokens = re.findall(r"[a-záéíóúüñ]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]


# --- Estado del índice (cargado una sola vez al iniciar) ---
_chunks: list[dict] = []
_indice: BM25Okapi | None = None


def _inicializar():
    global _chunks, _indice
    if not CHUNKS_FILE.exists():
        raise RuntimeError(f"No se encontró el archivo de chunks: {CHUNKS_FILE}")
    with open(CHUNKS_FILE, encoding="utf-8") as f:
        _chunks = json.load(f)
    corpus_tokens = [tokenize(c["texto"]) for c in _chunks]
    _indice = BM25Okapi(corpus_tokens)


# Inicializar al importar el módulo
_inicializar()


# --- Lógica de consulta (misma que query_engine.py) ---
def _recuperar(consulta: str) -> list[dict]:
    tokens = tokenize(consulta)
    scores = _indice.get_scores(tokens)
    ranking = sorted(
        [{"chunk": _chunks[i], "score": round(float(s), 4)} for i, s in enumerate(scores)],
        key=lambda x: x["score"],
        reverse=True,
    )
    return [r for r in ranking[:TOP_K] if r["score"] > 0.0]


def _construir_prompt(consulta: str, recuperados: list[dict]) -> str:
    partes = []
    chars = 0
    for i, r in enumerate(recuperados, 1):
        texto = r["chunk"]["texto"]
        if chars + len(texto) > MAX_CHARS_CONTEXTO:
            break
        partes.append(f"[DOCUMENTO {i} — {r['chunk']['doc_id']}]\n{texto}")
        chars += len(texto)
    contexto = "\n\n---\n\n".join(partes)
    return f"""Eres un asistente jurídico especializado en derecho administrativo-fiscal mexicano.

Tu tarea es responder la siguiente consulta basándote ÚNICAMENTE en los documentos jurídicos proporcionados.
No inventes información. Si los documentos no contienen suficiente información para responder, indícalo.

CONSULTA:
{consulta}

DOCUMENTOS DE REFERENCIA:
{contexto}

INSTRUCCIONES DE RESPUESTA:
- Responde en español, de forma clara y directa.
- Fundamenta cada afirmación en el contenido de los documentos.
- Al final incluye una sección "Referencias" con los documentos usados.
- No elabores más allá de lo que dicen los documentos.
"""


def _generar_respuesta(prompt: str, consulta: str, recuperados: list[dict]) -> str:
    # TODO: activar cuando haya saldo OpenAI
    # from openai import OpenAI
    # client = OpenAI()
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.1,
    # )
    # return response.choices[0].message.content
    docs = [r["chunk"]["doc_id"] for r in recuperados]
    return (
        "[RESPUESTA SIMULADA — pendiente conexión OpenAI]\n\n"
        f"Consulta recibida: '{consulta}'\n\n"
        "Documentos que se enviarían al modelo:\n"
        + "\n".join(f"  - {d}" for d in docs)
        + "\n\nCuando se active OpenAI, aquí aparecerá la respuesta fundamentada."
    )


# --- Endpoint ---
@router.post("/consulta", response_model=ConsultaResponse)
def consulta(request: ConsultaRequest):
    if not request.consulta.strip():
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía.")

    recuperados = _recuperar(request.consulta)

    if not recuperados:
        return ConsultaResponse(
            consulta=request.consulta,
            respuesta="No se encontraron documentos relevantes para esta consulta.",
            referencias=[],
            chunks_usados=0,
        )

    prompt = _construir_prompt(request.consulta, recuperados)
    respuesta = _generar_respuesta(prompt, request.consulta, recuperados)

    referencias = [
        ReferenciaItem(
            doc_id=r["chunk"]["doc_id"],
            score=r["score"],
            tipo=r["chunk"]["tipo"],
            materia=r["chunk"]["materia"],
            preview=r["chunk"]["texto"][:200] + "...",
        )
        for r in recuperados
    ]

    return ConsultaResponse(
        consulta=request.consulta,
        respuesta=respuesta,
        referencias=referencias,
        chunks_usados=len(recuperados),
    )
