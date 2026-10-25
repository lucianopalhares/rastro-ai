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
from rastro_ai.document_indexing.infrastructure.chunking.langchain_text_chunker import (
    LangChainTextChunker,
)
from unittest.mock import patch

from rastro_ai.indexing import (
    chunk_text as public_chunk_text,
    extract_text,
    index_document,
    index_document_in_store,
)


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
        with self.assertRaisesRegex(ValueError, "max_tokens"):
            chunk_text("text", document_id="doc-1", max_tokens=0)
        with self.assertRaisesRegex(ValueError, "overlap_tokens"):
            chunk_text("text", document_id="doc-1", max_tokens=10, overlap_tokens=10)

    # /**
    #  * Confirma que o modo padrão respeita fronteiras de parágrafos e preserva offsets.
    #  * Histórico: v2 — cobre o chunking estrutural baseado em tokens aproximados.
    #  */
    def test_default_chunking_prefers_markdown_paragraph_boundaries(self) -> None:
        text = "# Decisão\n\n" + " ".join(["PostgreSQL"] * 8) + "\n\n" + "# Próximos passos\n\n" + " ".join(["Validar"] * 8)

        chunks = chunk_text(
            text,
            document_id="doc-1",
            max_tokens=8,
            overlap_tokens=2,
        )

        self.assertGreater(len(chunks), 1)
        self.assertTrue(
            all(text[chunk.start_offset : chunk.end_offset] == chunk.content for chunk in chunks)
        )
        self.assertTrue(any(chunk.content.startswith("# Próximos passos") for chunk in chunks))
        self.assertTrue(all(chunk.project_id == "" for chunk in chunks))

    # /**
    #  * Confirma que o orçamento usa o tokenizer real e funciona com texto Unicode.
    #  * Histórico: v4 — cobre a integração do `tiktoken` com offsets UTF-8.
    #  */
    def test_default_chunking_uses_real_tokenizer_for_unicode(self) -> None:
        text = "Reunião: decisões sobre São Paulo, integração e embeddings. " * 80

        chunks = chunk_text(text, document_id="doc-unicode", max_tokens=40, overlap_tokens=5)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(
            all(text[chunk.start_offset : chunk.end_offset] == chunk.content for chunk in chunks)
        )


    def test_index_document_extracts_and_chunks_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "meeting.txt"
            path.write_text("Decisão: usar PostgreSQL.\n" * 20, encoding="utf-8")

            chunks = index_document("doc-1", path, chunk_size=60, overlap=10)

            self.assertGreater(len(chunks), 1)
            self.assertTrue(chunks[0].content.startswith("Decisão"))
            self.assertTrue(chunks[-1].content.endswith("PostgreSQL."))

    # /**
    #  * Confirma que a fachada pública usa a mesma estratégia LangChain da indexação.
    #  * Existe para impedir divergência entre chamadas diretas e o fluxo de documentos.
    #  * Histórico: v4 — unifica `chunk_text` público com `LangChainTextChunker`.
    #  */
    def test_public_chunk_text_uses_langchain_strategy(self) -> None:
        text = "Decisão sobre PostgreSQL.\n\nPróximos passos de integração."

        chunks = public_chunk_text(
            text,
            document_id="doc-1",
            project_id="project-1",
            max_tokens=8,
            overlap_tokens=2,
        )

        self.assertGreater(len(chunks), 1)
        self.assertTrue(
            all(text[chunk.start_offset : chunk.end_offset] == chunk.content for chunk in chunks)
        )
        self.assertTrue(all(chunk.project_id == "project-1" for chunk in chunks))

    def test_use_case_depends_on_extractor_port(self) -> None:
        class InMemoryExtractor:
            def extract(self, path: str) -> str:
                self.path = path
                return "Conteúdo de teste"

        extractor = InMemoryExtractor()
        use_case = IndexDocumentUseCase(extractor, LangChainTextChunker())

        chunks = use_case.execute("doc-1", "ignored.txt", chunk_size=100, overlap=10)

        self.assertEqual(extractor.path, "ignored.txt")
        self.assertEqual(chunks[0].content, "Conteúdo de teste")

    # /**
    #  * Confirma que o caso de uso depende do contrato injetado e preserva metadados.
    #  * Histórico: v2 — cobre a remoção do acoplamento direto ao serviço de domínio.
    #  */
    def test_use_case_delegates_chunking_to_port(self) -> None:
        class InMemoryExtractor:
            def extract(self, path: str) -> str:
                return "Texto extraído"

        class SpyChunker:
            def __init__(self) -> None:
                self.arguments = None

            def chunk(self, text: str, **kwargs):
                self.arguments = (text, kwargs)
                return chunk_text("resultado", document_id=kwargs["document_id"], chunk_size=100)

        chunker = SpyChunker()
        use_case = IndexDocumentUseCase(InMemoryExtractor(), chunker)

        chunks = use_case.execute(
            "doc-1",
            "ignored.txt",
            project_id="project-1",
            max_tokens=20,
            overlap_tokens=3,
        )

        self.assertEqual(chunks[0].content, "resultado")
        self.assertEqual(chunker.arguments[0], "Texto extraído")
        self.assertEqual(chunker.arguments[1]["project_id"], "project-1")
        self.assertEqual(chunker.arguments[1]["max_tokens"], 20)

    # /**
    #  * Confirma que o adaptador LangChain preserva conteúdo, offsets e projeto.
    #  * Histórico: v2 — cobre a conversão de `Document` para `DocumentChunk`.
    #  */
    def test_langchain_chunker_preserves_offsets_and_project(self) -> None:
        text = "Reunião sobre São Paulo.\n\nPróximos passos de integração."

        chunks = LangChainTextChunker().chunk(
            text,
            document_id="doc-1",
            project_id="project-1",
            max_tokens=8,
            overlap_tokens=2,
        )

        self.assertGreater(len(chunks), 1)
        self.assertEqual([chunk.index for chunk in chunks], list(range(len(chunks))))
        self.assertTrue(all(text[chunk.start_offset : chunk.end_offset] == chunk.content for chunk in chunks))
        self.assertTrue(all(chunk.project_id == "project-1" for chunk in chunks))

    # /**
    #  * Confirma que a operação ponta a ponta envia os chunks ao boundary de persistência.
    #  * Histórico: v1 — cobre a integração entre indexação e persistência.
    #  * Histórico: v2 — deixa de observar a criação implícita do PGVector durante o import;
    #  * a composição do backend passa a ser responsabilidade do container explícito.
    #  */
    def test_index_document_in_store_persists_chunks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "meeting.txt"
            path.write_text("Conteúdo indexável", encoding="utf-8")

            with patch.dict(
                "os.environ",
                {
                    "VECTOR_STORE_BACKEND": "postgres",
                    "DATABASE_URL": "postgresql://test/test",
                    "OPENAI_API_KEY": "test-key",
                },
            ), patch("rastro_ai.retrieval.index_chunks") as index_chunks:
                chunks = index_document_in_store("doc-1", path, project_id="project-1")

            index_chunks.assert_called_once_with(chunks)
            self.assertEqual(chunks[0].project_id, "project-1")

    def test_infrastructure_adapter_is_composable(self) -> None:
        self.assertIsInstance(Utf8FileTextExtractor(), Utf8FileTextExtractor)


if __name__ == "__main__":
    unittest.main()
