"""
api/consulta.py
Endpoint POST /api/consulta — retrieval hibrido BM25 + embeddings semanticos.
"""

import json
import math
import re
from pathlib import Path
from fastapi import APIRouter, HTTPException
from rank_bm25 import BM25Okapi
from openai import OpenAI

from backend.core.settings import settings
from backend.core.logger import log_consulta
from backend.schemas.consulta import ConsultaRequest, ConsultaResponse, ReferenciaItem

router = APIRouter()

CHUNKS_FILES = [
    Path("data/processed/chunks/jurisprudencia_chunks.json"),
    Path("data/processed/chunks/norm_001_cff_codigo_fiscal_federacion_chunks.json"),
    Path("data/processed/chunks/norm_002_lfpca_procedimiento_contencioso_administrativo_chunks.json"),
    Path("data/processed/chunks/norm_003_lfpa_procedimiento_administrativo_chunks.json"),
    Path("data/processed/chunks/norm_005_cfpc_codigo_federal_procedimientos_civiles_chunks.json"),
]
EMBEDDINGS_FILE = Path("data/processed/chunks/jurisprudencia_embeddings.json")
MODELO_EMBEDDING = "text-embedding-3-small"
MODELO_CHAT = "gpt-4o-mini"
TOP_K = 3
MAX_CHARS_CONTEXTO = 12000
PESO_BM25 = 0.5
PESO_SEMANTICO = 0.5


def tokenize(text: str) -> list[str]:
    stopwords = {
        "de", "la", "el", "en", "y", "a", "los", "las", "del", "un", "una",
        "con", "por", "que", "se", "no", "es", "al", "su", "lo", "le", "o",
        "para", "como", "pero", "si", "son", "has", "fue", "ser", "esta",
        "este", "esto", "entre", "sobre", "ante", "dicho", "dicha", "mismo",
    }
    tokens = re.findall(r"[a-záéíóúüñ]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]


def coseno(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(x * x for x in b))
    return dot / (na * nb) if na and nb else 0.0


_chunks: list[dict] = []
_embeddings: list[dict] = []
_indice: BM25Okapi | None = None


def _inicializar():
    global _chunks, _embeddings, _indice
    _chunks = []
    for path in CHUNKS_FILES:
        with open(path, encoding="utf-8") as f:
            _chunks.extend(json.load(f))
    with open(EMBEDDINGS_FILE, encoding="utf-8") as f:
        _embeddings = json.load(f)
    corpus_tokens = [tokenize(c["texto"]) for c in _chunks]
    _indice = BM25Okapi(corpus_tokens)


_inicializar()

def _buscar_articulo_directo(consulta: str) -> list[dict] | None:
    """Detecta si la consulta pide un artículo específico y lo recupera directamente."""
    patrones_doc = [
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*cfpc|cfpc.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*procedimientos\s+civiles", "norm_005_cfpc_codigo_federal_procedimientos_civiles"),
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*cff|cff.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*c[oó]digo\s+fiscal", "norm_001_cff_codigo_fiscal_federacion"),
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*lfpca|lfpca.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*contencioso", "norm_002_lfpca_procedimiento_contencioso_administrativo"),
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*lfpa|lfpa.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*procedimiento\s+administrativo", "norm_003_lfpa_procedimiento_administrativo"),
    ]

    consulta_lower = consulta.lower()

    for patron, doc_id in patrones_doc:
        match = re.search(patron, consulta_lower)
        if match:
            num = next(g for g in match.groups() if g is not None)
            chunk_id = f"{doc_id}_art_{num}"
            chunk = next((c for c in _chunks if c["chunk_id"] == chunk_id), None)
            if chunk:
                return [{"chunk": chunk, "score": 1.0, "score_bm25": 1.0}]

    return None

def _buscar_articulo_directo(consulta: str) -> list[dict] | None:
    patrones_doc = [
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*cfpc|cfpc.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*procedimientos\s+civiles", "norm_005_cfpc_codigo_federal_procedimientos_civiles"),
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*cff|cff.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*c[oó]digo\s+fiscal", "norm_001_cff_codigo_fiscal_federacion"),
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*lfpca|lfpca.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*contencioso", "norm_002_lfpca_procedimiento_contencioso_administrativo"),
        (r"art[íi]culo\s+(\d+[\w\-]*)\s+.*lfpa|lfpa.*art[íi]culo\s+(\d+[\w\-]*)|art[íi]culo\s+(\d+[\w\-]*)\s+.*procedimiento\s+administrativo", "norm_003_lfpa_procedimiento_administrativo"),
    ]
    consulta_lower = consulta.lower()
    for patron, doc_id in patrones_doc:
        match = re.search(patron, consulta_lower)
        if match:
            num = next(g for g in match.groups() if g is not None)
            chunk_id = f"{doc_id}_art_{num}"
            chunk = next((c for c in _chunks if c["chunk_id"] == chunk_id), None)
            if chunk:
                return [{"chunk": chunk, "score": 1.0, "score_bm25": 1.0}]
    return None

def _recuperar_hibrido(consulta: str, client: OpenAI) -> list[dict]:
    # IDs con embedding disponible
    embedding_map = {e["chunk_id"]: e["embedding"] for e in _embeddings}

    # Score BM25 sobre todos los chunks
    tokens = tokenize(consulta)
    bm25_scores = _indice.get_scores(tokens)
    bm25_max = max(bm25_scores) if max(bm25_scores) > 0 else 1.0
    bm25_norm = [s / bm25_max for s in bm25_scores]

    # Embedding de la consulta
    resp = client.embeddings.create(model=MODELO_EMBEDDING, input=consulta)
    vector_consulta = resp.data[0].embedding

    combinados = []
    for i, chunk in enumerate(_chunks):
        bm25_n = bm25_norm[i]
        chunk_id = chunk["chunk_id"]

        if chunk_id in embedding_map:
            sem = coseno(vector_consulta, embedding_map[chunk_id])
            sem_score = sem
            score_final = PESO_BM25 * bm25_n + PESO_SEMANTICO * sem_score
        else:
            # Sin embedding: solo BM25
            score_final = bm25_n

        combinados.append({
            "chunk": chunk,
            "score": round(score_final, 4),
            "score_bm25": round(float(bm25_scores[i]), 4),
        })

    combinados.sort(key=lambda x: x["score"], reverse=True)
    return [r for r in combinados[:TOP_K] if r["score"] > 0.0]

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


@router.post("/consulta", response_model=ConsultaResponse)
def consulta(request: ConsultaRequest):
    if request.access_key != settings.access_key:
        raise HTTPException(status_code=401, detail="Clave de acceso incorrecta.")
    if not request.consulta.strip():
        raise HTTPException(status_code=400, detail="La consulta no puede estar vacía.")
    client = OpenAI(api_key=settings.openai_api_key)
    recuperados = _buscar_articulo_directo(request.consulta) or _recuperar_hibrido(request.consulta, client)

    if not recuperados:
        return ConsultaResponse(
            consulta=request.consulta,
            respuesta="No se encontraron documentos relevantes para esta consulta.",
            referencias=[],
            chunks_usados=0,
        )

    import time
    inicio = time.time()

    prompt = _construir_prompt(request.consulta, recuperados)

    response = client.chat.completions.create(
        model=MODELO_CHAT,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    respuesta = response.choices[0].message.content

    duracion_ms = int((time.time() - inicio) * 1000)

    log_consulta(
        consulta=request.consulta,
        chunks_usados=len(recuperados),
        docs_recuperados=[r["chunk"]["doc_id"] for r in recuperados],
        chars_respuesta=len(respuesta),
        duracion_ms=duracion_ms,
    )

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