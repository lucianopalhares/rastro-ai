# Rastro AI

Aplicação composta por uma API NestJS, um serviço Python de indexação e PostgreSQL com pgvector.

## Fluxo local com Docker

Defina `OPENAI_API_KEY` no arquivo `.env` da raiz quando quiser executar indexação com embeddings. Construa as imagens:

```bash
docker compose build api ai-indexer
```

Inicie os serviços nesta ordem lógica: banco vetorial, indexador Python e API. O Compose respeita a saúde do banco antes de iniciar o indexador:

```bash
docker compose up -d vector-db ai-indexer api
```

Confira os containers:

```bash
docker compose ps
```

Resultado esperado: `vector-db`, `ai-indexer` e `api` saudáveis. As portas publicadas são API `3039`, Python `18473`, inspector Node `9229`, `debugpy` `5678` e PostgreSQL `55432`.

## Verificações HTTP na ordem correta

1. Verifique a API:

```bash
curl --fail-with-body http://127.0.0.1:3039/api/v1/health
```

Resultado esperado: HTTP `200`.

2. Verifique o Python:

```bash
curl --fail-with-body http://127.0.0.1:18473/health
```

Resultado esperado: HTTP `200` com `{"status":"ok"}`.

3. Para testar somente a indexação Python, envie um documento diretamente:

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

Resultado esperado: HTTP `200` com `documentId`, `chunks` e `backend: "postgres"`.

## Busca semântica pela API

A API pública expõe a busca vetorial determinística por projeto e delega a consulta ao
Rastro AI, que gera o embedding da pergunta e consulta o PGVector:

```bash
curl --fail-with-body --get \
  --url 'http://127.0.0.1:3039/api/v1/documents/search?projectId=debug-project&query=qual%20banco%20foi%20decidido&limit=5' \
  --header 'accept: application/json'
```

Resultado esperado: HTTP `200` com `projectId`, `query` e `results`; cada resultado contém
`documentId`, `chunkIndex`, `content`, `score` e `citation` com offsets verificáveis.

## Observabilidade local com Langfuse

O Langfuse self-hosted é opcional e roda em um Compose complementar. A interface fica em
`http://127.0.0.1:38917` e o armazenamento de mídia usa a porta `38918`.

```bash
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d
```

Crie o projeto e as chaves na interface, preencha `LANGFUSE_PUBLIC_KEY` e
`LANGFUSE_SECRET_KEY` no `.env`, defina `LANGFUSE_ENABLED=true` e reinicie o `ai-indexer`.
O fluxo de indexação passará a registrar duração, status, projeto, contagem de chunks,
modelo e dimensão sem enviar o texto dos documentos.

Para acompanhar tokens e custo de embeddings, configure o modelo `text-embedding-3-small`
em `Project Settings > Models`. O Rastro conta os tokens localmente; opcionalmente,
`LANGFUSE_EMBEDDING_INPUT_COST_PER_TOKEN` informa um preço direto em USD por token.

Os valores padrão do Compose são apenas para desenvolvimento local; troque as senhas,
`salt`, `NEXTAUTH_SECRET` e `ENCRYPTION_KEY` antes de expor o stack fora da máquina local.

4. Para testar o fluxo completo API → Python, envie o fixture pela API:

```bash
curl --fail-with-body --request POST \
  --url http://127.0.0.1:3039/api/v1/documents/upload \
  --header 'accept: application/json' \
  --form 'projectId=debug-project' \
  --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"
```

Resultado esperado: HTTP `200`, documento com `projectId: "debug-project"` e `status: "ready"` quando `OPENAI_API_KEY` estiver válida.

## Fluxo de indexação pela API

A árvore detalhada de classes, métodos, repositories e providers está em
[`docs/architecture/document-upload-indexing-flow.md`](docs/architecture/document-upload-indexing-flow.md).

O fluxo integrado começa no upload da API e delega a indexação ao processo Python:

```text
POST /api/v1/documents/upload
  → API NestJS
  → POST http://ai-indexer:8000/index
  → serviço Python
  → PostgreSQL/pgvector
```

A API usa estas variáveis de ambiente:

```text
AI_INDEXING_URL=http://ai-indexer:8000/index
AI_INDEXING_TIMEOUT_MS=60000
```

`AI_INDEXING_URL` aponta para o serviço Python na rede interna do Compose. A porta publicada `18473` (`http://127.0.0.1:18473/index`) é usada somente quando o host chama o Python diretamente; a API dentro do container usa `ai-indexer:8000`.

No código, a chamada está em `rastro-api/src/modules/documents/infrastructure/http-document-indexer.ts`. O caso de uso do upload envia o documento, aguarda a confirmação do Python e persiste o status `ready` ou `failed`.

## Breakpoints no VS Code

Com os containers em execução, abra a raiz no VS Code e selecione `Debug Docker: API + Python` com `F5`. O perfil faz attach à API em `9229` e ao Python em `5678`.

Breakpoints úteis:

- API: `rastro-api/src/modules/documents/application/upload-document.use-case.ts` e `rastro-api/src/modules/documents/infrastructure/http-document-indexer.ts`;
- Python: `rastro-ai/src/rastro_ai/service.py` e `rastro-ai/src/rastro_ai/indexing.py`.

## Parar os serviços

```bash
docker compose down
```

Esse comando remove os containers, mas preserva o volume nomeado do PostgreSQL.
