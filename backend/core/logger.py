"""
backend/core/logger.py
Bloque 10 — Logging de consultas del sistema.
Registra cada consulta, documentos recuperados y resultado en un archivo de log.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "consultas.jsonl"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "sistema.log", encoding="utf-8"),
        logging.StreamHandler(),
    ]
)

logger = logging.getLogger("juris-ai")


def log_consulta(
    consulta: str,
    chunks_usados: int,
    docs_recuperados: list[str],
    chars_respuesta: int,
    duracion_ms: int,
):
    """Registra una consulta completada en el archivo de log JSONL."""
    entrada = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "consulta": consulta,
        "chunks_usados": chunks_usados,
        "docs_recuperados": docs_recuperados,
        "chars_respuesta": chars_respuesta,
        "duracion_ms": duracion_ms,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entrada, ensure_ascii=False) + "\n")

    logger.info(f"Consulta registrada | chunks={chunks_usados} | {duracion_ms}ms | '{consulta[:60]}'")
