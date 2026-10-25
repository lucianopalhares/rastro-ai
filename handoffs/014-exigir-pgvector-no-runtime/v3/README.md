# 014/v3 — Verificação real do pgvector obrigatório

- Versão: `v3`; versão-base: `v2` aplicada; data: 2026-10-25 -03:00; status: `verified`.
- Aplicação: API `rastro-api`, serviço Python `rastro-ai` e PostgreSQL/pgvector; smoke executado nos containers existentes.
- Estado reconciliado: código exigia `postgres`; faltava apenas confirmar o caminho HTTP real com embeddings e persistência.

## O que foi feito

- Executado upload real pela API usando o fixture `rastro-api/test/fixtures/upload/meeting.md`.
- Confirmado retorno `status: "ready"`, persistência de um chunk no PostgreSQL e dimensão de embedding `384`.
- Executado `POST /index` direto no serviço Python; resposta confirmou `backend: "postgres"`.

## O que muda na aplicação

- A tarefa passa a `verified`: o fluxo real API → Python → OpenAI embeddings → PostgreSQL/pgvector foi comprovado.
- O runtime continua rejeitando configuração ausente ou lexical; testes/evaluation continuam usando o double lexical apenas explicitamente.
- Fora do escopo: troca de modelo, alteração de schema, retry e processamento assíncrono.

## Jornada da aplicação nesta versão

O upload de um documento agora foi validado no caminho que será usado pela pessoa operadora: a API recebe o arquivo, delega ao Python, o Python gera embeddings e persiste no pgvector, e a API retorna `ready`. A confirmação direta no endpoint Python também mostrou `backend: postgres`.

## Como usar e validar a aplicação nesta versão

1. Defina `OPENAI_API_KEY` no `.env` da raiz.
2. Execute `docker compose up -d vector-db ai-indexer api`.
3. Execute `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"`.
4. Espere HTTP `200` com `status: "ready"`; confirme no PostgreSQL um chunk com `vector_dims(embedding)=384`.

## Cobertura por comportamento

- Seleção de backend: testes unitários rejeitam ausência e `memory`; smoke direto confirmou `backend: "postgres"`.
- Indexação integrada: upload HTTP retornou `ready` e o banco confirmou chunk persistido com embedding de dimensão `384`.
- Contrato Python: `POST /index` direto retornou HTTP `200`, `chunks: 1` e backend PostgreSQL.
- Hook estrutural: os quatro arquivos da implementação foram validados após a atualização.

## Instruções de validação

- `uv run --project . --with tiktoken --with 'psycopg[binary]' python -m unittest discover -s tests -p 'test_*.py'`: esperado, 28 testes aprovados.
- `docker compose config`: esperado, backend `postgres`, banco e dimensão `384` configurados.
- `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"`: esperado, documento `ready`.
- `curl --fail-with-body --request POST --url http://127.0.0.1:18473/index --header 'content-type: application/json' --data '{"document":{"id":"smoke-direct-014","projectId":"debug-project","name":"smoke.md","content":"PostgreSQL com pgvector e embeddings."}}'`: esperado, `{"documentId":"smoke-direct-014","chunks":1,"backend":"postgres"}`.
- `docker compose exec -T vector-db psql -U rastro -d rastro -Atc "SELECT project_id || '|' || document_id || '|' || count(*) || '|' || min(vector_dims(embedding)) FROM document_chunks WHERE project_id = 'debug-project' GROUP BY project_id, document_id ORDER BY max(created_at) DESC LIMIT 1;"`: esperado, projeto `debug-project`, documento indexado, quantidade positiva e dimensão `384`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/014-exigir-pgvector-no-runtime/README.md handoffs/014-exigir-pgvector-no-runtime/TIMELINE.md handoffs/014-exigir-pgvector-no-runtime/v3/README.md handoffs/014-exigir-pgvector-no-runtime/v3/TIMELINE.md`: esperado, quatro arquivos válidos.
