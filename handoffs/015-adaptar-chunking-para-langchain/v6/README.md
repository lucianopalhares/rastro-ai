# 015/v6 — Adapter LangChain para PGVector

- Versão: `v6`; versão-base: `v5`; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: serviço Python `rastro-ai`, PostgreSQL/pgvector e imagens Docker; arquivos conferidos: repository, testes, dependências e Dockerfiles.
- Reconciliação: `PostgresVectorStore` executava SQL próprio sobre `document_chunks`; casos de uso dependiam da porta `VectorStore`, permitindo trocar somente o adapter.

## O que foi feito

- Alterado `rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py` para usar `langchain_postgres.PGVector` atrás da classe `PostgresVectorStore`.
- Criada a ponte `RepositoryEmbeddings`, mantendo o `EmbeddingRepository` da Rastro como origem dos vetores e evitando acoplamento dos casos de uso a `Document`.
- `upsert` agora envia metadata de projeto, documento, índice e offsets, além de ID SHA-256 determinístico; `search` aplica filtro obrigatório por projeto e converte distância cosine para score local.
- Adicionadas `langchain-postgres>=0.0.19,<1` e dependências equivalentes aos Dockerfiles; testes SQL foram substituídos por testes contratuais do adapter LangChain.

## O que muda na aplicação

- A persistência e busca do runtime passam a usar as tabelas/coleção gerenciadas pelo `langchain-postgres`, com dimensão `384` e distância cosine explícitas.
- Os casos de uso, a porta `VectorStore`, `DocumentChunk`, offsets, `project_id`, IDs estáveis e formato `RetrievedChunk` permanecem próprios da Rastro.
- A tabela legada `document_chunks` não é migrada nem removida automaticamente; dados já existentes precisam ser reindexados para a coleção LangChain antes de depender do novo runtime.
- Fora do escopo: apagar schema antigo, migrar dados históricos, alterar embeddings/modelo, executar chamada OpenAI ou publicar/deployar alterações externas.

## Jornada da aplicação nesta versão

Antes, o fluxo usava SQL manual para gravar e consultar vetores no pgvector. Agora, chunks são convertidos em conteúdo e metadata do LangChain, persistidos pelo `PGVector` e reconvertidos para entidades da Rastro na busca. O resultado percebido deve permanecer equivalente; a próxima evolução é reindexar dados antigos e comparar ranking/latência com evaluation real.

## Como usar e validar a aplicação nesta versão

Suba o PostgreSQL/pgvector e o `ai-indexer` com `docker compose up -d vector-db ai-indexer`; a coleção `rastro_document_chunks` é criada/verificada pelo adapter. Configure `OPENAI_API_KEY` para indexação real; sem credencial, use os testes e o smoke de inicialização/coleção descritos abaixo.

## Cobertura por comportamento

- Persistência/idempotência: `tests/test_postgres_vector_store.py::test_upsert_persists_metadata_and_stable_id` verifica metadata e ID estável enviados ao `PGVector`.
- Isolamento/citações: `test_search_returns_chunk_and_applies_project_filter` verifica filtro obrigatório, offsets, projeto e conversão de score.
- Dimensão: `test_rejects_incompatible_embedding_dimension` confirma a proteção antes do vector store.
- Integração: os testes unitários/contratuais somam 31 casos, evaluation `20/20`, build Docker e upsert/busca reais do PGVector no PostgreSQL passaram; dados legados e chamada OpenAI real não foram migrados/executados.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m unittest discover -s tests -p 'test_*.py'`: esperado, `31` testes aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python evals/evaluate.py`: esperado, `20/20` casos aprovados.
- `cd /home/dev/dev/ia/rastro-ai/rastro-ai && .venv/bin/python -m compileall -q src tests evals`: esperado, término sem erro.
- `cd /home/dev/dev/ia/rastro-ai && docker compose build ai-indexer`: esperado, imagem construída com `langchain-postgres`.
- `cd /home/dev/dev/ia/rastro-ai && docker compose run --rm ai-indexer python -c "from langchain_postgres import PGVector; E=type('E',(),{'embed_documents':lambda s,t:[[0.0]*384 for _ in t],'embed_query':lambda s,t:[0.0]*384}); v=PGVector(embeddings=E(),connection='postgresql://rastro:rastro@vector-db:5432/rastro',collection_name='rastro_smoke_v6',embedding_length=384,create_extension=False); print(type(v).__name__)"`: esperado, `PGVector` impresso sem erro.
- Smoke local adicional: o adapter executou `upsert` e `search` reais contra PostgreSQL/pgvector com embeddings fake, retornando `smoke-project/smoke-doc/1.0`; os registros temporários foram removidos após a verificação.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v1/README.md handoffs/015-adaptar-chunking-para-langchain/v1/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v2/README.md handoffs/015-adaptar-chunking-para-langchain/v2/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v3/README.md handoffs/015-adaptar-chunking-para-langchain/v3/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v4/README.md handoffs/015-adaptar-chunking-para-langchain/v4/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v5/README.md handoffs/015-adaptar-chunking-para-langchain/v5/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v6/README.md handoffs/015-adaptar-chunking-para-langchain/v6/TIMELINE.md`: esperado, handoffs válidos.
