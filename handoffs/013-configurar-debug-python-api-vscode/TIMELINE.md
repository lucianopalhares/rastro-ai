# Timeline — 013

## v1 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: `.vscode/launch.json` ausente; `rastro-api/package.json`, `rastro-api/src/main.ts`, `rastro-ai/src/rastro_ai/service.py` e `docker-compose.yml`.
- Mudanças aplicadas: compound do VS Code para Python/NestJS e script `start:debug` da API.
- Problema resolvido: ausência de breakpoint reproduzível nos dois processos do fluxo API → Python.
- Pendências: validações finais dependentes das ferramentas instaladas no ambiente e smoke manual do VS Code.

## v2 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais: `docker-compose.yml`, `.vscode/launch.json`, `rastro-api/package.json`, `rastro-ai/Dockerfile.dev`, `rastro-ai/README.md` e `rastro-api/README.md`.
- Mudanças: configuração Docker-first com inspector Node em `9229`, `debugpy` em `5678`, attach composto e comandos documentados.
- Problema resolvido: divergência entre o perfil local da v1 e o runtime oficial em containers.
- Pendências: executar build/up Docker e confirmar attach manual no VS Code.

## Verificações da v2 — 2026-10-24 -03:00

- Build e subida Docker: aprovados; containers da API, IA e PostgreSQL ficaram saudáveis.
- Health checks API/Python e inspector Node: aprovados com HTTP `200` e resposta em `9229/json/list`.
- Hook estrutural, JSON, Compose config e whitespace: aprovados.
- Attach visual no VS Code: permanece como ação manual pendente.

## v3 — 2026-10-24 -03:00

- Status: `applied`.
- Mudanças: comando `curl` de upload do fixture foi adicionado ao README da API.
- Problema resolvido: falta de instrução completa para reproduzir o upload durante o debug.
- Verificação: controller, rota, campos multipart e fixture conferidos; execução real do upload ficou pendente por depender de credencial OpenAI.

## v4 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: dependência `multer` adicionada ao manifest da API após o smoke retornar `property file should not exist`.
- Problema resolvido: parser multipart ausente no container da API.
- Pendências: rebuild da API, smoke HTTP do upload e confirmação do status conforme a credencial OpenAI.

## v5 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: endpoint passou a validar somente `projectId` no body e receber `file` exclusivamente por `@UploadedFile()`.
- Problema resolvido: `ValidationPipe` rejeitava o campo multipart como propriedade extra.
- Pendências: rebuild da API e novo smoke do upload.

## v6 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: fallback para `request.file` adicionado ao controller de upload.
- Problema resolvido: arquivo multipart parseado pelo Multer não chegava ao parâmetro `@UploadedFile()`.
- Pendências: rebuild da API e repetição do `curl` documentado.

## v7 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: comando `curl` corrigido com `file=@$PWD/...`; controller voltou ao binding padrão.
- Problema resolvido: o caminho era enviado como texto porque faltava o marcador `@`.
- Verificação: rebuild da API e novo smoke executados; resposta HTTP `200` com `status: ready`.

## v8 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: chamada direta `POST /index` do Python documentada no README da API.
- Problema resolvido: falta de instrução para isolar a indexação sem passar pela API.
- Verificação: rota, payload, porta publicada e resposta esperada conferidos contra o serviço real.

## v9 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: README raiz criado com a ordem correta e os requests de health, Python direto e API integrada.
- Problema resolvido: instruções de validação estavam distribuídas e não havia roteiro central.
- Verificação: comandos e portas conferidos contra Compose, launch.json e endpoints reais.

## v10 — 2026-10-24 -03:00

- Status: `applied`.
- Mudança: fluxo API → Python e variáveis `AI_INDEXING_URL`/`AI_INDEXING_TIMEOUT_MS` documentados nos READMEs raiz e da API.
- Problema resolvido: delegação interna da indexação não estava explicitada.
- Verificação: Compose, cliente HTTP, referências documentais e hook estrutural conferidos.

## Finalização — 2026-10-24 -03:00

- Status: `verified`.
- Todas as versões `v1` a `v10` foram conferidas; cada uma permanece com status final `applied`.
- Verificações: builds Docker, containers saudáveis, health checks, inspector Node, `debugpy`, upload API com `file=@...` retornando `200`/`ready`, indexação direta Python, JSON, Compose, whitespace e hook estrutural.
- Pendência não bloqueadora: attach visual no VS Code depende da sessão gráfica do usuário e não foi automatizado.
- Próxima etapa: nenhuma ativada; `CURRENT.md` permanece em `013` como último registro finalizado.

## Evidências finais — 2026-10-24 -03:00

- API no container: 10 testes Jest aprovados; Python: 26 testes unittest aprovados.
- Docker: `docker compose build`, `docker compose config` e containers `api`, `ai-indexer` e `vector-db` saudáveis.
- HTTP: health checks API/Python aprovados; upload com `file=@...` retornou HTTP `200` e `status: ready`; indexação direta Python aprovada.
- Estrutural: JSON, `git diff --check` e validação dos 22 arquivos de handoff aprovados.
- Observação: `npm test` no host não foi executável por ausência de `node_modules`; o mesmo teste foi aprovado dentro do container oficial.

## Commit final — 2026-10-24 -03:00

- Commit: `4e10498` — `Configura debug Docker para API e Python`.
- Lista explícita: configuração VS Code, Compose, Dockerfile Python de desenvolvimento, manifest/controller/READMEs da API e IA, README raiz, `.gitignore` e controles/handoffs da implementação `013`.
- Verificação pós-commit: commit criado sem alterações não relacionadas no índice; implementação permanece `verified`.
