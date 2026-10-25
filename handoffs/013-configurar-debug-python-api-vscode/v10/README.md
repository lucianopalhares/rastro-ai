# 013/v10 — Documentar o fluxo API → Python

- Versão-base: `v9` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: raiz e `rastro-api`.
- Arquivos conferidos: `README.md`, `rastro-api/README.md`, `docker-compose.yml` e `rastro-api/src/modules/documents/infrastructure/http-document-indexer.ts`.
- Estado encontrado: os requests estavam documentados, mas faltava explicar a delegação interna e as variáveis `AI_INDEXING_URL`/`AI_INDEXING_TIMEOUT_MS`.

## O que foi feito

- Adicionadas aos READMEs raiz e da API a sequência `POST /api/v1/documents/upload` → `POST http://ai-indexer:8000/index` → PostgreSQL/pgvector.
- Documentadas as variáveis de ambiente, a diferença entre hostname interno Docker e porta publicada no host e o arquivo que implementa a chamada.

## O que muda na aplicação

- Não há mudança de runtime; somente o fluxo existente foi explicitado na documentação.
- O README deixa claro que a API não importa Python: ela chama o processo Python separado por HTTP e aguarda a confirmação antes de persistir `ready` ou `failed`.

## Jornada da aplicação nesta versão

Antes, os comandos permitiam testar API e Python, mas não mostravam a ligação entre eles. Agora, a documentação explica a chamada externa, o endereço interno do Compose, o timeout e o ponto do código que delega a indexação.

## Como usar e validar a aplicação nesta versão

1. Suba os serviços com `docker compose up -d vector-db ai-indexer api`.
2. Confira `AI_INDEXING_URL` no Compose.
3. Execute o upload documentado na raiz.
4. Observe breakpoints no cliente HTTP da API e no handler Python.

## Cobertura por comportamento

- Contrato HTTP: endpoint externo, endpoint interno e payload documentados.
- Configuração: `AI_INDEXING_URL` e `AI_INDEXING_TIMEOUT_MS` conferidos contra Compose e cliente HTTP.
- Smoke integrado: upload API, indexação Python e status `ready` foram executados nas versões anteriores.

## Instruções de validação

- `docker compose config`: esperado, `AI_INDEXING_URL=http://ai-indexer:8000/index` e timeout `60000` visíveis na configuração resolvida.
- `rg -n "AI_INDEXING_URL|AI_INDEXING_TIMEOUT_MS|ai-indexer:8000/index" README.md rastro-api/README.md docker-compose.yml rastro-api/src/modules/documents/infrastructure/http-document-indexer.ts`: esperado, referências documentais e de runtime encontradas.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v10/README.md handoffs/013-configurar-debug-python-api-vscode/v10/TIMELINE.md`: esperado, quatro arquivos válidos.
