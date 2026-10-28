# Timeline — 026 módulo de evaluation de retrieval

## 2026-10-27 -03:00 — abertura

- Status: `proposed`.
- Dependência: implementação 025 verificada; runtime de busca semântica existente em `PostgresChunkVectorStore`.
- Decisão: separar métricas determinísticas de ranking do DeepEval e reutilizar a fachada pública somente no comando integrado.
- Escopo: evaluator injetável, golden dataset com casos diretos, paráfrase, múltiplas evidências, ausência e isolamento.
- Pendência: executar testes e confirmar a avaliação contra PostgreSQL/PGVector com corpus cujos IDs estejam no dataset.

## 2026-10-27 -03:00 — aplicação v1

- Status: `applied`.
- Evidência: 3 testes específicos, 44 testes Python no container e hook estrutural passaram.
- Mudanças: evaluator, golden dataset, métricas de ranking e testes sem rede aplicados; runtime não foi alterado.
- Pendência: executar o comando integrado com PostgreSQL/PGVector, documentos indexados e credenciais configuradas.
- Controle: `CURRENT.md` permanece em `026`; não marcar `verified` nem gerar commit final enquanto a integração real não for executada.

## 2026-10-27 -03:00 — aplicação v2

- Status: `applied`.
- Versão-base: `v1` aplicada; os arquivos reais foram relidos e a mudança ficou restrita ao módulo de evaluation e seus testes.
- Mudanças: Recall@k, Precision@k, MRR, nDCG, isolamento, score e abstinência foram separados em módulos puros.
- Evidência: 4 testes específicos, 45 testes Python no container, hook estrutural e diff limpo.
- Pendência: integração PGVector real com corpus anotado ainda não executada.

## 2026-10-27 -03:00 — aplicação v3

- Status: `applied`.
- Versão-base: `v2` aplicada; referências atuais foram conferidas antes da mudança.
- Mudanças: golden movido para `rastro-ai/evals/retrieval/dataset/golden.json`; caminho padrão do loader atualizado.
- Evidência: schema e contrato dos cinco casos preservados; testes e hook devem ser repetidos com os oito handoffs.
- Pendência: integração PGVector real da implementação 026 continua não executada.

## 2026-10-27 -03:00 — aplicação v5

- Status: `applied`.
- Versão-base: `v4` aplicada; os dois datasets, runners e testes foram reconciliados.
- Mudanças: golden único em `rastro-ai/evals/dataset/golden.json`; baseline e retrieval compartilham o schema; duplicações removidas.
- Evidência: 45 testes no container, baseline 20/20 e hook estrutural aprovados.
- Pendência: integração PGVector real da implementação 026 continua não executada.

## 2026-10-27 -03:00 — aplicação v6

- Status: `applied`.
- Versão-base: `v5` aplicada; comandos, runners e golden único foram conferidos.
- Mudanças: diferença entre testes automatizados e fluxo real documentada no módulo e no índice de evaluations.
- Evidência: documentação adicionada; testes e hook serão repetidos.
- Pendência: avaliação real contra PGVector permanece não executada.

## 2026-10-27 -03:00 — aplicação v8

- Status: `applied`.
- Versão-base: `v7` aplicada; README e comandos atuais foram conferidos.
- Mudanças: seção de validação passou a explicar cada comando, seus pré-requisitos e o resultado esperado.
- Evidência: documentação atualizada; teste automatizado e hook serão repetidos.
- Pendência: avaliação PGVector real continua não executada.

## 2026-10-27 -03:00 — aplicação v9

- Status: `applied`.
- Versão-base: `v8` aplicada; README e comando real foram conferidos.
- Mudanças: árvore textual adicionada para explicar Docker, evaluator, PGVector, chunks e métricas.
- Evidência: alteração documental; teste automatizado e hook serão repetidos.
- Pendência: fluxo real contra PGVector continua não executado.

## 2026-10-27 -03:00 — aplicação v12

- Status: `applied`.
- Versão-base: `v11` aplicada; comando normal, Compose, Dockerfile e configuração de attach foram conferidos.
- Mudanças: execução com `debugpy`, `--wait-for-client`, porta 5678 e mapeamento de `/app/evals` documentados.
- Evidência: documentação atualizada; testes automatizados e hook estrutural serão repetidos.
- Pendência: attach interativo do VS Code e avaliação PGVector real continuam dependentes de execução manual.

## 2026-10-27 -03:00 — aplicação v13

- Status: `applied`.
- Versão-base: `v12` aplicada; configuração de attach e documentação foram conferidas.
- Mudanças: VS Code configurado para a porta 5679 e para mapear `/app/evals`.
- Evidência: configuração local atualizada; testes e hook estrutural serão repetidos.
- Pendência: attach interativo e evaluation PGVector real continuam pendentes.

## 2026-10-27 -03:00 — aplicação v14

- Status: `applied`.
- Versão-base: `v13` aplicada; `run_evaluation()` e os métodos chamados foram conferidos.
- Mudanças: comentários simples adicionados imediatamente antes das chamadas internas do evaluator.
- Evidência: testes automatizados e hook estrutural serão executados nesta rodada.
- Pendência: validação interativa do breakpoint e evaluation PGVector real continuam pendentes.

## 2026-10-27 -03:00 — aplicação v15

- Status: `applied`.
- Versão-base: `v14` aplicada; golden, pipeline de chunking, Compose e retriever foram conferidos.
- Mudanças: preparador de corpus, container PostgreSQL/PGVector isolado, comandos com database dedicado e teste do contrato corpus/golden.
- Evidência: Compose válido, banco de evaluation saudável e 5 testes automatizados aprovados.
- Pendência: indexação integrada depende de `OPENAI_API_KEY`; evaluation PGVector e debug manual permanecem pendentes.

## 2026-10-27 -03:00 — aplicação v16

- Status: `applied`.
- Versão-base: `v15` aplicada; comandos Docker e modos de execução foram conferidos.
- Mudanças: script executável com modos `test`, `real`, `real --prepare` e opção `--ks`.
- Evidência: modo automatizado executado com 5 testes e `OK`; sintaxe shell será repetida.
- Pendência: execução real pelo script depende de credencial OpenAI e corpus preparado.

## 2026-10-27 -03:00 — aplicação v17

- Status: `applied`.
- Versão-base: `v16` aplicada; script original e caminhos da raiz foram conferidos.
- Mudanças: criado atalho `run_evaluation.sh` na raiz, encaminhando todos os argumentos ao script original.
- Evidência: sintaxe e modo automatizado serão executados nesta rodada.
- Pendência: modo real continua dependente de OpenAI e banco de evaluation.

## 2026-10-27 -03:00 — aplicação v18

- Status: `applied`.
- Versão-base: `v17` aplicada; saída do evaluator e consumidores de `EvaluationResult` foram conferidos.
- Mudanças: relatório estruturado com resumo, scores, qualidade, falhas e casos; nenhum envio ao Langfuse.
- Evidência: teste de contrato será executado junto dos testes do retrieval e do hook estrutural.
- Pendência: thresholds e integração de scores com Langfuse permanecem fora desta rodada.

## 2026-10-27 -03:00 — finalização da implementação 026

- Status: `verified`.
- Evidência: 47 testes Python, Compose válido, banco `evaluation-vector-db` saudável, 26 documentos compatíveis com o golden, 34 handoffs válidos e evaluation real executada.
- Resultado real: Recall@5 `0.85`, MRR `0.877451`, nDCG@5 `0.767099`, isolamento `1.0`, ordenação `1.0` e abstinência `0.0`.
- Limite conhecido: abstinência ainda falha nos casos sem evidência porque o retriever retorna candidatos sem threshold; isso não bloqueia a verificação estrutural da implementação.
- Controle: `CURRENT.md` atualizado para `idle`; próxima melhoria deve ser uma nova implementação.

## 2026-10-27 -03:00 — commit da implementação 026

- Commit: `d89f068` — `Implementa evaluation de retrieval`.
- Conteúdo: evaluator desacoplado, golden único, banco PGVector isolado, scripts, relatório estruturado e handoffs versionados.
- Verificação: 47 testes no container, script `test` com 6 testes e `OK`, Compose válido, `git diff --check` e 40 handoffs válidos.

## 2026-10-27 -03:00 — aplicação v10

- Status: `applied`.
- Versão-base: `v9` aplicada; cadeia real de retrieval e README foram conferidos.
- Mudanças: árvore passou a nomear métodos/classes e a explicar cada responsabilidade abaixo.
- Evidência: alteração documental; teste automatizado e hook serão repetidos.
- Pendência: fluxo real contra PGVector continua não executado.

## 2026-10-27 -03:00 — aplicação v7

- Status: `applied`.
- Versão-base: `v6` aplicada; Compose, Dockerfile e caminhos de execução foram conferidos.
- Mudanças: Docker passou a ser o caminho oficial dos testes e da avaliação real; host ficou como alternativa.
- Evidência: READMEs e instruções de validação atualizados; testes e hook serão repetidos.
- Pendência: avaliação PGVector real continua não executada.

## 2026-10-27 -03:00 — aplicação v4

- Status: `applied`.
- Versão-base: `v3` aplicada; código real conferido antes da mudança.
- Mudanças: comentários passaram a registrar responsabilidade e ordem do CLI, orquestrador e cada métrica.
- Evidência: nenhuma lógica ou saída foi alterada; testes e hook serão repetidos.
- Pendência: integração PGVector real da implementação 026 continua não executada.

## 2026-10-27 -03:00 — aplicação v8

- Status: `applied`.
- Versão-base: `v7` aplicada; documentação e comandos atuais foram conferidos.
- Mudanças: seção de validação passou a explicar cada comando, seus pré-requisitos e o resultado esperado.
- Evidência: documentação atualizada; teste automatizado e hook serão repetidos.
- Pendência: avaliação PGVector real continua não executada.

## 2026-10-27 -03:00 — aplicação v9

- Status: `applied`.
- Versão-base: `v8` aplicada; README e comando real foram conferidos.
- Mudanças: árvore textual adicionada para explicar Docker, evaluator, PGVector, chunks e métricas.
- Evidência: alteração documental; teste automatizado e hook serão repetidos.
- Pendência: fluxo real contra PGVector continua não executado.
