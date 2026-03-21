"use client";

import { useState } from "react";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

interface Referencia {
  doc_id: string;
  score: number;
  tipo: string;
  materia: string;
  preview: string;
}

interface ResultadoConsulta {
  consulta: string;
  respuesta: string;
  referencias: Referencia[];
  chunks_usados: number;
}

export default function Home() {
  const [consulta, setConsulta] = useState("");
  const [resultado, setResultado] = useState<ResultadoConsulta | null>(null);
  const [cargando, setCargando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function buscar() {
    if (!consulta.trim()) return;
    setCargando(true);
    setError(null);
    setResultado(null);

    try {
      const res = await fetch(`${API_BASE}/api/consulta`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ consulta }),
      });
      if (!res.ok) throw new Error(`Error del servidor: ${res.status}`);
      const data: ResultadoConsulta = await res.json();
      setResultado(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "Error desconocido");
    } finally {
      setCargando(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      buscar();
    }
  }

  return (
    <main style={styles.main}>
      <div style={styles.container}>

{/* Header */}
        <div style={styles.header}>
          <div style={styles.headerTop}>
            <img src="/logo.jpg" alt="JFCN" style={styles.logo} />
            <div style={styles.headerTexto}>
              <div style={styles.headerBadges}>
                <span style={styles.badge}>MVP 1</span>
                <span style={styles.badgeMateria}>Administrativo · Fiscal</span>
              </div>
              <h1 style={styles.titulo}>Buscador de Jurisprudencia JFCN</h1>
              <p style={styles.subtitulo}>
                Inteligencia Fiscal del Despacho — Corpus jurisprudencial controlado
              </p>
            </div>
          </div>
        </div>

        {/* Search */}
        <div style={styles.searchBox}>
          <textarea
            style={styles.textarea}
            placeholder="Escribe tu consulta jurídica... (Enter para buscar)"
            value={consulta}
            onChange={(e) => setConsulta(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={4}
          />
          <button
            style={{ ...styles.boton, opacity: cargando ? 0.7 : 1 }}
            onClick={buscar}
            disabled={cargando}
          >
            {cargando ? "Consultando..." : "Consultar"}
          </button>
        </div>

        {/* Error */}
        {error && (
          <div style={styles.errorBox}>
            <strong>Error:</strong> {error}
          </div>
        )}

        {/* Resultado */}
        {resultado && (
          <div style={styles.resultado}>

            {/* Respuesta */}
            <div style={styles.seccion}>
              <div style={styles.seccionHeader}>
                <span style={styles.seccionLabel}>Respuesta</span>
                <span style={styles.seccionMeta}>
                  {resultado.chunks_usados} documento{resultado.chunks_usados !== 1 ? "s" : ""} consultado{resultado.chunks_usados !== 1 ? "s" : ""}
                </span>
              </div>
              <p style={styles.respuestaTexto}>{resultado.respuesta}</p>
            </div>

            {/* Referencias */}
            {resultado.referencias.length > 0 && (
              <div style={styles.seccion}>
                <div style={styles.seccionHeader}>
                  <span style={styles.seccionLabel}>Fuentes</span>
                </div>
                <div style={styles.referencias}>
                  {resultado.referencias.map((ref, index) => (
                    <div key={`${ref.doc_id}-${index}`} style={styles.refCard}>
                      <div style={styles.refHeader}>
                        <span style={styles.refDocId}>{ref.doc_id}</span>
                        <span style={styles.refScore}>relevancia {ref.score}</span>
                      </div>
                      <div style={styles.refMeta}>
                        {ref.tipo} · {ref.materia}
                      </div>
                      <p style={styles.refPreview}>{ref.preview}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        )}

        {/* Footer */}
        <div style={styles.footer}>
          Sistema en fase de prueba controlada · Las respuestas son orientativas y deben ser verificadas por un profesional
        </div>

      </div>
    </main>
  );
}

const styles: Record<string, React.CSSProperties> = {
  main: {
    minHeight: "100vh",
    padding: "48px 16px",
    background: "#0f1117",
  },
  container: {
    maxWidth: 820,
    margin: "0 auto",
    display: "flex",
    flexDirection: "column",
    gap: 28,
  },
  header: {
    borderBottom: "1px solid #2a2d3a",
    paddingBottom: 24,
  },
 headerTop: {
    display: "flex",
    flexDirection: "row" as const,
    alignItems: "flex-start",
    gap: 24,
  },
  badge: {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: "1px",
    padding: "3px 10px",
    background: "#1e3a5f",
    color: "#60a5fa",
    borderRadius: 4,
    textTransform: "uppercase" as const,
  },
  badgeMateria: {
    fontSize: 11,
    fontWeight: 600,
    letterSpacing: "0.5px",
    padding: "3px 10px",
    background: "#1a2a1a",
    color: "#4ade80",
    borderRadius: 4,
  },
  titulo: {
    fontSize: 32,
    fontWeight: 800,
    color: "#f1f5f9",
    letterSpacing: "-0.5px",
    marginBottom: 8,
  },
  subtitulo: {
    fontSize: 14,
    color: "#64748b",
    letterSpacing: "0.2px",
  },
logo: {
    height: 110,
    width: "auto",
    objectFit: "contain" as const,
    flexShrink: 0,
  },
headerTexto: {
    display: "flex",
    flexDirection: "column" as const,
    gap: 6,
    justifyContent: "center",
  },
  headerBadges: {
    display: "flex",
    gap: 8,
    marginBottom: 14,
  },
  searchBox: {
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  textarea: {
    width: "100%",
    padding: "16px 18px",
    fontSize: 16,
    lineHeight: "1.6",
    border: "1.5px solid #2a2d3a",
    borderRadius: 10,
    resize: "vertical",
    fontFamily: "inherit",
    outline: "none",
    background: "#161920",
    color: "#f1f5f9",
  },
  boton: {
    alignSelf: "flex-end",
    padding: "12px 36px",
    fontSize: 15,
    fontWeight: 700,
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    letterSpacing: "0.3px",
  },
  errorBox: {
    padding: "14px 18px",
    background: "#1f1215",
    border: "1px solid #7f1d1d",
    borderRadius: 8,
    fontSize: 14,
    color: "#fca5a5",
  },
  resultado: {
    display: "flex",
    flexDirection: "column",
    gap: 20,
  },
  seccion: {
    background: "#161920",
    borderRadius: 12,
    padding: "22px 24px",
    border: "1px solid #2a2d3a",
  },
  seccionHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 16,
  },
  seccionLabel: {
    fontSize: 11,
    fontWeight: 700,
    letterSpacing: "1.5px",
    textTransform: "uppercase" as const,
    color: "#60a5fa",
  },
  seccionMeta: {
    fontSize: 12,
    color: "#475569",
  },
  respuestaTexto: {
    fontSize: 16,
    lineHeight: 1.8,
    color: "#cbd5e1",
    whiteSpace: "pre-wrap",
  },
  referencias: {
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  refCard: {
    padding: "14px 16px",
    background: "#0f1117",
    border: "1px solid #1e2433",
    borderRadius: 8,
  },
  refHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 4,
  },
  refDocId: {
    fontSize: 12,
    fontWeight: 700,
    fontFamily: "monospace",
    color: "#94a3b8",
  },
  refScore: {
    fontSize: 11,
    color: "#475569",
    fontFamily: "monospace",
  },
  refMeta: {
    fontSize: 11,
    color: "#4ade80",
    marginBottom: 8,
    fontWeight: 600,
  },
  refPreview: {
    fontSize: 13,
    color: "#64748b",
    lineHeight: 1.6,
    whiteSpace: "pre-wrap",
  },
  footer: {
    fontSize: 11,
    color: "#334155",
    textAlign: "center" as const,
    paddingTop: 8,
    borderTop: "1px solid #1e2433",
    lineHeight: 1.6,
  },
};