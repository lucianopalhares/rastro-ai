# Linha do tempo das implementações

Cada registro tem no máximo 8 linhas; detalhes técnicos ficam na pasta numerada correspondente.

## 013 — Configurar debug do Python e da API no VS Code

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: raiz (`.vscode`) e API (`rastro-api/package.json`), com debug do serviço `rastro-ai`.
- Por que foi feito: permitir breakpoints simultâneos no fluxo API → indexador Python.
- Impactos: adiciona perfil composto local e script NestJS de debug; produção e Compose permanecem inalterados.
- Resolve: inicialização manual separada dos processos durante diagnóstico.
- Pasta: `handoffs/013-configurar-debug-python-api-vscode/`

## 013 — Finalização da configuração de debug

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: raiz, API NestJS e serviço Python.
- Por que foi feito: consolidar breakpoints Docker e o fluxo reproduzível API → Python.
- Impactos: adiciona debugpy/inspector, documentação e requests de validação; runtime funcional preservado.
- Resolve: diagnóstico integrado dos dois processos; build Docker, health checks e smoke de upload/indexação aprovados.
- Pasta: `handoffs/013-configurar-debug-python-api-vscode/`

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

## 011 — Persistência vetorial com pgvector

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: raiz e IA (`docker-compose.yml`, schema e `rastro-ai`)
- Por que foi feito: substituir o índice lexical efêmero por persistência vetorial compatível com Supabase.
- Impactos: adiciona PostgreSQL/pgvector com volume, embeddings locais e backend semântico configurável.
- Resolve: upsert, consulta cosine, isolamento por projeto e testes do adapter; upload automático permanece fora do escopo.
- Pasta: `handoffs/011-persistencia-vetorial-pgvector/`

## 011 — Persistência vetorial com pgvector verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: raiz e IA (`docker-compose.yml`, schema e `rastro-ai`)
- Por que foi feito: confirmar o backend persistente com banco e adapter reais, além da suíte local.
- Impactos: implementação encerrada; `CURRENT.md` avança para `009`, mantida em standby.
- Resolve: extensão, tabela, índices, upsert, consulta semântica e isolamento por projeto validados.
- Verificação: container saudável, 21 testes, compilação, Compose, diff, hook e smoke real aprovados.
- Pasta: `handoffs/011-persistencia-vetorial-pgvector/`

## 012 — Integrar upload da API à indexação Python

- Data/hora: 2026-10-24 -03:00 | Status: `applied`
- Aplicação afetada: API `rastro-api`, IA `rastro-ai` e raiz compartilhada se o transporte exigir.
- Por que foi feita: registrar a próxima capacidade para que um arquivo enviado pela API seja indexado pela aplicação Python.
- Impactos: API envia documentos ao serviço Python e persiste `ready`/`failed`; retry e idempotência automática não foram incluídos.
- Resolve: conecta o upload `pending` à extração, chunking e persistência dos chunks.
- Pasta: `handoffs/012-integrar-upload-indexacao-python/`

## 012 — Integrar upload da API à indexação Python verificada

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: API `rastro-api`, IA `rastro-ai` e raiz compartilhada.
- Por que foi feita: confirmar ponta a ponta o upload, chunking, embeddings externos e persistência vetorial.
- Impactos: documento curto gerou 1 chunk e documento longo gerou 3 chunks; ambos ficaram `ready` com embeddings de dimensão `384` no PostgreSQL.
- Resolve: critério da integração confirmado com testes, compilação, build, Compose, smoke HTTP real e validação estrutural.
- Verificação: API com 10 testes e build; Python com 26 testes, `compileall` e imports modulares; imagem Docker, Compose, banco e hook estrito aprovados.
- Pendências: retry, idempotência explícita, processamento assíncrono e remoção dos wrappers legados.
- Pasta: `handoffs/012-integrar-upload-indexacao-python/` | Próxima ação: aguardar nova autorização explícita.

## 014 — Exigir pgvector no runtime

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: impedir fallback lexical silencioso quando o fluxo esperado usa embeddings e pgvector.
- Impactos: exige backend persistente no runtime e mantém memória somente para testes explícitos.
- Resolve: divergência entre busca semântica declarada e `InMemoryVectorStore` selecionado sem configuração.
- Verificação: 28 testes, compilação, Compose, containers saudáveis e hook passaram; smoke PostgreSQL/pgvector pendente por ausência de chave OpenAI.
- Pasta: `handoffs/014-exigir-pgvector-no-runtime/` | Próxima ação: executar validação completa e promover para `verified`.

## 014 — Finalização com verificação pendente

- Data/hora: 2026-10-25 -03:00 | Status mantido: `applied`.
- Aplicação afetada: IA (`rastro-ai`).
- Verificação: 28 testes, compilação, Compose, containers saudáveis e hook estrito aprovados.
- Pendência: smoke HTTP com OpenAI/pgvector não executado por ausência de `OPENAI_API_KEY`.
- Commit: não gerado enquanto a verificação externa permanecer pendente.
- Pasta: `handoffs/014-exigir-pgvector-no-runtime/` | Próxima ação: executar smoke e promover para `verified`.

## 014 — Verificação do fluxo persistente concluída

- Data/hora: 2026-10-25 10:18 -03:00 | Status: `verified`.
- Aplicação afetada: API `rastro-api`, IA `rastro-ai` e PostgreSQL/pgvector.
- Verificação: upload API `ready`, endpoint Python `backend: postgres`, chunk persistido com embedding `384`, 28 testes, Compose e hook aprovados.
- Resolve: confirma no fluxo real que o runtime usa embeddings e pgvector, sem fallback lexical.
- Pendências: nenhuma dentro do escopo; retry e processamento assíncrono permanecem fora do escopo.
- Pasta: `handoffs/014-exigir-pgvector-no-runtime/` | Próxima ação: gerar commit explícito da tarefa.

## 014 — Commit criado

- Data/hora: 2026-10-25 10:18 -03:00 | Status: `verified`.
- Commit: `52e1820` — `Exigir pgvector no runtime`.
- Verificação: smoke API/Python/pgvector, 28 testes, compilação, Compose e hook estrutural aprovados.
- Pasta: `handoffs/014-exigir-pgvector-no-runtime/` | Próxima ação: nenhuma.

## 015 — Adaptar chunking para LangChain

- Data/hora: 2026-10-25 -03:00 | Status: `proposed`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: preparar a substituição do chunker próprio por adaptador LangChain sem acoplar o domínio à biblioteca.
- Impactos: nenhum no runtime nesta rodada; preservação de offsets, tokens, projeto e baseline é requisito da implementação.
- Resolve: registra a próxima capacidade após a verificação do pgvector.
- Verificação: prevista com testes de chunking/indexação, evaluation, compilação, smoke e hook estrutural.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: reconciliar arquivos reais e implementar `v1`.

## 015 — Adaptador LangChain aplicado

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: desacoplar o caso de uso da implementação concreta de chunking.
- Impactos: LangChain entra somente na infraestrutura; contratos, offsets, projeto e fachada legada são preservados.
- Resolve: injeta `TextChunker`, converte documentos LangChain em `DocumentChunk` e cobre offsets sobrepostos.
- Verificação: 30 testes, evaluation `20/20` e compilação aprovados; hook final e smoke externo pendentes.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: solicitar finalização.

## 015 — Dependência Docker corrigida

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`) e imagens Docker de desenvolvimento/produção.
- Por que foi feita: o container não instalava `langchain-text-splitters`, embora o runtime já o importasse.
- Impactos: rebuild das imagens passa a incluir a dependência necessária ao adaptador LangChain.
- Resolve: `ModuleNotFoundError` durante a inicialização do `ai-indexer`.
- Verificação: build sem cache, import no container, serviço saudável via Compose, 30 testes, evaluation 20/20, compilação e hook aprovados.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: solicitar finalização e gerar commit explícito.

## 015 — Implementação finalizada e verificada

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`), schema PostgreSQL/pgvector e documentação arquitetural.
- Por que foi feita: consolidar chunking, embeddings e PGVector com LangChain e remover o schema vetorial legado não utilizado.
- Impactos: novos chunks usam as tabelas `langchain_pg_*`; a tabela local antiga e seus 27 registros foram removidos sem migração.
- Resolve: fluxo documentado, provider/vector store integrados, schema inicial simplificado e metadados preservados nas tabelas LangChain.
- Verificação: consultas PostgreSQL, compilação, hook estrutural e validações do Compose concluídos; pytest não disponível na imagem.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: nenhuma.

## 015 — Commit criado

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Commit: `73bbec1` — `Consolidar fluxo LangChain de indexação`.
- Verificação: lista explícita da implementação commitada; alterações não relacionadas permaneceram fora do índice.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: nenhuma.

## 015 — Vector store PGVector adaptado ao LangChain

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`), PostgreSQL/pgvector e imagens Docker.
- Por que foi feita: completar a adoção de LangChain no fluxo de chunks, embeddings e busca vetorial.
- Impactos: a persistência passa a usar coleção/tabelas do `langchain-postgres`; tabela legada permanece e dados existentes não são migrados automaticamente.
- Resolve: adiciona adapter com IDs estáveis, metadata de citações, filtro obrigatório por projeto e conversão de score.
- Verificação: 31 testes, evaluation `20/20`, compilação, build Docker, upsert/busca reais do PGVector no Compose e hook aprovados.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: reindexar dados, smoke com credencial e finalizar.

## 015 — Preparação para reranking, chains, prompts e LangGraph

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`) e imagens Docker.
- Por que foi feita: preparar o fluxo futuro de RAG generativo sem ativar chamadas externas prematuramente.
- Impactos: adiciona portas, adapters e workflow opcional; o runtime atual continua extrativo e determinístico.
- Resolve: separa retrieval, reranking, geração estruturada, citações e orquestração futura.
- Verificação: 35 testes, evaluation `20/20`, compilação, build Docker, import no container e hook aprovados.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: escolher provider, ativar grafo e finalizar.

## 015 — Embeddings integrados ao LangChain

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`) e imagens Docker.
- Por que foi feita: adotar a interface de embeddings usada no ecossistema LangChain mantendo as regras próprias da Rastro.
- Impactos: transporte, batching e retries passam pelo `OpenAIEmbeddings`; dimensão, porta, pgvector e contratos locais permanecem controlados.
- Resolve: substitui o cliente HTTP manual por adapter LangChain testável e compatível com futuros provedores.
- Verificação: 31 testes, evaluation `20/20`, compilação, build Docker, import no container e hook aprovados; chamada externa pendente por credencial.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: solicitar finalização e smoke com credencial.

## 015 — Fachada de chunking unificada

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: eliminar a divergência entre `chunk_text` público e o fluxo `index_document`.
- Impactos: ambos usam `LangChainTextChunker`; a entidade `DocumentChunk`, offsets e metadados permanecem preservados.
- Resolve: uma única estratégia de chunking nos caminhos públicos, com teste dedicado.
- Verificação: 31 testes, evaluation `20/20` e compilação aprovados; hook estrutural válido.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: solicitar finalização e gerar commit explícito.

## 016 — Composition root do serviço Python

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: preparar a evolução para orquestração e evaluation sem criar infraestrutura durante imports.
- Impactos: containers explícitos para indexação e retrieval; API pública e contratos atuais preservados.
- Resolve: remove instâncias globais das fachadas e move a validação do backend para a composição do runtime.
- Verificação: unittest, evaluation, compilação, importação segura e hook estrutural registrados na versão `016/v1`.
- Pasta: `handoffs/016-reorganizar-arquitetura-python/` | Próxima ação: finalizar `016` antes de ativar `017`.

## 016 — Composition root verificado

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`).
- Verificação: 36 testes, evaluation `20/20`, importação segura sem backend, compilação, `git diff --check` e hook estrutural aprovados.
- Pendências: namespaces, workflows e evaluation permanecem planejados e não foram aplicados nesta etapa.
- Pasta: `handoffs/016-reorganizar-arquitetura-python/` | Próxima ação: executar `skill finalizar tarefa 016` para encerrar e criar o commit explícito.

## 016 — Duplicações removidas e verificado

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`).
- Por que foi feita: eliminar aliases sem consumidores internos e provider de embeddings não utilizado.
- Impactos: namespaces antigos deixam de ser importáveis; fachadas públicas e `document_indexing` permanecem como caminhos suportados.
- Resolve: reduz caminhos duplicados para entidades, casos de uso, adapters e chunking.
- Verificação: 36 testes, evaluation `20/20`, compilação e busca de referências residuais aprovados.
- Pasta: `handoffs/016-reorganizar-arquitetura-python/` | Próxima ação: confirmar consumidores externos e finalizar `016`.

## 016 — Finalizada

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`).
- Verificação: testes, evaluation `20/20`, compilação, imports canônicos, rejeição dos aliases removidos, hook e `git diff --check` aprovados.
- Commit: `ceb639e` — `Reorganizar arquitetura do serviço Python`.
- Próxima ação: `017-consolidar-namespaces-python`; `CURRENT.md` avançado para `017`.
- Pasta: `handoffs/016-reorganizar-arquitetura-python/`.

## 017 — Renomear fluxo de extração e chunking

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`) e documentação arquitetural.
- Por que foi feita: distinguir geração de chunks da persistência vetorial nos nomes do código.
- Impactos: fachadas, caso de uso, serviço, exports, testes e documentos usam `extract_and_chunk_document` e `index_document_chunks`.
- Resolve: elimina a ambiguidade de `index_document()` e `index_document_in_store()` sem alterar o runtime funcional.
- Verificação: testes, evaluation, compilação, busca de referências e hook estrutural registrados na versão `017/v1`.
- Pasta: `handoffs/017-renomear-fluxo-extracao-chunking/` | Próxima ação: verificar e finalizar `017`.

## 017 — Nomenclatura semântica verificada

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`) e documentação arquitetural.
- Verificação: 36 testes, evaluation `20/20`, compilação, imports semânticos, ausência de referências ativas antigas e hook estrutural aprovados.
- Pendências: imports externos dos nomes antigos precisam migrar; smoke externo não foi repetido nesta rodada.
- Pasta: `handoffs/017-renomear-fluxo-extracao-chunking/` | Próxima ação: finalizar `017` antes de ativar `018`.

## 017 — Renomeação verificada

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Aplicação afetada: IA (`rastro-ai`) e documentação arquitetural.
- Verificação: 36 testes, evaluation `20/20`, compilação, imports novos, ausência de referências antigas e hook estrutural aprovados.
- Pendências: consumidores externos dos nomes antigos precisam migrar; nenhuma alteração externa foi executada.
- Pasta: `handoffs/017-renomear-fluxo-extracao-chunking/` | Próxima ação: finalizar `017` antes de ativar `018`.

## 017 — Nomenclatura semântica aplicada

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Aplicação afetada: IA (`rastro-ai`) e documentação arquitetural.
- Por que foi feita: tornar explícitas as responsabilidades de persistência, busca, containers, stores e adapters.
- Impactos: nomes internos e exports mudaram; contrato HTTP, embeddings, PGVector e evaluation permanecem iguais.
- Resolve: elimina a ambiguidade de `retrieval.index_chunks()` e dos nomes genéricos de vector stores.
- Verificação: testes, evaluation, compilação, busca de referências e hook estrutural registrados em `017/v2`.
- Pasta: `handoffs/017-renomear-fluxo-extracao-chunking/` | Próxima ação: verificar e finalizar `017`.
- Commit: `acf2c2b` — `Esclarecer nomes do fluxo de chunks e retrieval`.
- Verificação: commit criado com lista explícita dos arquivos da implementação.

## 021 — Revisar fluxo e comentários dos handoffs

- Data/hora: 2026-10-26 -03:00 | Status: `applied`
- Aplicação afetada: raiz (`AGENTS.md`, `docs/instruction.md` e `.agents/skills/implementation-flow/`).
- Por que foi feita: explicar decisões importantes em linguagem simples e preservar rastreabilidade sem aumentar ruído.
- Impactos: comentários usam histórico `NNN-vN`; versões registram estado-base, escopo, invariantes, mudança e evidência.
- Resolve: ambiguidade sobre comentários obrigatórios e falta de contrato mínimo para cada rodada.
- Pasta: `handoffs/021-revisar-fluxo-e-comentarios-handoffs/`

## 021 — Revisar fluxo e comentários dos handoffs — finalização

- Data/hora: 2026-10-26 -03:00 | Status: `verified`
- Aplicação afetada: raiz (`AGENTS.md`, `docs/instruction.md` e `.agents/skills/implementation-flow/`).
- Verificação: hook estrutural com cobertura comportamental aprovado; alterações locais de Python excluídas por não pertencerem à tarefa.
- Resultado: governança conferida e tarefa encerrada; não há próxima etapa ativa nesta iniciativa.
- Pasta: `handoffs/021-revisar-fluxo-e-comentarios-handoffs/`
