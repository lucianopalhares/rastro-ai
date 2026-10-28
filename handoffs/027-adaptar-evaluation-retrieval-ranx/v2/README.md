# 027/v2 — Separação entre ranking e invariantes

- Versão-base: `v1` aplicada; código real relido em `rastro-ai/evals/retrieval/metrics`, `evaluate.py`, testes e README.
- Estado encontrado: métricas clássicas e regras específicas estavam no mesmo diretório, embora os exports públicos já estivessem concentrados em `metrics/__init__.py`.
- Escopo autorizado: mover módulos para `metrics/ranking/` e `metrics/invariants/`, atualizar imports e documentar a distinção; preservar nomes públicos e comportamento.
- Invariantes: nenhum cálculo, relatório, golden, ID de chunk ou fluxo de runtime muda; imports por `evals.retrieval.metrics` continuam válidos.

## O que foi feito

Separados os módulos de ranking (`Recall`, `Precision`, `MRR`, `nDCG` e adapter ranx) dos invariantes do produto (`abstention`, `project_isolation` e `score_ordering`); o namespace público foi mantido como fachada de compatibilidade.

## O que muda na aplicação

A árvore de código passa a expressar a diferença entre métricas padronizadas e regras específicas, sem mudança de comportamento ou de contrato JSON. Não foram adicionadas novas métricas nem alterado o retriever.

## Jornada da aplicação nesta versão

Antes, todos os módulos ficavam em `metrics/`; agora o evaluator continua importando o mesmo namespace público, enquanto a manutenção interna identifica claramente ranking e invariantes.

## Como usar e validar a aplicação nesta versão

Use os mesmos comandos da v1: `./rastro-ai/evals/retrieval/run_evaluation.sh test` para a suíte controlada e o comando `real` do README para PGVector. O comportamento esperado é idêntico ao da v1.

## Cobertura por comportamento

- Compatibilidade de imports: `rastro-ai/tests/test_retrieval_evaluation.py`; esperado: imports públicos e 6 testes aprovados.
- Separação estrutural: inspeção de `metrics/ranking/` e `metrics/invariants/`; esperado: cada módulo no grupo correto.
- Integração real: não executada nesta rodada; depende do banco e corpus de evaluation.

## Instruções de validação

```bash
python3 -m compileall -q rastro-ai/evals/retrieval rastro-ai/tests && git diff --check
```

Resultado esperado: compilação e diff sem erros.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: 6 testes e `OK`, preservando o contrato público após a reorganização.
