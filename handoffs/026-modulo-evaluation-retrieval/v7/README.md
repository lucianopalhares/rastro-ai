# 026/v7 — Comandos oficiais no Docker

- Versão: `v7`; versão-base: `026/v6` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: a documentação apresentava comandos locais como caminho principal, embora o serviço oficial rode no container `ai-indexer`.
- Escopo autorizado: atualizar README do módulo e índice de evaluation para priorizar Docker e manter host apenas como alternativa.
- Invariantes: nenhum código de runtime ou métrica muda; testes continuam sem rede; fluxo real mantém PGVector e embeddings configurados pelo Compose.
- Arquivos reais conferidos: `docker-compose.yml`, `Dockerfile`, READMEs de evaluation e handoffs ativos.

## O que foi feito

- Os testes automatizados agora têm comando Docker com mounts explícitos de `tests` e `evals`.
- A execução real agora inicia `vector-db`/`ai-indexer` e roda o evaluator em container com o golden montado.
- Os comandos locais foram mantidos somente como alternativa para desenvolvimento com dependências no host.

## O que muda na aplicação

- A documentação passa a refletir o ambiente oficial e reproduzível do projeto.
- Nenhum comportamento de runtime, métrica ou dataset foi alterado.
- Fora do escopo: execução real nesta rodada, thresholds automáticos e DeepEval.

## Jornada da aplicação nesta versão

Antes, uma pessoa poderia tentar executar um comando local sem as dependências instaladas e concluir que a evaluation não funcionava. Agora, o caminho principal usa a imagem e o ambiente do `ai-indexer`.

## Como usar e validar a aplicação nesta versão

Leia `rastro-ai/evals/retrieval/README.md` e execute primeiro o teste Docker. Para o fluxo real, suba `vector-db`/`ai-indexer`, monte `evals` no container de execução e rode o módulo contra o golden único. A integração real está indisponível no teste automático e não foi executada nesta rodada.

## Cobertura por comportamento

- Comando automatizado: README do módulo documenta container, mounts e resultado esperado.
- Evidência unitária: os testes unitários do retrieval permanecem aprovados no container.
- Comando real: README documenta Compose, dependências, golden montado e critérios de qualidade.
- Código local: permanece apenas como alternativa explicitamente identificada.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, testes do módulo aprovados.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d vector-db ai-indexer && docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m evals.retrieval.evaluate --dataset /app/evals/dataset/golden.json --ks 1,3,5`: esperado, JSON do fluxo real quando corpus, PGVector e credenciais estiverem configurados; não executado nesta rodada.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v7/README.md handoffs/026-modulo-evaluation-retrieval/v7/TIMELINE.md`: esperado, dezesseis handoffs válidos.
