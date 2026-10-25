"""Servidor HTTP mínimo para receber e indexar documentos da API."""

from __future__ import annotations

import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .indexing import extract_chunk_and_persist_document


# /**
#  * Processa o contrato JSON enviado pela API e confirma a persistência dos chunks.
#  * Existe para oferecer uma ponte HTTP pequena sem adicionar framework ao serviço Python.
#  * Histórico: v1 — cria o endpoint de indexação e o health check.
#  * v2 — recebe o modelo `Document` serializado pela API e informa o backend usado.
#  */
class IndexingRequestHandler(BaseHTTPRequestHandler):
    """Recebe requisições de indexação do serviço NestJS."""

    # /** Histórico: v1 — responde ao health check do Compose. */
    def do_GET(self) -> None:
        if self.path != "/health":
            self._send_json(404, {"error": "Not found"})
            return
        self._send_json(200, {"status": "ok"})

    # /**
    #  * Valida e indexa o payload de um documento.
    #  * Histórico: v1 — adiciona POST `/index` com arquivo temporário UTF-8.
    #  */
    def do_POST(self) -> None:
        if self.path != "/index":
            self._send_json(404, {"error": "Not found"})
            return

        try:
            payload = self._read_payload()
            raw_document = payload.get("document")
            if not isinstance(raw_document, dict):
                raise ValueError("document is required")
            document_id = self._required_string(raw_document, "id")
            project_id = self._required_string(raw_document, "projectId")
            file_name = self._required_string(raw_document, "name")
            content = self._required_string(raw_document, "content")
            suffix = Path(file_name).suffix.lower()
            if suffix not in {".md", ".txt"}:
                raise ValueError("Only .md and .txt files are supported")

            with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=suffix) as file:
                file.write(content)
                file.flush()
                chunks = extract_chunk_and_persist_document(
                    document_id,
                    file.name,
                    project_id=project_id,
                )
            self._send_json(
                200,
                {
                    "documentId": document_id,
                    "chunks": len(chunks),
                    "backend": os.environ.get("VECTOR_STORE_BACKEND", "postgres"),
                },
            )
        except (ValueError, json.JSONDecodeError) as error:
            self._send_json(400, {"error": str(error)})
        except Exception as error:  # pragma: no cover - boundary protection
            self._send_json(500, {"error": str(error)})

    # /** Histórico: v1 — limita o corpo recebido para proteger o processo. */
    def _read_payload(self) -> dict[str, object]:
        length = int(self.headers.get("content-length", "0"))
        max_bytes = int(os.environ.get("AI_MAX_REQUEST_BYTES", 5 * 1024 * 1024))
        if length <= 0 or length > max_bytes:
            raise ValueError("Request body size is invalid")
        raw_body = self.rfile.read(length)
        payload = json.loads(raw_body.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError("Request body must be an object")
        return payload

    # /** Histórico: v1 — centraliza a validação de strings obrigatórias. */
    @staticmethod
    def _required_string(payload: dict[str, object], key: str) -> str:
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key} is required")
        return value

    # /** Histórico: v1 — serializa respostas JSON do boundary HTTP. */
    def _send_json(self, status: int, payload: dict[str, object]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # /** Histórico: v1 — evita ruído de logs em testes e no serviço local. */
    def log_message(self, format: str, *args: object) -> None:
        return


# /** Histórico: v1 — inicia o servidor configurado por ambiente. */
def serve() -> None:
    """Inicia o endpoint de indexação Python."""

    host = os.environ.get("AI_HOST", "0.0.0.0")
    port = int(os.environ.get("AI_PORT", "8000"))
    server = ThreadingHTTPServer((host, port), IndexingRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    serve()
