from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from rastro_ai.document_indexing.application.use_cases.index_document import IndexDocumentUseCase
from rastro_ai.document_indexing.domain.services import chunk_text
from rastro_ai.document_indexing.infrastructure.extraction.utf8_file_text_extractor import (
    Utf8FileTextExtractor,
)
from rastro_ai.indexing import extract_text, index_document


class IndexingTests(unittest.TestCase):
    def test_extract_text_normalizes_utf8_markdown(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "meeting.md"
            path.write_bytes("\ufeffLinha 1\r\n\r\n\r\nLinha 2  \r\n".encode("utf-8"))

            self.assertEqual(extract_text(path), "Linha 1\n\nLinha 2")


    def test_extract_text_rejects_unsupported_and_empty_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            unsupported = Path(directory) / "meeting.pdf"
            unsupported.write_text("texto", encoding="utf-8")
            empty = Path(directory) / "empty.txt"
            empty.write_text("\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Only"):
                extract_text(unsupported)
            with self.assertRaisesRegex(ValueError, "required"):
                extract_text(empty)


    def test_chunk_text_is_reproducible_and_keeps_offsets(self) -> None:
        text = "A" * 80 + " " + "B" * 80 + " " + "C" * 80

        first = chunk_text(text, document_id="doc-1", chunk_size=100, overlap=20)
        second = chunk_text(text, document_id="doc-1", chunk_size=100, overlap=20)

        self.assertEqual(first, second)
        self.assertEqual([chunk.index for chunk in first], list(range(len(first))))
        self.assertTrue(all(text[chunk.start_offset : chunk.end_offset] == chunk.content for chunk in first))
        self.assertTrue(all(chunk.document_id == "doc-1" for chunk in first))


    def test_chunk_text_validates_configuration(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive"):
            chunk_text("text", document_id="doc-1", chunk_size=0)
        with self.assertRaisesRegex(ValueError, "between"):
            chunk_text("text", document_id="doc-1", chunk_size=10, overlap=10)


    def test_index_document_extracts_and_chunks_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "meeting.txt"
            path.write_text("Decisão: usar PostgreSQL.\n" * 20, encoding="utf-8")

            chunks = index_document("doc-1", path, chunk_size=60, overlap=10)

            self.assertGreater(len(chunks), 1)
            self.assertTrue(chunks[0].content.startswith("Decisão"))
            self.assertTrue(chunks[-1].content.endswith("PostgreSQL."))

    def test_use_case_depends_on_extractor_port(self) -> None:
        class InMemoryExtractor:
            def extract(self, path: str) -> str:
                self.path = path
                return "Conteúdo de teste"

        extractor = InMemoryExtractor()
        use_case = IndexDocumentUseCase(extractor)

        chunks = use_case.execute("doc-1", "ignored.txt", chunk_size=100, overlap=10)

        self.assertEqual(extractor.path, "ignored.txt")
        self.assertEqual(chunks[0].content, "Conteúdo de teste")

    def test_infrastructure_adapter_is_composable(self) -> None:
        self.assertIsInstance(Utf8FileTextExtractor(), Utf8FileTextExtractor)


if __name__ == "__main__":
    unittest.main()
