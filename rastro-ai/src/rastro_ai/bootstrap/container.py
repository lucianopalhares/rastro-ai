"""Composição explícita dos componentes usados pelo runtime da IA."""

from __future__ import annotations

from dataclasses import dataclass
from os import environ

from ..document_indexing.application.ports import VectorStore
from ..document_indexing.application.use_cases.answer_question import (
    AnswerQuestionUseCase,
)
from ..document_indexing.application.use_cases.index_document import IndexDocumentUseCase
from ..document_indexing.application.use_cases.retrieve_chunks import RetrieveChunksUseCase
from ..document_indexing.infrastructure.chunking.langchain_text_chunker import (
    LangChainTextChunker,
)
from ..document_indexing.infrastructure.embeddings.openai_embedding_repository import (
    OpenAIEmbeddingRepository,
)
from ..document_indexing.infrastructure.extraction.utf8_file_text_extractor import (
    Utf8FileTextExtractor,
)
from ..document_indexing.infrastructure.retrieval.postgres_vector_store import (
    PostgresVectorStore,
)


# /**
#  * Agrupa as dependências necessárias para extrair e dividir documentos.
#  * Existe para manter a criação do caso de uso fora das fachadas públicas e permitir
#  * que runtime, testes e evaluation escolham suas próprias implementações.
#  * Histórico: v1 — cria o primeiro composition root do serviço Python.
#  */
@dataclass(frozen=True, slots=True)
class IndexingContainer:
    """Expõe as dependências compostas para o fluxo de indexação."""

    text_extractor: Utf8FileTextExtractor
    text_chunker: LangChainTextChunker
    index_document: IndexDocumentUseCase


# /**
#  * Agrupa o vector store e os casos de uso de consulta e resposta.
#  * Existe para impedir que módulos públicos criem estado global durante o import.
#  * Histórico: v1 — cria o container explícito do fluxo de retrieval.
#  */
@dataclass(frozen=True, slots=True)
class RetrievalContainer:
    """Expõe as dependências compostas para retrieval e respostas."""

    vector_store: VectorStore
    retrieve_chunks: RetrieveChunksUseCase
    answer_question: AnswerQuestionUseCase


# /**
#  * Constrói as dependências determinísticas de extração, chunking e indexação.
#  * Existe para centralizar a composição sem exigir configuração de banco ou provider.
#  * Histórico: v1 — substitui instâncias globais da fachada de indexação.
#  */
def build_indexing_container() -> IndexingContainer:
    """Retorna um container de indexação sem inicializar infraestrutura externa."""

    text_extractor = Utf8FileTextExtractor()
    text_chunker = LangChainTextChunker()
    return IndexingContainer(
        text_extractor=text_extractor,
        text_chunker=text_chunker,
        index_document=IndexDocumentUseCase(text_extractor, text_chunker),
    )


# /**
#  * Constrói o backend persistente e os casos de uso de consulta.
#  * Existe para validar a configuração somente quando o fluxo vetorial é solicitado,
#  * preservando a importação segura das fachadas e mantendo o backend PostgreSQL obrigatório.
#  * Histórico: v1 — move a seleção do backend para o composition root.
#  */
def build_retrieval_container() -> RetrievalContainer:
    """Retorna o container vetorial configurado explicitamente pelo ambiente."""

    backend = environ.get("VECTOR_STORE_BACKEND", "").strip().casefold()
    if backend != "postgres":
        raise ValueError("VECTOR_STORE_BACKEND must be 'postgres'")

    vector_store = PostgresVectorStore.from_environment(
        OpenAIEmbeddingRepository.from_environment()
    )
    retrieve_chunks = RetrieveChunksUseCase(vector_store)
    return RetrievalContainer(
        vector_store=vector_store,
        retrieve_chunks=retrieve_chunks,
        answer_question=AnswerQuestionUseCase(retrieve_chunks),
    )

