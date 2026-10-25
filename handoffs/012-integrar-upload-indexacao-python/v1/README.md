# 012/v1 — Contrato e integração do upload com a indexação Python

- Versão-base: estado real conferido em 2026-10-24; não há versão anterior da implementação 012.
- Status: `applied`; aplicação: `rastro-api`, `rastro-ai` e `docker-compose.yml`.
- Arquivos reais conferidos: `rastro-api/src/modules/documents/presentation/documents.controller.ts`, `application/upload-document.use-case.ts`, `application/document-file.storage.ts`, `infrastructure/local-document-file.storage.ts`, `domain/document.ts`, `documents.module.ts`, além de `rastro-ai/src/rastro_ai/document_indexing/application/use_cases/index_document.py`, `application/ports.py`, `indexing.py` e `retrieval.py`.
- Estado encontrado: a API salvava `.md`/`.txt` e criava documentos `pending`; a IA indexava caminhos locais, mas não havia ponte executável entre os processos.

## O que foi feito

Foi criado o contrato `DocumentIndexer`, o adaptador HTTP da API, o endpoint Python `/index`, a composição do serviço `ai-indexer`, a operação Python de persistência dos chunks e os testes dos fluxos de sucesso/falha. O upload agora armazena o arquivo, envia o payload ao Python, e salva o documento como `ready` ou `failed`; a operação também preserva o backend de memória como padrão.

## O que muda na aplicação

A aplicação agora dispara a indexação Python durante o upload, propaga `documentId`/`projectId`, atualiza `pending → processing → ready/failed` e retorna o estado persistido. O transporte é síncrono e não possui retry automático; frontend, deploy, migração externa e geração por LLM permanecem fora do escopo. O serviço usa o backend vetorial configurado e mantém a memória como fallback.

## Jornada da aplicação nesta versão

Antes, o arquivo enviado era armazenado pela API e permanecia pendente. Agora, a API envia o conteúdo ao serviço Python, que extrai, divide e persiste os chunks; a resposta informa `ready` quando a indexação confirma ou `failed` quando o serviço falha.

## Como usar e validar a aplicação nesta versão

Suba o serviço Python com `PYTHONPATH=rastro-ai/src AI_PORT=18473 python3 -m rastro_ai.service` e valide `curl -fsS http://127.0.0.1:18473/health`. Envie um documento com `curl -fsS -X POST http://127.0.0.1:18473/index -H 'content-type: application/json' --data '{"document":{"id":"doc-smoke","projectId":"project-smoke","name":"meeting.md","content":"# Decisão\nUsar PostgreSQL.","status":"processing"}}'`; espere HTTP 200 e `{"documentId":"doc-smoke","chunks":1,"backend":"memory"}` no modo local. No Compose, `docker compose up --build api ai-indexer` deve manter ambos saudáveis; o endpoint Python fica publicado em `http://127.0.0.1:18473` por padrão.

## Cobertura por comportamento

- Integração upload → indexação: coberta pelos testes do gateway HTTP, do caso de uso e pelo smoke do endpoint Python.
- Estados e falhas: cobertos por `ready` no sucesso e `failed` quando o indexador retorna erro; retry e idempotência automática permanecem pendentes.
- Persistência vetorial: `index_document_in_store` chama o vector store configurado; a implementação 011 permanece a dependência persistente.

## Instruções de validação

- `cd rastro-api && docker compose run --rm --no-deps api npm test -- --runInBand`: esperado, 3 suítes e 10 testes aprovados.
- `cd rastro-api && docker compose run --rm --no-deps api npm run build`: esperado, compilação NestJS concluída.
- `cd rastro-ai && python3 -m unittest discover -s tests -v && python3 -m compileall -q src tests`: esperado, 23 testes aprovados e compilação sem erros.
- `PYTHONPATH=rastro-ai/src AI_PORT=18473 python3 -m rastro_ai.service` e os dois `curl` acima: esperado, health `ok` e resposta 200 com chunks.
- `docker compose config`: esperado, serviços `api`, `ai-indexer` e `vector-db` válidos.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/012-integrar-upload-indexacao-python/README.md handoffs/012-integrar-upload-indexacao-python/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v1/README.md handoffs/012-integrar-upload-indexacao-python/v1/TIMELINE.md`: esperado, 4 arquivos válidos.
- `docker-compose.yml` não possui comentários JSDoc; a exceção é o formato declarativo, documentado nesta versão.
