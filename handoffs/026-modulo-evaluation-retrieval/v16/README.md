# 026/v16 — Script dos modos de evaluation

- Versão: `v16`; versão-base: `026/v15` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: os comandos Docker de teste e evaluation real eram longos e precisavam ser copiados manualmente.
- Escopo autorizado: criar um script shell executável e documentar os modos `test` e `real`; não alterar métricas nem o runtime.
- Invariantes: `test` não usa banco ou OpenAI; `real` usa `evaluation-vector-db`; `--prepare` é opcional e explícito.
- Arquivos reais alterados: `rastro-ai/evals/retrieval/run_evaluation.sh` e `rastro-ai/evals/retrieval/README.md`.

## O que foi feito

- Criado script com os modos `test` e `real`.
- Adicionado `--prepare` para reindexar o golden somente quando solicitado.
- Adicionado `--ks` para configurar os valores de ranking sem editar o comando Docker.
- Documentado o uso curto e a diferença entre os dois modos.

## O que muda na aplicação

- O usuário não precisa mais copiar os comandos extensos do Compose.
- O modo automatizado executa os 5 testes de retrieval sem infraestrutura externa.
- O modo real sobe/aguarda o banco de evaluation e consulta o retriever PGVector; com `--prepare`, também alimenta o banco.
- Não há mudança no cálculo das métricas ou no runtime do serviço.

## Jornada da aplicação nesta versão

`run_evaluation.sh test` executa o unittest em container temporário; `run_evaluation.sh real` aguarda `evaluation-vector-db`, monta o evaluator e executa o retrieval real; `real --prepare` executa o seeder antes da consulta.

## Como usar e validar a aplicação nesta versão

Use `./rastro-ai/evals/retrieval/run_evaluation.sh test` para validação rápida e `./rastro-ai/evals/retrieval/run_evaluation.sh real` para consultar o banco isolado já preparado.

## Cobertura por comportamento

- Teste automatizado: comando Docker curto, sem PostgreSQL, OpenAI ou corpus real.
- Evaluation real: banco, dataset e retriever configurados pelo script.
- Preparação opcional: embeddings só são gerados com `real --prepare`.
- Configuração: `--ks` altera os valores de k sem duplicar comandos.

## Instruções de validação

- `bash -n rastro-ai/evals/retrieval/run_evaluation.sh`: esperado, sintaxe válida.
- `./rastro-ai/evals/retrieval/run_evaluation.sh --help`: esperado, mostrar os modos `test` e `real`.
- `./rastro-ai/evals/retrieval/run_evaluation.sh test`: esperado, 5 testes e `OK`.
- Evidência unitária: o modo `test` executou os 5 testes de `tests.test_retrieval_evaluation` e terminou com `OK`.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml config --quiet`: esperado, Compose válido.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- Evaluation real: `./rastro-ai/evals/retrieval/run_evaluation.sh real`; depende de `evaluation-vector-db`, corpus preparado e `OPENAI_API_KEY`, e deve imprimir JSON.
- Validação integrada/manual: não executada nesta rodada; o modo real chama embeddings externos e pode gerar custo.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com todos os README/TIMELINE da implementação 026: esperado, todos os handoffs válidos.
