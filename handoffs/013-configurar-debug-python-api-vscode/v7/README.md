# 013/v7 — Corrigir o comando curl do upload

- Versão-base: `v6` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: `rastro-api`.
- Arquivos conferidos: controller de upload, `rastro-api/README.md`, fixture Markdown e logs do container.
- Estado encontrado: o comando executado usava `file=$PWD/...` sem `@`; Multer recebeu o caminho como texto e `req.file` ficou vazio.

## O que foi feito

- Restaurado o binding padrão do controller com `@Body() request` e `@UploadedFile() file`, removendo o fallback e o log temporário das tentativas anteriores.
- Corrigido o comando do README para `file=@$PWD/rastro-api/test/fixtures/upload/meeting.md`, mantendo `projectId`, MIME e rota.
- Mantida a dependência `multer`, necessária para o `FileInterceptor('file')`.
- O JSDoc do método registra a correção `v7` e o motivo do retorno ao contrato padrão.

## O que muda na aplicação

- Não há novo contrato de runtime: o endpoint usa novamente o binding NestJS documentado para multipart.
- O comando copiado passa o arquivo como arquivo real; sem `@`, o curl envia apenas uma string e a API responde `A file is required`.

## Jornada da aplicação nesta versão

Antes, o comando sem `@` enviava o caminho como campo textual e produzia `A file is required`. Agora, o `curl` usa `file=@...`, o Multer popula `req.file`, o controller recebe `@UploadedFile()` e o fluxo pode continuar até a indexação. A próxima evolução é confirmar o status final conforme as credenciais de embeddings.

## Como usar e validar a aplicação nesta versão

1. Execute `docker compose build api`.
2. Recrie a API com `docker compose rm -sf -v api && docker compose up -d api`.
3. Na raiz, execute o comando corrigido do `rastro-api/README.md`.
4. Confira HTTP `200` e `status: ready`; esse resultado depende de `OPENAI_API_KEY` válida.

## Cobertura por comportamento

- Multipart: o contrato `file=@...` foi conferido contra `FileInterceptor('file')` e `@UploadedFile()`.
- Diagnóstico: logs confirmaram que o comando anterior enviava `file` como texto; a correção altera o comando, não o contrato da aplicação.
- Integração: o smoke HTTP do curl é a evidência real do upload; embeddings e status `ready` dependem da configuração externa.

## Instruções de validação

- `docker compose build api`: esperado, imagem construída.
- `docker compose rm -sf -v api && docker compose up -d api`: esperado, API recriada e saudável.
- `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"`: executado com sucesso, HTTP `200`, `projectId: debug-project` e `status: ready`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v7/README.md handoffs/013-configurar-debug-python-api-vscode/v7/TIMELINE.md`: esperado, quatro arquivos válidos.
