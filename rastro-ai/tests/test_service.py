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

        with patch("rastro_ai.service.index_document_in_store", return_value=(object(),)) as index:
            handler.do_POST()

        self.assertEqual(handler.response_status, 200)
        index.assert_called_once()


if __name__ == "__main__":
    unittest.main()
