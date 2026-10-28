# 026/v18 — Relatório estruturado para observabilidade

- Versão: `v18`; versão-base: `026/v17` aplicada; data: 2026-10-27 -03:00; status: `verified`.
- Estado-base: o evaluator imprimia métricas e casos em JSON, mas sem separar resumo, scores, falhas, entrada, esperado e retrieval.
- Escopo autorizado: estruturar a saída para uso humano e futura integração com Langfuse, sem enviar dados ao Langfuse nesta rodada.
- Invariantes: métricas e cálculos permanecem iguais; o evaluator continua independente de vendor; `expected_answer` continua no golden.
- Arquivos reais alterados: `rastro-ai/evals/retrieval/report.py`, `rastro-ai/evals/retrieval/evaluate.py`, `rastro-ai/evals/retrieval/README.md` e `rastro-ai/tests/test_retrieval_evaluation.py`.

## O que foi feito

- Criado `build_report()` com contrato `rastro-ai.retrieval-report.v1`.
- Organizados `run`, `summary`, `scores`, `quality`, `failures` e `cases`.
- Adicionados scores com `name`, `value` e `data_type`, além de razões determinísticas por falha.
- Mantido o envio ao Langfuse fora do escopo.

## O que muda na aplicação

- O JSON continua detalhado, mas passa a ser separável em resumo, scores e investigação por caso.
- Cada caso carrega `input`, `expected`, `retrieval`, `scores` e `diagnostics`.
- A saída já pode ser adaptada futuramente para traces, observations e scores do Langfuse sem alterar as métricas.
- `quality.status` fica `not_evaluated` até thresholds serem configurados.

## Jornada da aplicação nesta versão

`run_evaluation()` calcula as métricas; `build_report()` transforma o resultado em um contrato de relatório; o CLI imprime o contrato e não faz chamadas externas de observabilidade.

## Como usar e validar a aplicação nesta versão

Execute `./run_evaluation.sh real` para produzir o relatório estruturado ou `./run_evaluation.sh test` para verificar o contrato sem banco e sem OpenAI.

## Cobertura por comportamento

- Resumo: contagens e métricas agregadas ficam em `summary`.
- Scores: métricas possuem nome, valor e tipo numérico.
- Diagnóstico: falhas possuem caso, razões, esperado e retornado.
- Futuro Langfuse: `run`, `cases` e `scores` são independentes do SDK.

## Instruções de validação

- `./run_evaluation.sh test`: esperado, 6 testes e `OK`.
- `bash -n run_evaluation.sh rastro-ai/evals/retrieval/run_evaluation.sh`: esperado, sintaxe válida.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml config --quiet`: esperado, Compose válido.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- Inspecionar o JSON do modo real: esperado, chaves `schema`, `run`, `summary`, `scores`, `quality`, `failures` e `cases`.
- Validação real do evaluator: executada pelo usuário no banco de evaluation; resultado observado com `case_count=20`, `Recall@5=0.85`, `MRR=0.877451`, `project_isolation=1.0`, `score_ordering=1.0` e `abstention=0.0`.
- Validação Langfuse: não aplicada; esta versão somente prepara o contrato e não envia dados externos.
- Integração Langfuse: indisponível nesta versão; nenhum SDK, trace ou score é enviado.
- Evidência unitária: o teste do contrato verifica schema, falha, score numérico e resposta esperada.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com todos os README/TIMELINE da implementação 026: esperado, todos os handoffs válidos.
