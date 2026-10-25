# 013/v6 — Reforçar a leitura do arquivo multipart

- Versão-base: `v5` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: `rastro-api`.
- Arquivos conferidos: `rastro-api/src/modules/documents/presentation/documents.controller.ts`, `rastro-api/package.json`, `rastro-api/README.md` e logs do container.
- Estado encontrado: Multer 2.5.0 parseava o multipart, mas `@UploadedFile()` chegava `undefined` no handler e retornava `A file is required`.

## O que foi feito

- O método `DocumentsController.upload` passou a receber `@Req()` e usar `request.file` como fallback quando `@UploadedFile()` não estiver preenchido.
- O arquivo efetivo foi centralizado em `uploadedFile`; validações e o caso de uso continuam recebendo o mesmo conteúdo, nome, MIME e tamanho.
- O JSDoc do método recebeu o histórico `v6`, explicando a compatibilidade com metadata de upload divergente.

## O que muda na aplicação

- O endpoint preserva os campos `projectId` e `file`, mas tolera a forma como o interceptor expõe o arquivo no request.
- Requests sem arquivo continuam retornando `400`; uploads válidos deixam de falhar com `A file is required` quando `request.file` está disponível.
- Não há mudança no endpoint Python, no contrato de indexação ou na persistência.

## Jornada da aplicação nesta versão

Antes, Multer processava o multipart, mas o parâmetro `@UploadedFile()` não recebia o arquivo no handler NestJS. Agora, o controller consulta também `request.file`, encaminha o fixture ao caso de uso e mantém os breakpoints no upload e na indexação. A próxima evolução é confirmar o status `ready` com embeddings disponíveis.

## Como usar e validar a aplicação nesta versão

1. Execute `docker compose build api`.
2. Recrie a API com `docker compose rm -sf -v api && docker compose up -d api`.
3. Execute o `curl` do `rastro-api/README.md`.
4. Coloque breakpoint em `DocumentsController.upload` e inspecione `file`, `request.file` e `uploadedFile`.

## Cobertura por comportamento

- Contrato multipart: rota, campo `file`, `FileInterceptor` e `@UploadedFile()` permanecem preservados; o fallback cobre o request populado pelo Multer.
- Validação: `projectId` e arquivo continuam obrigatórios, com `400` para ausência; upload válido passa ao caso de uso.
- Integração: o build Docker e o `curl` real são as evidências necessárias; o status final depende do backend de embeddings e de `OPENAI_API_KEY`.

## Instruções de validação

- `docker compose build api`: esperado, imagem reconstruída com o controller atualizado.
- `docker compose rm -sf -v api && docker compose up -d api`: esperado, API recriada sem o volume anônimo antigo de `node_modules`.
- `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form "file=$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"`: esperado, não retornar `A file is required`; HTTP `201` ou documento com `status: failed` se embeddings não estiverem configurados.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v6/README.md handoffs/013-configurar-debug-python-api-vscode/v6/TIMELINE.md`: esperado, quatro arquivos válidos.
