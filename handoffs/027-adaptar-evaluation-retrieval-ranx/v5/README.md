# 027/v5 — Organização explícita do fluxo de evaluation

- Versão-base: `v4` aplicada; `evaluate.py`, `report.py` e os testes reais foram conferidos.
- Estado encontrado: o fluxo funcionava, mas `run_evaluation` concentrava retrieval, invariantes, ranking e agregação em um único bloco.
- Escopo autorizado: separar responsabilidades internas e explicitar imports; preservar cálculos, nomes públicos e contrato do relatório.
- Invariante: `ranking_metrics` continua usando ranx; `invariants_metrics` continua independente e executada antes do ranking.

## O que foi feito

Em `rastro-ai/evals/retrieval/evaluate.py`, os imports agora apontam diretamente para `invariants_metrics` e `ranking_metrics`. O fluxo foi dividido em `_initialize_metric_totals`, `_evaluate_invariants`, `_evaluate_ranking_metrics` e `_aggregate_metrics`, com comentários em pt-BR explicando a ordem e a responsabilidade de cada etapa.

## O que muda na aplicação

O comportamento e o JSON permanecem compatíveis. A mudança é estrutural e de legibilidade: agora fica visível no código o caminho `retrieval → invariantes → ranking → agregação`. A alteração não muda o formato do relatório, não executa avaliação real contra PGVector e não reorganiza os arquivos de métricas.

## Jornada da aplicação nesta versão

Antes, uma única função misturava as quatro etapas; agora uma pessoa consegue ler cada etapa por uma função nomeada e entender por que ela existe. O resultado percebido é um fluxo mais fácil de manter e revisar, sem impacto no resultado calculado.

## Como usar e validar a aplicação nesta versão

Execute `./rastro-ai/evals/retrieval/run_evaluation.sh test`. O comando usa o retriever controlado, passa pelas invariantes e pelo ranx e deve terminar com 6 testes e `OK`. O comando real continua disponível em `./rastro-ai/evals/retrieval/run_evaluation.sh` quando houver PGVector configurado.

## Cobertura por comportamento

- Organização do fluxo: `rastro-ai/evals/retrieval/evaluate.py`; esperado: imports explícitos e helpers separados para invariantes, ranking e agregação.
- Compatibilidade do cálculo: `rastro-ai/tests/test_retrieval_evaluation.py`; esperado: 6 testes e `OK`, incluindo métricas de ranking e invariantes.
- Compatibilidade do relatório: `rastro-ai/evals/retrieval/report.py` foi conferido; o formato usado por `build_report` permanece inalterado.
- Integração real/smoke manual: não aplicada; o escopo preserva o acesso ao PGVector e altera somente a organização interna.

## Instruções de validação

```bash
python3 -m compileall -q rastro-ai/evals/retrieval rastro-ai/tests && git diff --check
```

Resultado esperado: compilação e diff sem erros.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: 6 testes e `OK`.
