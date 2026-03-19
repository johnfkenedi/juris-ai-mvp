"""
schemas/consulta.py
Modelos Pydantic para el endpoint de consulta jurídica.
"""

from pydantic import BaseModel


class ConsultaRequest(BaseModel):
    consulta: str


class ReferenciaItem(BaseModel):
    doc_id: str
    score: float
    tipo: str
    materia: str
    preview: str


class ConsultaResponse(BaseModel):
    consulta: str
    respuesta: str
    referencias: list[ReferenciaItem]
    chunks_usados: int
