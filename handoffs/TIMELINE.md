# Linha do tempo das implementações

Cada registro tem no máximo 8 linhas; detalhes técnicos ficam na pasta numerada correspondente.

## 001 — Exemplo de validação de citações

- Data/hora: 2026-10-23 11:03 -03:00 | Status: `proposed`
- Aplicação afetada: `ia`
- Por que foi feito: demonstrar handoffs de validação de citações sem editar o código original.
- Impactos: apresenta operações insert, replace e remove com âncoras e código copiável.
- Resolve: define um padrão revisável para mudanças no fluxo LangGraph.
- Pasta: `handoffs/001-exemplo-validacao-citacoes/`

## 002 — Criar API NestJS DDD modular

- Data/hora: 2026-10-23 00:00 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api`)
- Por que foi feito: criar uma base NestJS atual com módulos DDD simples e TypeScript.
- Impactos: adiciona bootstrap, configuração, health check, documentos em memória e Dockerfile.
- Resolve: ausência de API executável; critério: build, testes e endpoints básicos funcionarem após aplicação.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 002 — Compose da API na raiz

- Data/hora: 2026-10-23 00:00 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`docker-compose.yml` na raiz)
- Por que foi feito: permitir executar a API real em `rastro-ai/` pela raiz do projeto.
- Impactos: adiciona serviço `api`, publicação da porta 3000 e health check sem novos serviços externos.
- Resolve: ausência de composição Docker raiz; critério: `docker compose config`, build e health check concluírem.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 002 — Hot reload no Compose da API

- Data/hora: 2026-10-23 00:00 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`docker-compose.yml` na raiz)
- Por que foi feito: refletir alterações em `rastro-ai/src/` sem reinício manual do container.
- Impactos: usa bind mount do código, volume anônimo para `node_modules` e Nest em modo watch.
- Resolve: ciclo local lento de edição e reinicialização; critério: alteração de código disparar reload automático.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 002 — Revisão do estado parcial antes do Compose

- Data/hora: 2026-10-23 00:00 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`docker-compose.yml` na raiz)
- Por que foi feito: evitar sobrescrever alterações parcialmente aplicadas da implementação ativa.
- Impactos: exige reler os arquivos reais e redefinir a operação e as âncoras conforme o estado encontrado.
- Resolve: risco de aplicar snippets históricos como se fossem o código atual; critério: handoff reconciliado antes da aplicação.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 002 — Compatibilidade do tsconfig com TypeScript 6

- Data/hora: 2026-10-23 00:00 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-ai/tsconfig.json`)
- Por que foi feito: corrigir `TS5011` e `TS5101` após a atualização do TypeScript exigida pelo NestJS Schematics 12.
- Impactos: define `rootDir` em `src` e silencia a depreciação de `baseUrl`, preservando o alias `@/*`.
- Resolve: falha do watch e do build da API no TypeScript 6; critério: watch e build Docker concluírem sem os dois erros.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 002 — Corrigir resolução de dependências no Docker

- Data/hora: 2026-10-23 00:00 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-ai/package.json` e `rastro-ai/Dockerfile.dev`)
- Por que foi feito: alinhar TypeScript ao peer dependency do NestJS Schematics 12 e tornar a instalação determinística.
- Impactos: exige gerar e versionar `rastro-ai/package-lock.json`; o build passa a usar `npm ci`.
- Resolve: falha `ERESOLVE` no `docker compose up --build`; critério: build, instalação, testes e compilação concluírem.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 002 — Corrigir instalação Docker sem lockfile

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-ai/Dockerfile.dev`)
- Por que foi feito: o build usa `npm ci`, mas o contexto não contém lockfile.
- Impactos: usa `npm install` no desenvolvimento; a instalação fica não determinística até o lockfile ser versionado.
- Resolve: erro `EUSAGE` na etapa de dependências; critério: `docker compose build api` concluir.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/v2/`

## 002 — Compatibilizar TypeScript 6

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-ai/tsconfig.json`)
- Por que foi feito: o watch reporta `TS5011` por falta de `rootDir` e `TS5101` pela depreciação de `baseUrl`.
- Impactos: define `rootDir` em `src` e silencia a depreciação durante a migração para TypeScript 6.
- Resolve: falha do watch antes da compilação; critério: watch e build concluírem sem os dois erros.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/v3/`

## 002 — Adicionar controller de documentos

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`src/modules/documents/presentation/documents.controller.ts`)
- Por que foi feito: `DocumentsModule` importa um controller que não existe no caminho esperado.
- Impactos: adiciona os endpoints de criação e listagem de documentos.
- Resolve: erro `TS2307` durante o watch; critério: build e chamadas HTTP concluírem.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/v4/`

## 002 — Regras de arquivos não versionáveis

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `root` (configuração compartilhada em `.gitignore` na raiz)
- Por que foi feito: evitar versionar dependências, builds, caches, logs e ambientes locais.
- Impactos: ignora artefatos derivados e preserva `.env.example`, código, documentação e handoffs.
- Resolve: ausência de regras globais de exclusão; critério: `git check-ignore` confirmar os padrões esperados.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/v5/`

## 002 — Finalização da aplicação

- Data/hora: 2026-10-23 -03:00 | Status: `applied`
- Aplicação afetada: API NestJS modular e configuração compartilhada da raiz.
- Por que foi feita: o responsável confirmou a aplicação dos handoffs da implementação.
- Impactos: implementação encerrada como aplicada; testes técnicos ainda não registrados.
- Resolve: ciclo de aplicação manual da tarefa 002; critério restante: build, testes e `git check-ignore`.
- Pasta: `handoffs/002-criar-api-nestjs-ddd-modular/`

## 003 — Consolidar ciclo de vida dos documentos

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-ai`)
- Por que foi feita: iniciar a continuação mínima da Fase 1 com um contrato documental preparado para indexação.
- Impactos: adiciona `projectId`, estados de processamento e transições determinísticas, sem banco ou IA.
- Resolve: ausência de escopo de projeto e de ciclo explícito no agregado `Document`.
- Critério: build, testes unitários e validação HTTP do novo campo passarem.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/`

## 003 — Reconciliação dos caminhos das aplicações

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api`)
- Por que foi feita: atualizar a rodada ativa após a API ser movida de `rastro-ai` para `rastro-api`.
- Impactos: cria a `v2` da tarefa sem sobrescrever a `v1`; os destinos oficiais são `rastro-api`, `rastro-front` e `rastro-ai`.
- Resolve: caminhos absolutos antigos nos handoffs e metadados incompatíveis com a validação.
- Critério: hook estrutural aprovado e handoff pronto para aplicação manual.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v2/`

## 003 — Correção da aplicação parcial

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api`)
- Por que foi feita: corrigir a aplicação parcial que deixou o domínio antigo e removeu `content` do DTO.
- Impactos: a `v3` contém somente os dois arquivos ainda divergentes; o caso de uso já aplicado não é repetido.
- Resolve: erros `TS2353` e `TS2345` reportados no watch da API.
- Critério: build, testes e POST com payload completo passarem.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v3/`

## 003 — Corrigir caminho da API no Compose

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `root` (`docker-compose.yml`)
- Por que foi feita: o Compose ainda procurava o Dockerfile na antiga pasta `rastro-ai`.
- Impactos: build e volume de desenvolvimento passam a usar `rastro-api`.
- Resolve: erro de arquivo `Dockerfile.dev` inexistente durante `docker compose up --build`.
- Critério: `docker compose config`, build e health check concluírem.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v4/`

## 003 — Documentar comandos de teste na raiz

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `root` (`README.md`)
- Por que foi feita: centralizar os comandos para iniciar, compilar e testar a API.
- Impactos: cria uma orientação inicial reproduzível para desenvolvimento local.
- Resolve: ausência de README raiz e de um ponto único para os comandos de verificação.
- Critério: README aplicado e comandos conferidos contra `rastro-api/package.json`.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v5/`

## 003 — Finalização bloqueada por aplicação parcial

- Data/hora: 2026-10-23 -03:00 | Status: `proposed` (aplicação parcial)
- Aplicação afetada: API `rastro-api` e raiz compartilhada.
- Por que foi feita: reconciliar a solicitação de finalização com o estado real das versões `v1`–`v5`.
- Impactos: contrato e Compose estão presentes, mas README, dependências e verificações finais permanecem pendentes.
- Resolve: registra evidência da tentativa de finalização sem avançar indevidamente a sequência.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/`

## 003 — Finalização após descarte da v5

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: API `rastro-api` e handoffs `v1`–`v4`.
- Por que foi feita: nova solicitação explícita de finalização após remover a rodada `v5`.
- Impactos: a tarefa permanece ativa porque testes/build continuam indisponíveis e não há confirmação de aplicação completa.
- Resolve: confirma que a sequência não avança enquanto persistirem as pendências.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/`

## 003 — Descartar rodada v5

- Data/hora: 2026-10-23 -03:00 | Status: `rolled-back`
- Aplicação afetada: handoff da raiz compartilhada.
- Por que foi feita: o responsável solicitou não utilizar a rodada `v5`.
- Impactos: a proposta de criar README raiz foi removida; `v1`–`v4` permanecem intactas.
- Resolve: elimina a rodada não desejada sem alterar os arquivos originais da aplicação.
- Pasta: `handoffs/003-consolidar-ciclo-vida-documentos/`

## 003 — Finalização solicitada após descarte da v5

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: API `rastro-api` e handoffs `v1`–`v4`.
- Por que foi feita: registrar nova solicitação de finalização após o descarte da `v5`.
- Impactos: a tarefa permanece ativa porque testes/build continuam indisponíveis e não há confirmação de aplicação completa.
- Resolve: confirma que a sequência não avança enquanto persistirem as pendências.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/`

## 003 — Configuração do Jest

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api`)
- Por que foi feita: preparar a execução dos testes TypeScript após a instalação das dependências.
- Impactos: alinha Jest/types com `ts-jest`, explicita o script e adiciona configuração Jest.
- Resolve: ausência de configuração reproduzível para os testes da API.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v6/`

## 003 — Reconciliação do formato do handoff

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api`)
- Por que foi feita: corrigir nomes e seções incompatíveis com `AGENTS.md` e `docs/instruction.md`.
- Impactos: os arquivos usam nomes originais e registram operações, âncoras, dependências e verificações.
- Resolve: divergências de formato dos handoffs da `v6`.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v6/`

## 003 — Verificação Docker da v6

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api`).
- Por que foi feita: definir os comandos de teste e build no ambiente Docker correto.
- Impactos: usa `docker compose build api` e comandos `docker compose run --rm --no-deps api`.
- Resolve: diferença entre dependências do host e dependências instaladas no container.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v6/`

## 003 — Explicitar tipos globais do Jest

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: `api` (`rastro-api/tsconfig.json`)
- Por que foi feita: `@types/jest` estava instalado, mas o TypeScript não reconhecia `describe`, `it` e `expect`.
- Impactos: os testes TypeScript passam a carregar explicitamente os tipos `node` e `jest`.
- Resolve: erro TS2593/TS2304 durante `npm test`; critério: testes e build Docker passarem após aplicação.
- Pasta: `handoffs/003-consolidar-ciclo-de-vida-documentos/v7/`

## 003 — Finalização verificada

- Data/hora: 2026-10-23 -03:00 | Status: `verified`
- Aplicação afetada: `api` (`rastro-api`) e configuração compartilhada já proposta nas versões anteriores.
- Por que foi feita: confirmar a aplicação integral da implementação e os critérios técnicos pendentes.
- Impactos: ciclo documental e execução dos testes estão verificados; a implementação permanece preservada como histórico.
- Resolve: falha de tipos globais do Jest e pendências de build/teste da tarefa 003.
- Verificação: Compose config, suíte Jest (5 testes), TypeScript e build passaram; nenhum commit foi gerado por alterações não relacionadas no worktree.
- Pasta: `handoffs/003-consolidar-ciclo-vida-documentos/`

## 004 — Upload mínimo de arquivos

- Data/hora: 2026-10-23 -03:00 | Status: `proposed`
- Aplicação afetada: API (`rastro-api`).
- Por que foi feita: iniciar a segunda etapa da Fase 1 após a tarefa 003 verificada.
- Impactos: propõe endpoint multipart, validação de `.md`/`.txt`, armazenamento local configurável e associação ao documento.
- Resolve: ausência de recebimento e persistência mínima de arquivos; indexação e extração continuam fora do escopo.
- Critério: testes, build e smoke HTTP do upload válido e inválido passarem após aplicação manual.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/`

## 004 — Upload mínimo de arquivos verificado

- Data/hora: 2026-10-23 -03:00 | Status: `verified`
- Aplicação afetada: API (`rastro-api`), alterada diretamente conforme o novo fluxo.
- Por que foi feita: implementar o recebimento, armazenamento e associação mínima de `.md` e `.txt`.
- Impactos: endpoint multipart, armazenamento local configurável, metadados de origem e limite de 5 MiB; indexação permanece futura.
- Resolve: ausência de upload funcional; 2 suítes e 7 testes, build Docker e build Nest passaram.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/` | Próxima ação: finalizar explicitamente a tarefa 004.

## 004 — Finalização verificada

- Data/hora: 2026-10-23 -03:00 | Status: `verified`
- Aplicação afetada: API (`rastro-api`).
- Por que foi feita: concluir a tarefa após testes, build e smoke HTTP do upload.
- Impactos: tarefa encerrada com upload válido e rejeição de extensão inválida comprovados.
- Resolve: ciclo de implementação do upload mínimo; armazenamento local e indexação permanecem nas etapas seguintes.
- Verificação: `201` para `.md`, `400` para `.pdf`, 2 suítes/7 testes, build Nest e build Docker passaram.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/`.

## 004 — Fixture versionado para simulação de upload

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: API `rastro-api` (fixture de teste manual).
- Por que foi feita: disponibilizar conteúdo reutilizável para simular uploads futuros.
- Impactos: adiciona `rastro-api/test/fixtures/upload/meeting.md`; não altera o código da API.
- Resolve: ausência de arquivo estável para o smoke test multipart.
- Verificação: conteúdo não vazio confirmado; comando curl registrado no handoff `v2`.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/v2/`

## 004 — Fixture em formato de transcrição de reunião

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: API `rastro-api` (fixture de teste manual).
- Por que foi feita: simular uma reunião curta com falas naturais entre participantes.
- Impactos: atualiza `rastro-api/test/fixtures/upload/meeting.md`; não altera o código da API.
- Resolve: conteúdo excessivamente estruturado para o cenário de transcrição.
- Verificação: arquivo não vazio e falas de três participantes conferidas; smoke HTTP permanece manual.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/v3/`

## 004 — Upload do fixture verificado

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: API `rastro-api` e fixture versionado.
- Por que foi feita: confirmar o upload real da transcrição de reunião pelo endpoint multipart.
- Impactos: nenhum código novo; o fixture foi aceito e associado ao projeto `project-1`.
- Resolve: validação manual pendente do arquivo reutilizável.
- Verificação: `HTTP/1.1 201 Created`, `status: pending`, conteúdo preservado e `source.storageKey` terminado em `.md`.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/v4/`

## 004 — Finalização da implementação

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: API `rastro-api` e fixture versionado.
- Por que foi feita: concluir a implementação após confirmação do upload, testes e build.
- Impactos: `CURRENT.md` avança para `005`; alterações não relacionadas permanecem fora do commit.
- Resolve: ciclo da implementação `004` encerrado com evidência de aplicação e verificação.
- Verificação: hook válido, smoke HTTP `201`, 2 suítes/7 testes e build NestJS aprovados.
- Pasta: `handoffs/004-upload-minimo-de-arquivos/`.
- Commit: `71f41be` — `Finalizar upload mínimo de arquivos`.

## 005 — Extração e chunking

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: criar a primeira capacidade executável de extração UTF-8 e divisão determinística após o upload verificado.
- Impactos: adiciona pacote Python, configuração mínima e cinco testes; embeddings, fila e vector store permanecem futuros.
- Resolve: ausência de texto normalizado, chunks, offsets e contrato testável para indexação.
- Verificação: `python3 -m unittest discover -s tests -v` passou com 5 testes; hook estrutural será executado antes da entrega.
- Pasta: `handoffs/005-extracao-e-chunking/`.

## 005 — Verificação e finalização

- Data/hora: 2026-10-24 18:28 -03:00 | Status: `verified`
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: concluir o ciclo após validação da implementação de extração e chunking.
- Impactos: `CURRENT.md` avança para `006`; nenhuma alteração de runtime foi feita nesta finalização.
- Resolve: implementação 005 verificada com testes, compilação e hook estrutural.
- Verificação: 7 testes unitários passaram, `compileall` passou e 8 arquivos de handoff foram validados.
- Pasta: `handoffs/005-extracao-e-chunking/`.

## 006 — Retrieval vetorial mínimo

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: permitir consulta de chunks relevantes com isolamento obrigatório por projeto.
- Impactos: adiciona retrieval síncrono, lexical e determinístico em memória; embeddings, banco e worker permanecem fora do escopo.
- Resolve: ausência de contrato, indexação e consulta após a geração de chunks.
- Verificação: 11 testes, `compileall` e hook estrutural passaram.
- Pasta: `handoffs/006-retrieval-vetorial-minimo/` | Próxima ação: finalizar tarefa 006.

## 006 — Finalização verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: confirmar testes, registros e critérios da implementação de retrieval mínimo.
- Impactos: `CURRENT.md` avança para `007`; alterações futuras de embeddings e persistência continuam fora do escopo.
- Resolve: ciclo da implementação 006 encerrado com retrieval filtrado por projeto verificado.
- Verificação: 11 testes, `compileall` e hook estrutural passaram.
- Pasta: `handoffs/006-retrieval-vetorial-minimo/` | Próxima ação: iniciar 007.

## 007 — Respostas com citações

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: transformar chunks recuperados em resposta com fonte ou ausência explícita de evidência.
- Impactos: resposta extrativa determinística, sem LLM, rede, embeddings ou custo adicional de geração.
- Resolve: contrato de resposta/citação, fachada pública, isolamento por projeto e testes do comportamento.
- Pasta: `handoffs/007-respostas-com-citacoes/`.

## 007 — Finalização verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: concluir a resposta extrativa com citações e ausência explícita de evidência.
- Impactos: `CURRENT.md` avança para `008`; API, frontend, worker, LLM e evaluation permanecem fora da 007.
- Resolve: critério da etapa confirmado com testes, compilação, smoke integrado e jornada de uso documentada.
- Verificação: hook estrito válido, 14 testes, `compileall` e smoke integrado aprovados.
- Pasta: `handoffs/007-respostas-com-citacoes/` | Próxima ação: iniciar `008-evaluation-baseline`.

## 008 — Evaluation baseline proposta

- Data/hora: 2026-10-24 -03:00 | Status: `proposed`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: criar dataset e referência reproduzível antes de evoluir retrieval ou geração.
- Impactos: avaliação determinística local; runtime permanece inalterado e DeepEval fica fora do escopo.
- Resolve: ausência de medição versionada para fontes, citações, ausência de evidência e isolamento.
- Verificação: prevista para `v1`, com 20 casos e métricas reproduzíveis.
- Pasta: `handoffs/008-evaluation-baseline/`.

## 008 — Evaluation baseline aplicada

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: versionar 20 casos e medir o fluxo determinístico antes de novas evoluções.
- Impactos: adiciona evaluation local sem alterar runtime, modelo, rede ou custo de inferência.
- Resolve: ausência de baseline para fontes, citações, ausência de evidência e isolamento.
- Verificação: 18 testes, 20/20 casos, quatro métricas em `1.0`, compilação e hook estrito passaram.
- Pasta: `handoffs/008-evaluation-baseline/` | Próxima ação: finalizar explicitamente a tarefa 008.

## 008 — Evaluation baseline verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: confirmar o baseline após execução completa da suíte, runner e validações estruturais.
- Impactos: implementação encerrada e `CURRENT.md` avançado para `009`; runtime permanece sem alteração.
- Resolve: critério da etapa 008 confirmado com dataset e métricas determinísticas reproduzíveis.
- Verificação: 18 testes, 20/20 casos, quatro métricas em `1.0`, compilação, diff limpo e hook estrito.
- Pasta: `handoffs/008-evaluation-baseline/`.
