# 013/v4 — Habilitar multipart no upload da API

- Versão-base: `v3` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: `rastro-api`.
- Arquivos conferidos: `rastro-api/package.json`, `rastro-api/src/modules/documents/presentation/documents.controller.ts`, `docker-compose.yml` e `rastro-api/README.md`.
- Estado encontrado: o `curl` correto retornava HTTP `400` com `property file should not exist`; `npm ls multer` confirmou a dependência ausente no container da API.

## O que foi feito

- Adicionada a dependência de runtime `multer` (`^2.5.0`) em `rastro-api/package.json`, necessária pelo `FileInterceptor('file')`.
- Mantida a rota, o campo multipart, o fixture e o comando `curl`; a correção atua na resolução do parser multipart antes da validação do DTO.
- A alteração resolve o erro `property file should not exist`, permitindo que o arquivo seja entregue por `@UploadedFile()` e que o body contenha somente `projectId`.
- O manifest JSON não suporta JSDoc; a exceção é registrada neste handoff. Não houve alteração de classe, método ou contrato TypeScript.

## O que muda na aplicação

- O upload `POST /api/v1/documents/upload` passa a interpretar corretamente o campo `file` quando a imagem da API é reconstruída.
- O contrato HTTP e o comando documentado permanecem iguais; produção somente recebe a dependência quando sua imagem for construída com o manifest atualizado.
- Containers existentes precisam ser reconstruídos com `docker compose build api` antes do teste; nenhum serviço externo foi alterado.

## Jornada da aplicação nesta versão

Antes, o `curl` chegava à API, mas o campo multipart era tratado como propriedade extra e falhava no `ValidationPipe`. Agora, após reconstruir a imagem, o Multer processa `file`, o controller recebe `@UploadedFile()` e o fluxo segue para a indexação Python. A próxima evolução continua sendo confirmar o status `ready` com credencial OpenAI válida.

## Como usar e validar a aplicação nesta versão

1. Na raiz, execute `docker compose build api`.
2. Recrie a API com `docker compose up -d api`.
3. Execute o `curl` do upload em `rastro-api/README.md`.
4. Confira HTTP `201` e o status do documento; `ready` depende de `OPENAI_API_KEY` válida.

## Cobertura por comportamento

- Multipart: dependência `multer` cobre o parser usado por `FileInterceptor('file')`; o contrato HTTP e a rota existentes permanecem inalterados.
- Validação: o erro observado `property file should not exist` é coberto pela reconstrução da imagem e pelo smoke HTTP do `curl`.
- Integração: build Docker e upload real devem ser executados após a aplicação; a versão não inclui credenciais nem altera o backend de embeddings.

## Instruções de validação

- `docker compose build api`: esperado, imagem reconstruída com `multer` instalado.
- `docker compose up -d api`: esperado, API saudável na porta `3039` e inspector em `9229`.
- `docker compose exec -T api npm ls multer --depth=0`: esperado, `multer@2.5.0` ou versão compatível `2.x` listada.
- `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form "file=$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"`: esperado, sem o erro `property file should not exist` e HTTP `201`; status `ready` exige `OPENAI_API_KEY` válida.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v4/README.md handoffs/013-configurar-debug-python-api-vscode/v4/TIMELINE.md`: esperado, quatro arquivos válidos.
