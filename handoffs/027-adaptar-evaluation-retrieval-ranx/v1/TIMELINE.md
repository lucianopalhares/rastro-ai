# Timeline — 027/v1 integração das métricas com ranx

## 2026-10-27 00:00 -03:00 — proposta e aplicação inicial

- Status: `proposed`.
- Arquivos reais conferidos: evaluator, métricas, testes, `pyproject.toml` e Dockerfiles.
- Decisão: usar `ranx` somente para Recall, Precision, MRR e nDCG; preservar regras próprias.
- Pendências: executar testes no container e confirmar equivalência dos valores controlados.

## 2026-10-27 21:30 -03:00 — aplicação da integração ranx

- Status: `applied`.
- Mudanças: dependência e Dockerfiles atualizados; adapter Qrels/Run criado; ranking clássico delegado ao ranx; README do evaluator atualizado.
- Verificação: compilação Python e `git diff --check` aprovados; suíte controlada ainda precisa ser registrada como evidência final.
- Pendência: executar hook estrutural e confirmar validação final da versão.

## 2026-10-27 22:00 -03:00 — evidência da v1

- Status: `applied`.
- Evidências: `docker compose ... build ai-indexer`, `./rastro-ai/evals/retrieval/run_evaluation.sh test`, `bash -n`, `compileall`, `git diff --check` e `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh`.
- Resultado: imagem construída com `ranx 0.3.21`; 6 testes terminaram com `OK`; hook validou 4 arquivos.
- Limite: avaliação real contra PGVector não foi executada nesta rodada; a inicialização JIT do Numba tornou a suíte controlada mais lenta.
