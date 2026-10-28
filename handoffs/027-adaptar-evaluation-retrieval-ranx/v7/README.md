# 027/v7 — HitRate e indicadores operacionais do retrieval

- Versão-base: `v6` aplicada; `evaluate.py`, adapter ranx, report, testes e documentação foram conferidos.
- Estado encontrado: o ranking básico estava coberto, mas não informava sucesso mínimo por consulta nem latência, erro e resultado vazio.
- Escopo autorizado: adicionar `HitRate@k`, latência média/P95, taxa de erro e taxa de resultado vazio, preservando métricas existentes e relatório compatível.
- Invariante: erro técnico não conta como abstention; lista vazia é tratada como zero no ranking quando havia evidência esperada.

## O que foi feito

Adicionado `hit_rate@k` ao adapter `ranx` e ao evaluator. O fluxo mede o tempo do retriever, agrega `retrieval_latency_ms`, `retrieval_latency_p95_ms`, `retrieval_error_rate` e `empty_result_rate`, e registra `retrieval_error` e `retrieval_latency_ms` por caso. O relatório marca erros técnicos como falhas. A documentação do retrieval e o fluxo em `docs/` foram atualizados.

## O que muda na aplicação

O JSON mantém as métricas antigas e recebe novos scores operacionais e `HitRate@k`. Falhas do retriever deixam de interromper silenciosamente a execução controlada: são registradas com o tipo da exceção, enquanto a busca vazia legítima permanece distinta de erro. O P95 é calculado sobre as latências das consultas executadas; não mede tempo de preparação do índice nem resposta do LLM.

## Jornada da aplicação nesta versão

Antes, a evaluation dizia principalmente se os chunks estavam relevantes; agora também informa se alguma evidência apareceu e se a busca foi rápida, estável ou vazia. A próxima evolução possível continua sendo diversidade, robustez ou MAP, somente se o projeto justificar.

## Como usar e validar a aplicação nesta versão

Execute `./rastro-ai/evals/retrieval/run_evaluation.sh test`. O resultado esperado é 7 testes e `OK`. Na saída do evaluator real, procure `hit_rate_at_1`, `retrieval_latency_ms`, `retrieval_latency_p95_ms`, `retrieval_error_rate` e `empty_result_rate` junto das métricas anteriores.

## Cobertura por comportamento

- HitRate: `rastro-ai/evals/retrieval/metrics/ranking_metrics/ranx_adapter.py` e `rastro-ai/tests/test_retrieval_evaluation.py`; evidência unitária e de contrato: suíte controlada; esperado: HitRate zero quando nenhum relevante aparece e um quando aparece no k.
- Operação: `rastro-ai/evals/retrieval/evaluate.py`; evidência de contrato: campos do `EvaluationResult` e teste controlado; esperado: latência média/P95 não negativa, erros e resultados vazios agregados separadamente.
- Falha técnica: `rastro-ai/evals/retrieval/report.py` e teste controlado; evidência de contrato: `retrieval_error` no caso; esperado: erro aparece como `retrieval_error`, não como abstention.
- Compatibilidade: suíte controlada; esperado: 7 testes e `OK`, com métricas anteriores preservadas.
- Integração real/smoke manual: não aplicada; PGVector real e thresholds de produção permanecem fora desta rodada.

## Instruções de validação

```bash
python3 -m compileall -q rastro-ai/evals/retrieval rastro-ai/tests && git diff --check
```

Resultado esperado: compilação e diff sem erros.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: 7 testes e `OK`. O primeiro uso pode emitir o aviso de compilação JIT do Numba usado pelo ranx.
