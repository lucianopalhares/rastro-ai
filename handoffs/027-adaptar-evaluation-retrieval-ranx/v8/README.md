# 027/v8 — Modos de saída e seleção de métricas

- Versão-base: `v7` aplicada; script CLI, evaluator, report, testes e READMEs foram conferidos.
- Estado encontrado: o JSON completo era adequado para auditoria, mas grande para leitura rápida e não permitia selecionar métricas.
- Escopo autorizado: adicionar `--summary`, `--only-failures` e `--metrics`, documentando comandos e fluxo sem remover o relatório completo.
- Invariante: filtros controlam apresentação; as invariantes continuam executadas para não esconder segurança, ordenação ou abstention.

## O que foi feito

O script `rastro-ai/evals/retrieval/run_evaluation.sh` e o CLI `evals.retrieval.evaluate` agora aceitam modos de saída e seleção por grupo ou nome. `build_report` preserva o modo completo, gera resumo agregado ou mantém somente casos falhos. Foram documentados os grupos `ranking`, `invariants` e `operational`.

## O que muda na aplicação

O comando completo permanece compatível. `--summary` remove os casos detalhados, `--only-failures` mantém somente falhas e `--metrics` filtra scores agregados e por caso. `--summary` e `--only-failures` não podem ser usados juntos. As invariantes continuam sendo calculadas internamente em qualquer seleção.

## Jornada da aplicação nesta versão

Antes, toda execução imprimia o relatório completo; agora a pessoa escolhe entre visão executiva, investigação de falhas ou auditoria detalhada. O mesmo resultado calculado pode ser filtrado para terminal ou futura publicação no Langfuse.

## Como usar e validar a aplicação nesta versão

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh real --summary
./rastro-ai/evals/retrieval/run_evaluation.sh real --only-failures
./rastro-ai/evals/retrieval/run_evaluation.sh real --summary --metrics ranking
./rastro-ai/evals/retrieval/run_evaluation.sh real --summary --metrics recall@3,precision@3,ndcg@3
```

Use o modo completo sem esses filtros para auditoria. `ranking` reúne HitRate, Recall, Precision, MRR e nDCG; `invariants` reúne isolamento, score ordering e abstention; `operational` reúne latência, erros e resultados vazios.

## Cobertura por comportamento

- Saída resumida e falhas: `rastro-ai/evals/retrieval/report.py` e `rastro-ai/tests/test_retrieval_evaluation.py`; evidência unitária e de contrato: 8 testes e `OK`.
- Seleção de métricas: `build_report` aceita grupos, nomes com `@` e nomes normalizados; esperado: scores selecionados sem alterar o cálculo padrão.
- CLI: `rastro-ai/evals/retrieval/run_evaluation.sh` e `evaluate.py`; evidência de contrato: `bash -n`, `--help` e testes do report.
- Segurança: invariantes continuam executadas internamente; esperado: filtros não ocultam falhas de isolamento, score ou abstention nos diagnósticos.
- Integração real/smoke manual: não aplicada; o PGVector real e a futura publicação no Langfuse permanecem fora desta rodada.

## Instruções de validação

```bash
bash -n rastro-ai/evals/retrieval/run_evaluation.sh
python3 -m compileall -q rastro-ai/evals/retrieval rastro-ai/tests
git diff --check
./rastro-ai/evals/retrieval/run_evaluation.sh --help
```

Resultado esperado: script válido, compilação e diff sem erros, e ajuda exibindo os novos parâmetros.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: 8 testes e `OK`.
