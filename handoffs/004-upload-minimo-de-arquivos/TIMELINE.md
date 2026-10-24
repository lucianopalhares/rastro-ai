# Linha do tempo — 004 Upload mínimo de arquivos

## v1 — 2026-10-23 -03:00

- Status: `proposed` | Versão-base: implementação `003` em status `verified`.
- Arquivos conferidos: `document.ts`, `documents.controller.ts`, `documents.module.ts`, `create-document.use-case.ts`, `document.repository.ts`, `package.json`, `main.ts`, `.gitignore` e Compose reais.
- Reconciliação: o fluxo JSON existente foi considerado preservado; não havia endpoint de upload, abstração de armazenamento ou associação de arquivo.
- Mudança proposta: adicionar contrato de armazenamento, adaptador local, caso de uso multipart, metadados opcionais no documento e testes unitários.
- Problema resolvido: ausência de recebimento e persistência mínima de arquivos `.md` e `.txt` vinculados a um projeto/documento.
- Pendências: aplicação manual, teste HTTP multipart e confirmação dos limites de armazenamento local.
- Verificação prevista: `npm test`, `npm run build` e chamada multipart com arquivo válido e inválido.

## v1 — 2026-10-23 -03:00 — Verificação

- Status: `verified` | A implementação foi aplicada diretamente na API real; o registro permanece sem código copiável.
- Arquivos alterados: domínio, contrato de armazenamento, adaptador local, caso de uso, módulo, controller e teste unitário.
- Comentários: classes, interfaces, construtores, métodos e cenários alterados receberam JSDoc com descrição e histórico `v1`.
- Verificação: `docker compose build api` passou; `docker compose run --rm --no-deps api npm test -- --runInBand` passou com 2 suítes e 7 testes; build passou.
- Impacto: upload multipart limitado a 5 MiB, extensões `.md`/`.txt`, conteúdo não vazio e associação por `source.storageKey`.
- Pendências: smoke HTTP multipart e substituição futura do armazenamento local por object storage permanecem fora desta rodada.

## Finalização — 2026-10-23 -03:00

- Status: `verified` | Todas as versões existentes foram conferidas; a `v1` está aplicada diretamente e verificada.
- Verificação adicional: smoke HTTP válido retornou `201` com `pending` e `source.storageKey`; extensão `.pdf` retornou `400`.
- Limitações: armazenamento local e indexação assíncrona continuam como responsabilidades das próximas etapas.
- Avanço: `CURRENT.md` será atualizado para `005`, conforme a sequência registrada.

## v2 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: `rastro-api/src/modules/documents/presentation/documents.controller.ts` e `.gitignore`; o endpoint permanece limitado a `.md`/`.txt` não vazios e o fixture é versionável.
- Mudança aplicada: criado `rastro-api/test/fixtures/upload/meeting.md` com conteúdo reutilizável para simulações manuais de upload.
- Problema resolvido: ausência de um arquivo estável no repositório para repetir o smoke test multipart.
- Impacto: nenhuma alteração no código da API, no armazenamento gerado ou nos testes automatizados.
- Pendências: executar o smoke HTTP usando o fixture quando a API estiver disponível.
- Verificação: fixture criado e conteúdo não vazio confirmado por leitura do arquivo; comando curl completo registrado em `v2/README.md`.

## v3 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivo real conferido: `rastro-api/test/fixtures/upload/meeting.md`; a versão `v2` estava aplicada e continha conteúdo em tópicos.
- Mudança aplicada: substituído o conteúdo por uma conversa curta e subsequente entre Marina, Rafael e João, com decisão e próximos passos.
- Problema resolvido: fixture anterior não simulava o formato irregular de uma transcrição de reunião.
- Impacto: melhora a representatividade do arquivo para uploads e futuras etapas de extração, sem alterar o endpoint.
- Pendências: executar smoke HTTP e, quando disponível, validar extração sobre a transcrição.
- Verificação: conteúdo e participantes conferidos; comandos completos registrados em `v3/README.md`.

## v4 — 2026-10-24 -03:00

- Status: `verified`.
- Arquivo real/endpoint conferidos: `rastro-api/test/fixtures/upload/meeting.md` e `POST /api/v1/documents/upload`.
- Evidência: smoke HTTP manual retornou `HTTP/1.1 201 Created` com `projectId: project-1`, `name: meeting.md`, conteúdo da transcrição, `source.storageKey` terminado em `.md` e `status: pending`.
- Problema resolvido: confirmação de que o fixture versionado pode ser usado no upload real local.
- Impacto: nenhum código alterado; indexação e extração continuam pendentes para etapas futuras.
- Pendências: nenhuma dentro do critério do upload mínimo.
- Verificação: comando e resultado completos registrados em `v4/README.md`.

## Finalização — 2026-10-24 -03:00

- Status: `verified`.
- Registros conferidos: README consolidado, versões `v1`–`v4`, timeline da implementação, timeline global e `CURRENT.md`.
- Verificações: hook estrutural válido; fixture não vazio com participantes; smoke HTTP `201 Created`; testes Docker com 2 suítes/7 testes; build NestJS aprovado.
- Avanço: `CURRENT.md` atualizado de `004` para `005`, conforme `SEQUENCE.md`.
- Commit: será registrado na entrada final após a criação do commit explícito da tarefa.
