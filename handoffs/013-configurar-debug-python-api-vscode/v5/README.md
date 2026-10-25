# 013/v5 — Corrigir validação do multipart no upload

- Versão-base: `v4` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: `rastro-api`.
- Arquivos conferidos: `rastro-api/src/modules/documents/presentation/documents.controller.ts`, `rastro-api/package.json`, `rastro-api/README.md` e container Docker da API.
- Estado encontrado: mesmo com `multer@2.5.0`, o upload retornava `property file should not exist`; a validação global estava aplicada ao body multipart completo.

## O que foi feito

- Alterado o método `DocumentsController.upload` para receber somente `@Body('projectId')` e manter o arquivo em `@UploadedFile()`.
- Adicionada validação explícita de `projectId` vazio ou ausente antes de chamar o caso de uso.
- Mantido o `FileInterceptor('file')`, o limite de 5 MiB e o contrato do comando `curl` documentado.
- O comentário JSDoc do método foi atualizado com o histórico `v5`, explicando a proteção contra a rejeição indevida do campo multipart.

## O que muda na aplicação

- O campo `file` deixa de ser interpretado pelo `ValidationPipe` global como propriedade extra do DTO do body.
- O upload válido pode prosseguir para o indexador Python; requests sem `projectId` ou sem arquivo continuam retornando `400`.
- Não houve mudança no contrato externo: os campos continuam `projectId` e `file` no mesmo endpoint.

## Jornada da aplicação nesta versão

Antes, o parser multipart estava instalado, mas o `ValidationPipe` rejeitava `file` antes do controller processar o upload. Agora, `projectId` é validado isoladamente, o arquivo é recebido por `@UploadedFile()` e o fluxo alcança o caso de uso e o indexador. A próxima evolução é confirmar `ready` com embeddings válidos.

## Como usar e validar a aplicação nesta versão

1. Execute `docker compose build api`.
2. Recrie a API com `docker compose up -d api`.
3. Execute o comando `curl` do `rastro-api/README.md`.
4. Coloque breakpoint em `DocumentsController.upload` e em `UploadDocumentUseCase.execute` para acompanhar o request.

## Cobertura por comportamento

- Contrato multipart: `FileInterceptor('file')` e `@UploadedFile()` permanecem responsáveis pelo arquivo; `projectId` é validado pelo parâmetro do body.
- Validação: requests sem `projectId` ou arquivo continuam protegidos por `BadRequestException`; o erro observado `property file should not exist` deixa de ocorrer em uploads válidos.
- Integração: o build Docker e o smoke HTTP do `curl` são as evidências necessárias; o status `ready` continua dependendo de `OPENAI_API_KEY`.

## Instruções de validação

- `docker compose build api`: esperado, imagem reconstruída com o controller atualizado.
- `docker compose up -d api`: esperado, API saudável na porta `3039`.
- `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form "file=$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"`: esperado, HTTP `201` ou documento com `status: failed` se embeddings não estiverem configurados; não deve retornar `property file should not exist`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v5/README.md handoffs/013-configurar-debug-python-api-vscode/v5/TIMELINE.md`: esperado, quatro arquivos válidos.
