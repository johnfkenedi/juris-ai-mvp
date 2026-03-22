import json, re
from pathlib import Path
from rank_bm25 import BM25Okapi

chunks = []
for f in [
    "data/processed/chunks/jurisprudencia_chunks.json",
    "data/processed/chunks/norm_001_cff_codigo_fiscal_federacion_chunks.json",
    "data/processed/chunks/norm_002_lfpca_procedimiento_contencioso_administrativo_chunks.json",
    "data/processed/chunks/norm_003_lfpa_procedimiento_administrativo_chunks.json",
    "data/processed/chunks/norm_005_cfpc_codigo_federal_procedimientos_civiles_chunks.json",
]:
    chunks.extend(json.loads(Path(f).read_text(encoding="utf-8")))

print("Total chunks:", len(chunks))

stopwords = {"de","la","el","en","y","a","los","las","del","un","una","con","por","que","se","no","es","al","su","lo","le","o","para","como","pero","si","son","has","fue","ser","esta","este","esto","entre","sobre","ante","dicho","dicha","mismo"}

def tokenize(text):
    tokens = re.findall(r"[a-zA-ZaeiouAEIOUáéíóúüñÁÉÍÓÚÜÑ]+", text.lower())
    return [t for t in tokens if t not in stopwords and len(t) > 2]

corpus = [tokenize(c["texto"]) for c in chunks]
indice = BM25Okapi(corpus)

consultas = [
    "articulo 1 codigo federal procedimientos civiles",
    "procedimientos civiles",
    "ARTICULO 1",
]

for consulta in consultas:
    tokens = tokenize(consulta)
    print("Consulta:", consulta)
    print("Tokens:", tokens)
    scores = indice.get_scores(tokens)
    ranking = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:3]
    for i, score in ranking:
        print("  score=", round(score, 4), "|", chunks[i]["chunk_id"])
    print()