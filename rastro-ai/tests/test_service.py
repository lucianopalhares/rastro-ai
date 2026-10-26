import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from rastro_ai.service import IndexingRequestHandler


class ServiceTests(unittest.TestCase):
    # /**
    #  * Confirma que o boundary HTTP valida o contrato e retorna a quantidade de chunks.
    #  * Histórico: v1 — cobre o POST usado pela API.
    #  */
    def test_index_endpoint_accepts_document_payload(self) -> None:
        payload = json.dumps(
            {
                "document": {
                    "id": "doc-1",
                    "projectId": "project-1",
                    "name": "meeting.md",
                    "content": "# Decisão\nUsar PostgreSQL.",
                    "status": "processing",
                },
            }
        ).encode("utf-8")
        handler = object.__new__(IndexingRequestHandler)
        handler.path = "/index"
        handler.headers = {"content-length": str(len(payload))}
        handler.rfile = io.BytesIO(payload)
        handler.wfile = io.BytesIO()
        handler.requestline = "POST /index HTTP/1.1"
        handler.request_version = "HTTP/1.1"
        handler.command = "POST"
        handler.send_response = lambda status: setattr(handler, "response_status", status)
        handler.send_header = lambda *_args: None
        handler.end_headers = lambda: None

        with patch("rastro_ai.service.extract_chunk_and_persist_document", return_value=(object(),)) as index:
            handler.do_POST()

        self.assertEqual(handler.response_status, 200)
        index.assert_called_once()

    # /**
    #  * Confirma o contrato de busca com filtro de projeto, limite, score e citação.
    #  * Histórico: 023-v1 — publica o boundary HTTP usado pelo Rastro API.
    #  */
    def test_search_endpoint_returns_deterministic_results(self) -> None:
        payload = json.dumps(
            {"projectId": "project-1", "query": "decisão do banco", "limit": 3}
        ).encode("utf-8")
        handler = object.__new__(IndexingRequestHandler)
        handler.path = "/search"
        handler.headers = {"content-length": str(len(payload))}
        handler.rfile = io.BytesIO(payload)
        handler.wfile = io.BytesIO()
        handler.requestline = "POST /search HTTP/1.1"
        handler.request_version = "HTTP/1.1"
        handler.command = "POST"
        handler.send_response = lambda status: setattr(handler, "response_status", status)
        handler.send_header = lambda *_args: None
        handler.end_headers = lambda: None

        chunk = type(
            "Chunk",
            (),
            {
                "document_id": "doc-1",
                "index": 0,
                "content": "Usar PostgreSQL.",
                "start_offset": 0,
                "end_offset": 17,
                "project_id": "project-1",
            },
        )()
        result = type("Retrieved", (), {"chunk": chunk, "score": 0.91})()

        with patch("rastro_ai.service.search_relevant_chunks", return_value=(result,)) as search:
            handler.do_POST()

        self.assertEqual(handler.response_status, 200)
        response = json.loads(handler.wfile.getvalue())
        self.assertEqual(response["results"][0]["score"], 0.91)
        self.assertEqual(response["results"][0]["citation"]["documentId"], "doc-1")
        search.assert_called_once_with("project-1", "decisão do banco", limit=3)


if __name__ == "__main__":
    unittest.main()
