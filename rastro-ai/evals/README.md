# Evaluation do Rastro AI

`dataset.json` contém 20 casos anonimizados e pequenos, cobrindo respostas fundamentadas, múltiplas fontes, ausência, conflito, citações, isolamento e prompt injection em documentos.

O comando `PYTHONPATH=src python3 -m evals.evaluate` executa o dataset contra as fachadas reais e compara as métricas determinísticas com `baseline.json`.

Este baseline não mede faithfulness ou relevância semântica por LLM: a aplicação atual é lexical, extrativa e não possui DeepEval, modelo, prompt ou trace de custo.
