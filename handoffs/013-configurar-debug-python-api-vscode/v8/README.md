# 013/v8 — Documentar indexação direta no Python

- Versão-base: `v7` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: `rastro-api`.
- Arquivos conferidos: `rastro-api/README.md`, `rastro-ai/src/rastro_ai/service.py`, `rastro-ai/src/rastro_ai/indexing.py` e `docker-compose.yml`.
- Estado encontrado: o README documentava o upload pela API, mas não a chamada direta `POST /index` do serviço Python.

## O que foi feito

- Adicionada ao README da API uma instrução completa de `curl` para `POST http://127.0.0.1:18473/index`.
- Documentados método, URL, header `content-type`, payload JSON com `document`, resposta esperada e pontos de breakpoint Python.
- Registrado que a chamada direta isola a indexação e não atravessa o controller ou o cliente HTTP da API.

## O que muda na aplicação

- Não há mudança de runtime, contrato ou persistência; somente a documentação de diagnóstico foi ampliada.
- A pessoa pode testar o indexador Python diretamente, usando o backend PostgreSQL do Compose, ou testar o fluxo completo pelo upload da API.

## Jornada da aplicação nesta versão

Antes, o README mostrava somente o upload pela API. Agora, há dois caminhos documentados: API → Python para o fluxo integrado e `POST /index` direto para isolar a indexação. A próxima evolução continua sendo observar o comportamento com breakpoints e avaliar o status retornado.

## Como usar e validar a aplicação nesta versão

1. Execute `docker compose up -d vector-db ai-indexer api` na raiz.
2. Para o fluxo integrado, use o upload documentado anteriormente.
3. Para isolar o Python, execute o `curl` de `http://127.0.0.1:18473/index` no README da API.
4. Coloque breakpoints em `rastro-ai/src/rastro_ai/service.py` e `rastro-ai/src/rastro_ai/indexing.py`.

## Cobertura por comportamento

- Contrato HTTP Python: conferido em `IndexingRequestHandler.do_POST`, com JSON `{ "document": ... }` e resposta `documentId`, `chunks` e `backend`.
- Comunicação Docker: porta publicada `18473` corresponde ao serviço Python na porta interna `8000`.
- Integração: o comando é reproduzível com os containers ativos; o resultado `backend: postgres` depende da configuração do Compose.

## Instruções de validação

- `curl --fail-with-body --request POST --url http://127.0.0.1:18473/index --header 'content-type: application/json' --data '{"document":{"id":"debug-document-001","projectId":"debug-project","name":"meeting.md","content":"A equipe decidiu usar PostgreSQL com pgvector."}}'`: esperado, HTTP `200` com `documentId`, `chunks` e `backend: "postgres"`.
- `python3 -m json.tool .vscode/launch.json`: esperado, JSON válido.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v8/README.md handoffs/013-configurar-debug-python-api-vscode/v8/TIMELINE.md`: esperado, quatro arquivos válidos.
