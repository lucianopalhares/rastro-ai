# Timeline — 027/v3 nomes explícitos para métricas e invariantes

## 2026-10-27 22:45 -03:00 — aplicação da v3

- Status: `applied`.
- Arquivos reais conferidos: diretórios de métricas, `metrics/__init__.py`, evaluator e README do retrieval.
- Mudanças: `ranking` renomeado para `ranking_metrics`; `invariants` renomeado para `invariants_metrics`; imports e documentação atualizados.
- Pendência: repetir compilação, suíte controlada e hook estrutural.

## 2026-10-27 23:00 -03:00 — evidência da v3

- Status: `applied`.
- Evidência: compilação Python, `git diff --check`, `./rastro-ai/evals/retrieval/run_evaluation.sh test` e hook estrutural concluídos.
- Resultado: 6 testes terminaram com `OK`; imports públicos e contrato do evaluator permaneceram compatíveis.
- Limite: evaluation real PGVector não executada; finalização e commit aguardam comando explícito.
