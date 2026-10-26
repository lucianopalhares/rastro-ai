# Rastro API

## Desenvolvimento e debug com Docker

Na raiz do repositório, construa a imagem de desenvolvimento da API e do indexador Python:

```bash
docker compose build api ai-indexer
```

Inicie a API, o indexador Python e o PostgreSQL:

```bash
docker compose up api ai-indexer vector-db
```

No VS Code, abra a raiz do repositório, selecione `Debug Docker: API + Python` e pressione `F5`. O perfil conecta à API NestJS em `127.0.0.1:9229` e ao Python em `127.0.0.1:5678`.

Breakpoints úteis ficam em `src/modules/documents/application/upload-document.use-case.ts` e `src/modules/documents/infrastructure/http-document-indexer.ts`. A API fica disponível em `http://127.0.0.1:3039/api/v1`.

Para verificar o health check:

```bash
curl --fail http://127.0.0.1:3039/api/v1/health
curl --fail http://127.0.0.1:18473/health
```

Resultado esperado: respostas HTTP `200`. O indexador usa PostgreSQL e embeddings OpenAI; defina `OPENAI_API_KEY` no `.env` antes de testar uploads.

Para enviar o documento de exemplo:

```bash
curl --fail-with-body --request POST \
  --url http://127.0.0.1:3039/api/v1/documents/upload \
  --header 'accept: application/json' \
  --form 'projectId=debug-project' \
  --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"
```

Resultado esperado: HTTP `200` e documento com `projectId` igual a `debug-project`; com `OPENAI_API_KEY` válida, o status esperado é `ready`.

## Fluxo API → Python

O upload da API delega a indexação ao serviço Python por HTTP:

```text
POST /api/v1/documents/upload
  → POST http://ai-indexer:8000/index
  → PostgreSQL/pgvector
```

Variáveis usadas pela API:

```text
AI_INDEXING_URL=http://ai-indexer:8000/index
AI_INDEXING_TIMEOUT_MS=60000
```

Dentro do Compose, `ai-indexer:8000` é o endereço interno do Python. A URL `http://127.0.0.1:18473/index` serve para chamadas diretas feitas pelo host. A implementação está em `src/modules/documents/infrastructure/http-document-indexer.ts`.

Para testar a indexação diretamente no serviço Python, sem passar pela API:

```bash
curl --fail-with-body --request POST \
  --url http://127.0.0.1:18473/index \
  --header 'content-type: application/json' \
  --data @- <<'JSON'
{
  "document": {
    "id": "debug-document-001",
    "projectId": "debug-project",
    "name": "meeting.md",
    "content": "A equipe decidiu usar PostgreSQL com pgvector."
  }
}
JSON
```

Resultado esperado: HTTP `200` com `documentId`, quantidade de `chunks` e `backend: "postgres"`. Essa chamada ignora a API e é útil para atingir breakpoints em `rastro-ai/src/rastro_ai/service.py` e `rastro-ai/src/rastro_ai/indexing.py`.

## Busca semântica

Consulte os chunks do projeto pela API NestJS; o Rastro AI gera o embedding da consulta e
retorna resultados do PGVector com score e citação:

```bash
curl --fail-with-body --get \
  --url 'http://127.0.0.1:3039/api/v1/documents/search?projectId=debug-project&query=qual%20banco%20foi%20decidido&limit=5' \
  --header 'accept: application/json'
```

Resultado esperado: HTTP `200` com `projectId`, `query` e `results`. `limit` aceita valores de
1 a 50; a busca sempre permanece filtrada pelo `projectId` informado.
