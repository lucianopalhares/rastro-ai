# 026/v14 — Comentários das chamadas do evaluator

- Versão: `v14`; versão-base: `026/v13` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: `run_evaluation()` tinha a finalidade documentada, mas suas chamadas internas não explicavam em linguagem simples o que cada etapa fazia.
- Escopo autorizado: adicionar comentários em `rastro-ai/evals/retrieval/evaluate.py`; não alterar cálculos, ordem ou contratos.
- Invariantes: a sequência da avaliação e os valores das métricas permanecem iguais; comentários ficam imediatamente antes das chamadas correspondentes.
- Arquivo real alterado: `rastro-ai/evals/retrieval/evaluate.py`.

## O que foi feito

- Comentadas as chamadas de busca, normalização, isolamento, ordenação de scores, MRR, abstinência, Recall@k, Precision@k, nDCG, média do MRR e montagem do resultado.
- Atualizado o histórico do bloco de `run_evaluation()` para registrar a rodada `026-v14`.

## O que muda na aplicação

- Não há mudança de runtime, cálculos, saída, dataset ou integração com PGVector.
- O fluxo interno de `run_evaluation()` fica legível diretamente no código para facilitar o acompanhamento durante o debug.

## Jornada da aplicação nesta versão

Para cada caso, o evaluator busca resultados, transforma seus IDs, valida isolamento e scores, calcula as métricas de ranking e depois agrega os valores antes de criar `EvaluationResult`.

## Como usar e validar a aplicação nesta versão

Abra `evaluate.py`, coloque breakpoints em `run_evaluation()` e execute o comando de debug já documentado; os comentários indicam a finalidade da próxima chamada.

## Cobertura por comportamento

- Fluxo do evaluator: comentários explicam cada chamada importante sem modificar a sequência.
- Métricas: Recall@k, Precision@k, MRR, nDCG, isolamento, score e abstinência continuam sendo calculados pelos mesmos métodos.
- Runtime: nenhuma alteração funcional.

## Instruções de validação

- Conferir `rastro-ai/evals/retrieval/evaluate.py`: esperado, cada chamada importante dentro de `run_evaluation()` possuir comentário simples imediatamente antes.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`.
- Evidência unitária: os 4 testes de `tests.test_retrieval_evaluation` devem terminar com `OK`; isso confirma que os comentários não alteraram o contrato das métricas.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- Validação manual integrada: não executada nesta rodada; o debug interativo continua dependendo do VS Code, PostgreSQL/PGVector, corpus e credenciais.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com todos os README/TIMELINE da implementação 026: esperado, todos os handoffs válidos.
