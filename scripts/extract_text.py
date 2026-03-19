"""
extract_text.py
Bloque 4 — Extracción de texto del corpus jurídico.
Lee PDFs de data/raw/ y guarda texto limpio en data/processed/.
"""

import pdfplumber
from pathlib import Path

RAW_DIRS = [
    Path("data/raw/jurisprudencia"),
    Path("data/raw/normativa"),
]
OUTPUT_DIR = Path("data/processed")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrae texto de todas las páginas de un PDF usando pdfplumber."""
    pages_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text.strip())
    return "\n\n".join(pages_text)


def main():
    print("=" * 60)
    print("EXTRACCIÓN DE TEXTO — CORPUS JURÍDICO MVP 1")
    print("=" * 60)

    resultados = []

    for raw_dir in RAW_DIRS:
        if not raw_dir.exists():
            print(f"[AVISO] Directorio no encontrado: {raw_dir}")
            continue

        pdfs = sorted(raw_dir.glob("*.pdf"))
        if not pdfs:
            print(f"[AVISO] Sin PDFs en: {raw_dir}")
            continue

        print(f"\nProcesando: {raw_dir}")
        print("-" * 40)

        for pdf_path in pdfs:
            try:
                texto = extract_text_from_pdf(pdf_path)
                chars = len(texto)
                lineas = texto.count("\n")

                # Guardar como .txt con mismo nombre base
                output_path = OUTPUT_DIR / (pdf_path.stem + ".txt")
                output_path.write_text(texto, encoding="utf-8")

                estado = "OK" if chars > 100 else "ADVERTENCIA: texto muy corto"
                print(f"  [{estado}] {pdf_path.name}")
                print(f"         chars: {chars:,}  |  líneas: {lineas:,}  →  {output_path.name}")

                resultados.append({
                    "archivo": pdf_path.name,
                    "chars": chars,
                    "estado": estado,
                })

            except Exception as e:
                print(f"  [ERROR] {pdf_path.name}: {e}")
                resultados.append({
                    "archivo": pdf_path.name,
                    "chars": 0,
                    "estado": f"ERROR: {e}",
                })

    print("\n" + "=" * 60)
    print(f"RESUMEN: {len(resultados)} archivos procesados")
    ok = sum(1 for r in resultados if r["estado"] == "OK")
    print(f"  OK:          {ok}")
    print(f"  Con problema: {len(resultados) - ok}")
    print("=" * 60)
    print(f"\nTextos guardados en: {OUTPUT_DIR.resolve()}")


if __name__ == "__main__":
    main()
