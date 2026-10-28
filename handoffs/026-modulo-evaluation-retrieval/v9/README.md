# 026/v9 — Árvore do fluxo real na documentação

- Versão: `v9`; versão-base: `026/v8` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: a documentação explicava o comando em texto, mas a relação entre Docker, evaluator, PGVector e métricas ainda precisava ser visualizada.
- Escopo autorizado: adicionar uma árvore textual do fluxo real ao README do retrieval, sem alterar código ou comandos.
- Invariantes: comando, dataset, runtime, métricas e pré-requisitos permanecem inalterados.
- Arquivo real conferido: `rastro-ai/evals/retrieval/README.md`.

## O que foi feito

- Adicionada uma árvore que detalha cada parte do comando e o caminho desde o container temporário até o JSON de métricas.
- Adicionado um resumo visual do fluxo e uma lista explícita do que o comando não faz.

## O que muda na aplicação

- Não há mudança de runtime; a documentação agora mostra a sequência de execução de forma visual.
- A árvore deixa explícito que o comando avalia retrieval, não API NestJS, indexação, geração de resposta ou DeepEval.

## Jornada da aplicação nesta versão

Antes, o comando precisava ser interpretado linha a linha. Agora, a árvore mostra container, mounts, imports, PGVector, chunks e métricas em uma única sequência.

## Como usar e validar a aplicação nesta versão

Leia `rastro-ai/evals/retrieval/README.md`, seção `O que acontece quando executo o comando real`, antes de executar a evaluation. A integração real continua manual.

## Cobertura por comportamento

- Fluxo documentado: árvore textual cobre Docker, evaluator, retriever, PGVector e métricas.
- Evidência unitária: testes automatizados existentes permanecem aprovados.
- Evidência integrada: não se aplica à alteração documental; o comando real continua não executado nesta rodada.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v7/README.md handoffs/026-modulo-evaluation-retrieval/v7/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v8/README.md handoffs/026-modulo-evaluation-retrieval/v8/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v9/README.md handoffs/026-modulo-evaluation-retrieval/v9/TIMELINE.md`: esperado, vinte handoffs válidos.
