# 026/v4 — Ordem de execução das métricas

- Versão: `v4`; versão-base: `026/v3` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: as métricas estavam desacopladas, mas os comentários não explicavam a ordem do fluxo entre CLI, retriever, métricas e agregação.
- Escopo autorizado: atualizar comentários JSDoc em funções, protocolo e serialização, sem alterar cálculos ou contratos.
- Invariantes: comportamento, entradas, saídas, dataset, runtime e integração PGVector permanecem inalterados.
- Arquivos reais conferidos: `rastro-ai/evals/retrieval/evaluate.py` e todos os módulos em `rastro-ai/evals/retrieval/metrics/`.

## O que foi feito

- Comentários do orquestrador documentam as etapas 0 a 6: CLI, dataset, retrieval, normalização, métricas, agregação e saída.
- Comentários de cada métrica documentam sua responsabilidade e a posição na execução por caso.
- O comentário de `as_dict()` registra que a serialização ocorre depois da agregação final.

## O que muda na aplicação

- Não há mudança de runtime ou de resultados; a alteração torna o fluxo auditável para manutenção e troubleshooting.
- A ordem documentada é: carregar dataset, buscar, normalizar IDs/scores, validar isolamento/score/abstinência, calcular ranking por k, agregar e serializar.
- Fora do escopo: refatoração adicional, DeepEval, novos casos e integração PGVector.

## Jornada da aplicação nesta versão

Antes, era necessário reconstruir a ordem lendo o corpo das funções. Agora, cada função informa o que faz e em qual etapa participa, preservando a separação da v2.

## Como usar e validar a aplicação nesta versão

Use os mesmos comandos da v3; a rodada é documental e não exige banco, embeddings ou credenciais. A integração PGVector continua manual e permanece fora desta verificação.

## Cobertura por comportamento

- Ordem documentada: inspeção dos comentários em `evaluate.py` e `metrics/*.py`.
- Preservação de comportamento: testes específicos e suíte completa sem alteração de resultados.
- Integração PGVector: não se aplica a comentários; permanece documentada nas versões anteriores.

## Instruções de validação

- `PYTHONPATH=src:. python3 -m unittest -q tests.test_retrieval_evaluation`: esperado, 4 testes aprovados.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest discover -s tests -p 'test*.py' -q`: esperado, 45 testes aprovados.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md`: esperado, dez handoffs válidos.
