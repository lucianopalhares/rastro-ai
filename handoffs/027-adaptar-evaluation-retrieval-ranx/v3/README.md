# 027/v3 — Nomes explícitos para métricas e invariantes

- Versão-base: `v2` aplicada; código real conferido em `rastro-ai/evals/retrieval/metrics`, evaluator e README.
- Estado encontrado: os diretórios `ranking/` e `invariants/` separavam responsabilidades, mas `ranking` podia ser confundido com uma etapa de reranking do runtime.
- Escopo autorizado: renomear os diretórios para `ranking_metrics/` e `invariants_metrics/`, atualizar imports e documentação, preservando exports públicos e comportamento.
- Invariantes: nenhum cálculo, relatório, golden, ID de chunk ou etapa do retriever muda; `evals.retrieval.metrics` continua sendo a fachada pública.

## O que foi feito

Renomeados os diretórios internos para `ranking_metrics/` e `invariants_metrics/`; imports do evaluator e documentação foram atualizados para deixar explícito que ranking é avaliação, não reranking.

## O que muda na aplicação

A estrutura fica menos ambígua para manutenção; o runtime não ganhou reranker e o contrato JSON, as métricas e os exports públicos permanecem iguais.

## Jornada da aplicação nesta versão

Antes, a pasta `ranking/` podia sugerir uma etapa operacional de reranking; agora `ranking_metrics/` identifica diretamente o cálculo de qualidade, enquanto `invariants_metrics/` identifica regras do produto.

## Como usar e validar a aplicação nesta versão

Use `./rastro-ai/evals/retrieval/run_evaluation.sh test`; o comando público permanece igual. Para o fluxo real, use o comando `real` documentado no README do retrieval; nenhum reranker é executado.

## Cobertura por comportamento

- Imports públicos: `rastro-ai/tests/test_retrieval_evaluation.py`; esperado: 6 testes aprovados.
- Organização estrutural: `metrics/ranking_metrics/` e `metrics/invariants_metrics/`; esperado: grupos nomeados explicitamente.
- Integração real/smoke manual: não aplicada nesta rodada porque a v3 só altera caminhos internos e não muda o runtime; depende do banco e corpus preparados para uma validação futura.

## Instruções de validação

```bash
python3 -m compileall -q rastro-ai/evals/retrieval rastro-ai/tests && git diff --check
```

Resultado esperado: compilação e diff sem erros.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: 6 testes e `OK`, com imports públicos preservados.
