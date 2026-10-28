# 027/v4 — Explicação simples das métricas

- Versão-base: `v3` aplicada; comentários reais conferidos em `metrics/ranking_metrics/` e `metrics/invariants_metrics/`.
- Estado encontrado: os comentários explicavam a implementação, mas não deixavam claro para uma pessoa não especialista qual pergunta cada métrica responde.
- Escopo autorizado: reescrever comentários JSDoc e README em linguagem simples, indicando interpretação de `0` e `1`; não alterar cálculos, imports ou contratos.
- Invariantes: código executável, resultados, nomes públicos, golden e fluxo de retrieval permanecem iguais.

## O que foi feito

Reescritos os comentários das métricas, invariantes e adapter para explicar finalidade, leitura do resultado e limites; adicionada tabela de interpretação e exemplos concretos ao README do retrieval.

## O que muda na aplicação

Não há mudança de runtime. O fluxo de avaliação fica compreensível por perguntas simples: encontrou tudo, trouxe ruído, encontrou cedo, ordenou bem, isolou o projeto ou soube ficar vazio.

## Jornada da aplicação nesta versão

Antes, os comentários priorizavam termos técnicos; agora cada função explica o que uma pessoa deve perguntar ao ler o resultado e o que significam valores altos ou baixos.

## Como usar e validar a aplicação nesta versão

Leia a tabela `Como ler cada resultado` no README do retrieval e execute `./rastro-ai/evals/retrieval/run_evaluation.sh test`; o comportamento esperado é o mesmo da v3.

## Cobertura por comportamento

- Legibilidade dos comentários: arquivos em `metrics/ranking_metrics/` e `metrics/invariants_metrics/`; esperado: cada função explica pergunta, interpretação e limite.
- Compatibilidade: `rastro-ai/tests/test_retrieval_evaluation.py`; esperado: 6 testes e `OK`.
- Integração real/smoke manual: não aplicada porque a v4 altera somente comentários e documentação; não há mudança de runtime para exercitar no PGVector.

## Instruções de validação

```bash
python3 -m compileall -q rastro-ai/evals/retrieval rastro-ai/tests && git diff --check
```

Resultado esperado: compilação e diff sem erros.

```bash
./rastro-ai/evals/retrieval/run_evaluation.sh test
```

Resultado esperado: 6 testes e `OK`.
