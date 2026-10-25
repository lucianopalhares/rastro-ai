# 017/v2 — Nomenclatura clara para busca semântica e persistência

- Versão: `v2`; versão-base: `017/v1` verificada; data: 2026-10-25 -03:00; status: `verified`.
- Aplicação: `/home/dev/dev/ia/rastro-ai/rastro-ai`; arquivos conferidos: fachada, container, casos de uso, vector stores, adapters, testes, evaluation, README e documentação arquitetural.
- Reconciliação: `v1` já distinguia extração/chunking de persistência, mas `retrieval.index_chunks()`, `RetrievalContainer`, `RetrieveChunksUseCase` e os stores ainda tinham nomes genéricos ou ambíguos.
- Decisão: renomear métodos e classes para descrever busca semântica, chunks e adapters; manter o módulo `rastro_ai.retrieval` nesta rodada para reduzir a superfície da mudança.

## O que foi feito

- Renomeados `index_chunks()` para `persist_document_chunks()` e `retrieve_chunks()` para `search_relevant_chunks()`.
- Renomeados `RetrievalContainer`/`build_retrieval_container()` para `SemanticSearchContainer`/`build_semantic_search_container()`.
- Renomeados `RetrieveChunksUseCase`, `PostgresVectorStore`, `InMemoryVectorStore` e `RepositoryEmbeddings` para `SearchRelevantChunksUseCase`, `PostgresChunkVectorStore`, `InMemoryChunkVectorStore` e `LangChainEmbeddingAdapter`.
- Renomeado o fluxo completo para `extract_chunk_and_persist_document()` e atualizados serviço HTTP, exports, testes, evaluation, README e arquitetura.
- O problema resolvido foi a mistura entre persistência, retrieval e busca semântica nos nomes das classes e métodos.

## O que muda na aplicação

- O endpoint HTTP continua recebendo e processando o mesmo documento; apenas os nomes internos da composição e das fachadas mudaram.
- `persist_document_chunks()` agora expressa geração de embeddings e gravação; `search_relevant_chunks()` expressa consulta de relevância.
- `PostgresChunkVectorStore` e `InMemoryChunkVectorStore` deixam explícito que armazenam/buscam chunks, e o adapter LangChain deixa explícita sua função de ponte.
- Não foram alterados filtros por projeto, offsets, scores, embeddings, PGVector, estratégia de chunking, evaluation, custo ou latência esperados.
- Risco conhecido: imports externos dos nomes antigos deixam de funcionar; o módulo `rastro_ai.retrieval` permanece preservado nesta rodada.

## Jornada da aplicação nesta versão

Antes, `retrieval.index_chunks()` parecia executar uma busca, embora persistisse chunks, e `RetrieveChunksUseCase` não deixava claro que retornava resultados relevantes. Agora, a sequência separa preparação, persistência e busca por nomes de comportamento, facilitando a futura orquestração e observabilidade.

## Como usar e validar a aplicação nesta versão

Use `rastro_ai.indexing.extract_and_chunk_document(...)` para gerar chunks, `rastro_ai.indexing.extract_chunk_and_persist_document(...)` para executar o fluxo completo e `rastro_ai.retrieval.search_relevant_chunks(...)` para buscar chunks relevantes. O endpoint HTTP `POST /index` e o upload da API permanecem iguais.

## Cobertura por comportamento

- Persistência: `tests/test_indexing.py::test_extract_chunk_and_persist_document_persists_chunks` cobre o novo boundary `persist_document_chunks`; evidência unitária ou contratual: teste de integração da fachada.
- Busca: `tests/test_retrieval.py::RetrievalTests` e `tests/test_answers.py::AnswerTests` usam `SearchRelevantChunksUseCase` e `InMemoryChunkVectorStore`; evidência unitária ou contratual: testes de ranking, isolamento e citações.
- PGVector: `tests/test_postgres_vector_store.py::PostgresChunkVectorStoreTests` cobre metadata, IDs, filtro por projeto e dimensão; evidência unitária ou contratual: contrato do adapter.
- Regressão: 36 testes, evaluation `20/20` e compilação aprovados; smoke externo não foi repetido nesta rodada.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: resultado, 36 testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && PYTHONPATH=src .venv/bin/python -m evals.evaluate`: resultado, `20/20` casos aprovados e métricas `1.0`.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: resultado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && rg -n 'build_retrieval_container|RetrieveChunksUseCase|InMemoryVectorStore|PostgresVectorStore|RepositoryEmbeddings|index_chunks|index_document_chunks' rastro-ai/src rastro-ai/tests rastro-ai/evals docs/architecture rastro-ai/README.md --glob '*.py' --glob '*.md' | rg -v 'Histórico'`: resultado, nenhuma referência ativa aos nomes antigos.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/017-renomear-fluxo-extracao-chunking/README.md handoffs/017-renomear-fluxo-extracao-chunking/TIMELINE.md handoffs/017-renomear-fluxo-extracao-chunking/v1/README.md handoffs/017-renomear-fluxo-extracao-chunking/v1/TIMELINE.md handoffs/017-renomear-fluxo-extracao-chunking/v2/README.md handoffs/017-renomear-fluxo-extracao-chunking/v2/TIMELINE.md`: esperado, handoffs válidos.
