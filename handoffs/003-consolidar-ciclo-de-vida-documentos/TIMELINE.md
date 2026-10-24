# Timeline — 003 Consolidar ciclo de vida dos documentos

## v1 — 2026-10-23

- Status: `proposed` | Versão-base: estado real da API NestJS, sem versão anterior desta implementação.
- Arquivos conferidos: `rastro-ai/src/modules/documents/domain/document.ts`, `application/create-document.use-case.ts`, `presentation/documents.controller.ts`, `src/main.ts`.
- Reconciliação: contrato atual encontrado com `pending`/`ready`, sem `projectId` e sem transições; nenhuma proposta anterior desta tarefa aplicada.
- Mudança proposta: adicionar `projectId`, estados de processamento e método de transição no domínio; propagar `projectId` no caso de uso e no DTO HTTP.
- Problema resolvido: documentos ainda não possuem escopo mínimo de projeto nem ciclo explícito para futura indexação.
- Pendências: aplicação manual; persistência, upload, worker e IA permanecem nas tarefas posteriores.
- Verificação: `npm test`, `npm run build` e teste HTTP de criação com e sem `projectId`.

## v2 — 2026-10-23

- Status: `proposed` | Versão-base: `v1`, invalidada para aplicação porque a API foi movida para `rastro-api`.
- Arquivos conferidos: os mesmos arquivos reais, agora em `rastro-api/src/modules/documents/`, além de `rastro-api/src/main.ts`.
- Reconciliação: código da API permanece equivalente; nenhum trecho da `v1` foi aplicado e os caminhos antigos foram considerados divergentes.
- Mudança proposta: repetir somente o contrato da `v1` com caminhos absolutos atuais e metadados aceitos pelo validador.
- Problema resolvido: handoffs da rodada anterior apontavam para a antiga pasta `rastro-ai` da API.
- Pendências: aplicação manual dos quatro handoffs; `rastro-ai` e `rastro-front` existem como destinos, ainda sem arquivos versionados.
- Verificação: executar o hook de validação, `npm test`, `npm run build` e teste HTTP de criação.

## v3 — 2026-10-23

- Status: `proposed` | Versão-base: `v2`, após aplicação parcial confirmada pelos erros do TypeScript.
- Arquivos conferidos: `rastro-api/src/modules/documents/domain/document.ts`, `application/create-document.use-case.ts` e `presentation/documents.controller.ts`.
- Reconciliação: `create-document.use-case.ts` já contém `projectId`; o domínio ainda é antigo; o controller contém `projectId`, mas perdeu `content`.
- Mudança proposta: corrigir somente o domínio e o DTO; não repetir o caso de uso já aplicado.
- Problema resolvido: incompatibilidade entre o comando de criação, o agregado e o payload HTTP.
- Pendências: aplicação manual da `v3` e execução de build, testes e chamadas HTTP.
- Verificação: hook estrutural, `npm run build` e `npm test -- --runInBand` em `rastro-api`.

## v4 — 2026-10-23

- Status: `proposed` | Versão-base: `v3`, após falha do `docker compose up --build` causada pelo caminho antigo.
- Arquivos conferidos: `/home/dev/dev/ia/rastro-ai/docker-compose.yml` e Dockerfiles reais em `rastro-api`.
- Reconciliação: o Compose ainda usa `./rastro-ai` como contexto e volume; `rastro-api/Dockerfile.dev` existe e é o destino correto.
- Mudança proposta: apontar contexto de build e bind mount para `rastro-api`, preservando porta, comando e health check.
- Problema resolvido: erro `failed to read dockerfile: open Dockerfile.dev: no such file or directory`.
- Pendências: aplicação manual e execução do build do Compose; handoffs `v1`–`v3` permanecem preservados.
- Verificação: `docker compose config` e `docker compose up --build`.

## v5 — 2026-10-23

- Status: `proposed` | Versão-base: `v4`; o README da raiz ainda não existia na aplicação real.
- Arquivos conferidos: ausência de `/home/dev/dev/ia/rastro-ai/README.md` e comandos previstos nos handoffs anteriores.
- Reconciliação: não há README anterior a preservar; nenhuma instrução de teste está disponível na raiz.
- Mudança proposta: criar README raiz com caminhos das aplicações, inicialização Docker e comandos de build/teste da API.
- Problema resolvido: os comandos de verificação estavam dispersos somente nos handoffs.
- Pendências: aplicação manual do novo README; resultados dos comandos continuam dependentes da aplicação das versões anteriores.
- Verificação: conferir os comandos documentados e executar `npm test -- --runInBand` e `npm run build` em `rastro-api`.

## Finalização solicitada — 2026-10-23

- Status: `proposed` mantido; a implementação não pode ser marcada como `applied` ou `verified`.
- Versões conferidas: `v1` a `v5`; o contrato da API e a alteração do Compose estão presentes na aplicação real, mas o README raiz da `v5` está ausente.
- Verificações: `docker compose config` passou; `npm test -- --runInBand` e `npm run build` falharam porque `jest` e `nest` não estão instalados; o hook falhou por operação ausente em handoff legado.
- Pendências: aplicar o README raiz, instalar/restaurar dependências da API, repetir testes/build e corrigir os metadados dos handoffs antes de nova finalização.
- Controle: `CURRENT.md` permanece em `003`; a implementação e os arquivos originais foram preservados.

## v5 — 2026-10-23 — Rodada descartada

- Status: `rolled-back`; a rodada continha somente a proposta de criar o README raiz e não foi aplicada.
- Ação: os arquivos de `v5/` não estão presentes; `v1`–`v4` permanecem preservadas.
- Impacto: a documentação de execução na raiz não faz mais parte desta tarefa.
- Pendências: permanecem as verificações da `v4`, incluindo dependências da API e validação dos handoffs.

## Finalização solicitada após descarte da v5 — 2026-10-23

- Status: `proposed` mantido; `v1`–`v4` ainda não têm confirmação explícita de aplicação nem verificações concluídas.
- Verificações: `docker compose config` passou; `npm test -- --runInBand` e `npm run build` continuam falhando porque `jest` e `nest` não estão instalados.
- Controle: `v5` permanece removida, `CURRENT.md` permanece em `003` e a tarefa `004` não foi ativada.

## v6 — 2026-10-23

- Status: `proposed` | Versão-base: `v4`; `v5` descartada antes da aplicação.
- Arquivos conferidos: `rastro-api/package.json`, `rastro-api/tsconfig.json` e `rastro-api/src/modules/documents/domain/document.spec.ts`.
- Reconciliação: o teste de domínio já existe e está adequado; o ambiente não encontra `jest`/`nest`, e o pacote mistura Jest 30 com `ts-jest` 29 sem configuração Jest explícita.
- Mudança proposta: alinhar Jest/types com `ts-jest`, explicitar o script e adicionar `jest.config.js`; nenhum teste de domínio é repetido.
- Problema resolvido: prepara a execução dos testes TypeScript após instalação das dependências.
- Pendências: aplicação manual, `npm install`, testes e build; avaliação HTTP permanece dependente da infraestrutura local.
- Verificação: validação do hook para os dois handoffs, `npm test -- --runInBand` e `npm run build`.

## v6 — Reconciliação do formato do handoff — 2026-10-23

- Status: `proposed`; a versão foi refeita após identificar nomes e seções incompatíveis com `AGENTS.md` e `docs/instruction.md`.
- Ajuste: os arquivos usam os nomes originais `package.json` e `jest.config.js`, sem o sufixo `.handoff.md`.
- Ajuste de conteúdo: cada handoff contém ponto estrutural, arquivo completo, explicação, dependências e verificação; o JavaScript usa comentário `////////////` antes do bloco novo.
- Exceção: `package.json` permanece JSON estrito e não aceita comentários; a alteração está justificada no handoff.
- Pendências: aplicação manual e validação; `handoffs/README.md` ainda diverge de `AGENTS.md` e `docs/instruction.md` quanto ao sufixo.

## Fluxo de handoff atualizado — 2026-10-23

- Status: `proposed`; o formato da `v6` foi corrigido conforme a regra solicitada.
- Arquivos de saída: `v6/api/package.json` e `v6/api/jest.config.js` contêm somente os arquivos integrais finais.
- Metadados: operação, âncoras, motivo, impacto, dependências e verificações ficam em `v6/README.md`.
- Comentários: somente blocos relevantes recebem comentários de bloco `/* ... */`; JSON permanece sem comentários por exigência de sintaxe.
- Regras sincronizadas: `AGENTS.md`, `docs/instruction.md`, `handoffs/README.md` e o hook de validação foram atualizados para o novo fluxo.

## Verificação Docker da v6 — 2026-10-23

- Ajuste: os testes e o build da API devem ser executados pelo serviço `api` do Compose, não diretamente no host.
- Comandos: `docker compose build api`, `docker compose run --rm --no-deps api npm test -- --runInBand` e `docker compose run --rm --no-deps api npm run build`.
- Motivo: o `Dockerfile.dev` instala as dependências e o Compose monta a API no ambiente correto.

## v7 — 2026-10-23

- Status: `proposed` | Versão-base: `v6`; a aplicação real foi novamente conferida antes da geração.
- Arquivo conferido: `rastro-api/tsconfig.json`; `package.json`, `jest.config.js` e `document.spec.ts` confirmam o contexto do erro.
- Reconciliação: `v6` já deixou Jest e `@types/jest` instalados/configurados; o `tsconfig.json` permanece sem `compilerOptions.types`.
- Mudança proposta: criar `v7/api/tsconfig.json` integral com `types: ["node", "jest"]`; as demais pastas de escopo permanecem vazias.
- Problema resolvido: o compilador passa a carregar os globais `describe`, `it` e `expect` usados pelo teste de domínio.
- Pendências: aplicação manual, execução dos testes e build; a implementação continua `proposed` e não libera a tarefa `004`.
- Verificação: `npx tsc --noEmit --types node,jest` passou no container; validar o arquivo entregue com o hook e repetir os comandos Docker após aplicação.

## Finalização verificada — 2026-10-23

- Status: `verified`; a aplicação real contém as propostas das versões `v1`–`v7`, incluindo `types: ["node", "jest"]` no `rastro-api/tsconfig.json`.
- Arquivos conferidos: domínio, caso de uso, controller, Compose, `package.json`, `jest.config.js`, `tsconfig.json` e teste de domínio na aplicação real.
- Verificações: `docker compose config` passou; `docker compose run --rm --no-deps api npm test -- --runInBand` passou com 1 suíte e 5 testes; `npm run build` passou.
- Verificação adicional: `npx tsc --noEmit` passou no container e o hook validou `v7/api/tsconfig.json`.
- Impacto: a implementação está pronta para uso; `CURRENT.md` foi atualizado para a próxima tarefa `004` registrada em `SEQUENCE.md`.
- Commit: não gerado; o worktree contém alterações de movimentação e arquivos não relacionados que impedem isolamento seguro.
