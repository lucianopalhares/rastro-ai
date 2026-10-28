# 026/v3 — Organização do golden dataset

- Versão: `v3`; versão-base: `026/v2` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: o golden estava em `rastro-ai/evals/retrieval/dataset.json`, junto do código do evaluator.
- Escopo autorizado: mover o arquivo para `rastro-ai/evals/retrieval/dataset/golden.json` e atualizar somente referências do loader e uso atual.
- Invariantes: contrato JSON, IDs `document_id:index`, métricas, runtime e resultados da v2 permanecem inalterados.
- Arquivos reais conferidos: `evaluate.py`, dataset, testes, README/timeline da 026 e controles da implementação.

## O que foi feito

- Criada a pasta `evals/retrieval/dataset/` e movido o golden para `golden.json`.
- O caminho padrão de `load_dataset()` e do CLI passou a apontar para essa pasta; o argumento `--dataset` continua permitindo substituição.

## O que muda na aplicação

- A organização separa código de evaluation e dados anotados, facilitando adicionar novos goldens sem misturar implementação e dataset.
- O comando sem `--dataset` continua usando o arquivo padrão; o runtime de busca e as métricas não mudam.
- Fora do escopo: novo corpus, alteração do schema JSON, DeepEval e integração PGVector.

## Jornada da aplicação nesta versão

Antes, o golden ficava na raiz do pacote de retrieval. Agora, os datasets ficam em uma pasta própria e o evaluator resolve esse caminho automaticamente, preservando a execução existente.

## Como usar e validar a aplicação nesta versão

Execute o evaluator sem `--dataset` para usar `evals/retrieval/dataset/golden.json`, ou informe outro arquivo com `--dataset`. A integração PGVector continua manual e depende de corpus e credenciais configurados.

## Cobertura por comportamento

- Resolução do caminho padrão: `tests/test_retrieval_evaluation.py`, que carrega o dataset sem argumento.
- Preservação do schema: o teste confirma os cinco casos e os casos de isolamento/ausência.
- Integração PGVector: não se aplica à mudança estrutural do dataset; permanece documentada nas versões anteriores.

## Instruções de validação

- `PYTHONPATH=src:. python3 -m unittest -q tests.test_retrieval_evaluation`: esperado, 4 testes aprovados e golden carregado da pasta `dataset`.
- `PYTHONPATH=src:. python3 -m evals.retrieval.evaluate --ks 1,3,5`: esperado, o CLI resolve `evals/retrieval/dataset/golden.json` como padrão quando o ambiente PGVector está configurado.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md`: esperado, oito handoffs válidos.
