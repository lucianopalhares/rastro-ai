# 012/v2 — Modelo Document e embeddings externos

- Versão-base: `v1` aplicada; reconciliação realizada em 2026-10-24 com API, serviço Python, Compose, schema e testes reais.
- Status: `applied`; aplicação: `rastro-api`, `rastro-ai`, `infra/postgres` e `docker-compose.yml`.
- Estado encontrado: a API já chamava o indexador, mas enviava DTO paralelo; o PostgreSQL aceitava provider local, enquanto o serviço Compose não tinha repository externo.
- Decisão: enviar `Document.toJSON()` em `{ document }` e usar `EmbeddingRepository` com `OpenAIEmbeddingRepository`, `text-embedding-3-small` e dimensão `384`.

## O que foi feito

O gateway da API passou a enviar o modelo `Document` existente. O serviço Python valida esse modelo, usa um repository de embeddings em lote e o `PostgresVectorStore` grava cada chunk com projeto, documento, índice, conteúdo, offsets e vetor na tabela `document_chunks`. O Compose usa PostgreSQL/pgvector e porta externa `18473` por padrão.

## O que muda na aplicação

Com `VECTOR_STORE_BACKEND=postgres` e `OPENAI_API_KEY`, cada upload chama o endpoint de indexação, gera embeddings externos e executa `INSERT ... ON CONFLICT` por `(project_id, document_id, chunk_index)`. O schema continua com `vector(384)`, portanto o repository envia `dimensions: 384`. Sem chave, a chamada real ao provedor falha explicitamente; não há fallback silencioso para embeddings falsos.

## Jornada da aplicação nesta versão

Antes, o upload criava o documento e encaminhava um DTO paralelo para um indexador que podia permanecer em memória. Agora, o upload encaminha o mesmo `Document` do domínio, chama o provedor externo em lote e persiste os vetores no PostgreSQL; a resposta informa `documentId`, quantidade de chunks e backend.

## Como usar e validar a aplicação nesta versão

Preencha `OPENAI_API_KEY` no `.env` local, sem versionar o valor. Suba `docker compose up --build vector-db ai-indexer api`; o endpoint externo do indexador será `http://127.0.0.1:18473`. Faça `curl -fsS -X POST http://127.0.0.1:3039/api/v1/documents/upload -F projectId=project-1 -F file=@rastro-api/test/fixtures/upload/meeting.md`; espere `status: "ready"`. Depois consulte `docker compose exec vector-db psql -U rastro -d rastro -c "SELECT project_id, document_id, chunk_index, length(content), start_offset, end_offset, vector_dims(embedding) FROM document_chunks ORDER BY created_at DESC LIMIT 10;"`; espere o projeto/documento enviados, chunks, offsets e dimensão `384`.

## Cobertura por comportamento

- Modelo enviado: evidência unitária/contratual em `http-document-indexer.spec.ts` confirma `{ document }` com o `DocumentProperties` serializado.
- Repository externo: evidência unitária em `test_openai_embedding_repository.py` confirma uma chamada em lote, modelo, dimensão e ordenação dos embeddings sem rede.
- Persistência: evidência unitária em `test_postgres_vector_store.py` confirma os campos SQL, `ON CONFLICT` e validação de dimensão; gravação real aguarda `OPENAI_API_KEY`.
- Integração/smoke real: schema e linha histórica foram consultados no PostgreSQL; o smoke API → OpenAI → `document_chunks` não foi aplicado nesta sessão porque `OPENAI_API_KEY` está ausente, sem substituir a evidência por dados falsos.

## Instruções de validação

- `cd rastro-api && docker compose run --rm --no-deps api npm test -- --runInBand`: esperado, 10 testes aprovados.
- `cd rastro-ai && python3 -m unittest discover -s tests -v && python3 -m compileall -q src tests`: esperado, 24 testes aprovados e compilação sem erros.
- `docker compose config`: esperado, `api`, `ai-indexer` com `VECTOR_STORE_BACKEND=postgres`, `vector-db` e porta externa padrão `18473` válidos.
- `docker compose exec vector-db psql -U rastro -d rastro -c "\d+ document_chunks"`: esperado, colunas de documento, offsets e `embedding vector(384)`.
- Com `OPENAI_API_KEY` configurada, executar o `curl` de upload e a consulta SQL acima; esperado, resposta `ready` e linha persistida em `document_chunks`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/012-integrar-upload-indexacao-python/README.md handoffs/012-integrar-upload-indexacao-python/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v1/README.md handoffs/012-integrar-upload-indexacao-python/v1/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v2/README.md handoffs/012-integrar-upload-indexacao-python/v2/TIMELINE.md`: esperado, 6 arquivos válidos.
