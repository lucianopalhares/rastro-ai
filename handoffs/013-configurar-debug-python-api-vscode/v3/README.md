# 013/v3 — Documentar upload do fixture no fluxo Docker

- Versão-base: `v2` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: `rastro-api`.
- Arquivos conferidos: `rastro-api/README.md`, `rastro-api/src/modules/documents/presentation/documents.controller.ts` e `rastro-api/test/fixtures/upload/meeting.md`; o README da IA foi conferido para confirmar que não era o destino solicitado.
- Estado encontrado: os READMEs documentavam health checks, mas não tinham um `curl` completo para enviar o fixture multipart.

## O que foi feito

- Adicionado ao `rastro-api/README.md` um comando copiável com `POST`, URL, header `accept`, campo `projectId`, campo multipart `file` e caminho absoluto do fixture `meeting.md`.
- Documentado o resultado esperado: HTTP `201`, projeto `debug-project` e status `ready` com credencial OpenAI válida; falha de indexação permanece representada por `status: failed` no contrato atual.
- A rota e os campos foram conferidos no `DocumentsController`; o arquivo de entrada foi conferido no fixture real.

## O que muda na aplicação

- Não há mudança de runtime, contrato ou persistência; somente a documentação de uso e validação foi ampliada.
- A pessoa consegue reproduzir o fluxo API → indexador Python usando o documento de exemplo existente.
- O comando pressupõe os containers Docker ativos e usa a porta publicada `3039`; não inclui credenciais no comando.

## Jornada da aplicação nesta versão

Antes, o README da API não mostrava como reproduzir o upload do fixture. Agora, após iniciar o Compose e conectar o debugger, a pessoa pode executar o `curl` documentado, atingir breakpoints no upload e no indexador e verificar o documento retornado. A próxima evolução é executar o smoke completo com credencial OpenAI; a geração de embeddings continua dependente de `OPENAI_API_KEY`.

## Como usar e validar a aplicação nesta versão

1. Execute `docker compose up -d vector-db ai-indexer api` na raiz.
2. Se necessário, abra o compound `Debug Docker: API + Python` no VS Code.
3. Execute o `curl` registrado em `rastro-api/README.md`.
4. Confira HTTP `201`, `projectId` `debug-project` e o status retornado.

## Cobertura por comportamento

- Rota multipart e contrato HTTP: conferidos em `DocumentsController.upload`, com `POST /api/v1/documents/upload` e campo `file`.
- Fixture: conferido `rastro-api/test/fixtures/upload/meeting.md`, formato Markdown aceito pelo indexador.
- Integração real: o comando foi documentado, mas não foi executado nesta rodada para evitar uma indexação externa sem confirmação de credencial/custo; health checks Docker da v2 permanecem aprovados.

## Instruções de validação

- `curl --fail-with-body --request POST --url http://127.0.0.1:3039/api/v1/documents/upload --header 'accept: application/json' --form 'projectId=debug-project' --form 'file=@/home/dev/dev/ia/rastro-ai/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown'`: esperado, HTTP `201`, documento do projeto `debug-project` e `status: ready` quando `OPENAI_API_KEY` estiver válida.
- `python3 -m json.tool .vscode/launch.json`: esperado, JSON válido.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v3/README.md handoffs/013-configurar-debug-python-api-vscode/v3/TIMELINE.md`: esperado, quatro arquivos válidos.
