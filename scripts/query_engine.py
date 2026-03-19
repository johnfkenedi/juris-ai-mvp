"""
query_engine.py
Bloque 4 — Motor de consulta jurídica MVP 1.
Flujo completo: consulta → retrieval BM25 → prompt → respuesta → referencias.
Modo actual: respuesta simulada (stub). Para activar OpenAI real,
descomentar la sección marcada con TODO y comentar el stub.
"""

import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi

# --- Configuración ---
CHUNKS_FILE = Path("data/processed/chunks/jurisprudencia_chunks.json")
TOP_K = 3
MAX_CHARS_CONTEXTO = 12000  # límite de contexto enviado al modelo


# --- Tokenización (igual que retrieval_bm25.py) ---
def tokenize(text: str) -> list[str]:
    stopwords = {
        "de", "la", "el", "en", "y", "a", "los", "las", "del", "un", "una",
        "con", "por", "que", "se", "no", "es", "al", "su", "lo", "le", "o",
        "para", "como", "pero", "si", "son", "has", "fue", "ser", "esta",
        "este", "esto", "entre", "sobre", "ante", "dicho", "dicha", "mismo",
    }
    tokens = re.findall(r"[a-záéíóúüñ]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]


# --- Carga e índice ---
def cargar_chunks(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def construir_indice(chunks: list[dict]) -> BM25Okapi:
    corpus_tokens = [tokenize(chunk["texto"]) for chunk in chunks]
    return BM25Okapi(corpus_tokens)


# --- Retrieval ---
def recuperar_chunks(consulta: str, chunks: list[dict], indice: BM25Okapi, top_k: int) -> list[dict]:
    tokens = tokenize(consulta)
    scores = indice.get_scores(tokens)
    ranking = sorted(
        [{"chunk": chunks[i], "score": round(float(s), 4)} for i, s in enumerate(scores)],
        key=lambda x: x["score"],
        reverse=True,
    )
    return [r for r in ranking[:top_k] if r["score"] > 0.0]


# --- Construcción del prompt ---
def construir_prompt(consulta: str, chunks_recuperados: list[dict]) -> str:
    contexto_partes = []
    chars_acumulados = 0

    for i, r in enumerate(chunks_recuperados, 1):
        texto = r["chunk"]["texto"]
        if chars_acumulados + len(texto) > MAX_CHARS_CONTEXTO:
            break
        contexto_partes.append(f"[DOCUMENTO {i} — {r['chunk']['doc_id']}]\n{texto}")
        chars_acumulados += len(texto)

    contexto = "\n\n---\n\n".join(contexto_partes)

    prompt = f"""Eres un asistente jurídico especializado en derecho administrativo-fiscal mexicano.

Tu tarea es responder la siguiente consulta basándote ÚNICAMENTE en los documentos jurídicos proporcionados.
No inventes información. Si los documentos no contienen suficiente información para responder, indícalo.
Cita los documentos relevantes al final de tu respuesta.

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
    return prompt


# --- Generación de respuesta ---
def generar_respuesta(prompt: str, consulta: str, chunks_recuperados: list[dict]) -> str:
    # TODO: reemplazar este stub por llamada real a OpenAI cuando haya saldo
    # from openai import OpenAI
    # client = OpenAI()  # lee OPENAI_API_KEY del entorno automáticamente
    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.1,
    # )
    # return response.choices[0].message.content

    # --- STUB: respuesta simulada para desarrollo sin API ---
    docs_usados = [r["chunk"]["doc_id"] for r in chunks_recuperados]
    return (
        f"[RESPUESTA SIMULADA — pendiente conexión OpenAI]\n\n"
        f"Consulta recibida: '{consulta}'\n\n"
        f"Documentos que se enviarían al modelo:\n"
        + "\n".join(f"  - {d}" for d in docs_usados)
        + "\n\nCuando se active OpenAI, aquí aparecerá la respuesta fundamentada."
    )


# --- Construcción de referencias visibles ---
def construir_referencias(chunks_recuperados: list[dict]) -> list[dict]:
    referencias = []
    for r in chunks_recuperados:
        chunk = r["chunk"]
        referencias.append({
            "doc_id": chunk["doc_id"],
            "score": r["score"],
            "tipo": chunk["tipo"],
            "materia": chunk["materia"],
            "preview": chunk["texto"][:200] + "...",
        })
    return referencias


# --- Motor principal ---
def consultar(consulta: str, chunks: list[dict], indice: BM25Okapi) -> dict:
    chunks_recuperados = recuperar_chunks(consulta, chunks, indice, TOP_K)

    if not chunks_recuperados:
        return {
            "consulta": consulta,
            "respuesta": "No se encontraron documentos relevantes para esta consulta.",
            "referencias": [],
            "chunks_usados": 0,
        }

    prompt = construir_prompt(consulta, chunks_recuperados)
    respuesta = generar_respuesta(prompt, consulta, chunks_recuperados)
    referencias = construir_referencias(chunks_recuperados)

    return {
        "consulta": consulta,
        "respuesta": respuesta,
        "referencias": referencias,
        "chunks_usados": len(chunks_recuperados),
        "prompt_chars": len(prompt),
    }


# --- Ejecución de prueba ---
def main():
    print("=" * 60)
    print("MOTOR DE CONSULTA JURÍDICA — MVP 1")
    print("=" * 60)

    chunks = cargar_chunks(CHUNKS_FILE)
    indice = construir_indice(chunks)
    print(f"Corpus cargado: {len(chunks)} documentos\n")

    consultas_prueba = [
        "¿Cuáles son los límites legales de una visita domiciliaria?",
        "¿Qué pasa si la autoridad no presentó el crédito fiscal a tiempo?",
        "¿Cuándo prescribe la facultad de cobro del SAT?",
    ]

    for consulta in consultas_prueba:
        print(f"\nCONSULTA: {consulta}")
        print("-" * 60)
        resultado = consultar(consulta, chunks, indice)
        print(f"Chunks usados: {resultado['chunks_usados']}")
        print(f"Prompt chars:  {resultado.get('prompt_chars', 'N/A')}")
        print(f"\nRESPUESTA:\n{resultado['respuesta']}")
        print(f"\nREFERENCIAS:")
        for ref in resultado["referencias"]:
            print(f"  [{ref['score']}] {ref['doc_id']}")
            print(f"  {ref['preview'][:100]}...")
        print()


if __name__ == "__main__":
    main()
