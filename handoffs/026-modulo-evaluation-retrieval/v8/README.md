# 026/v8 — Detalhamento dos comandos de validação

- Versão: `v8`; versão-base: `026/v7` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: a documentação separava os fluxos, mas ainda deixava comandos sem explicar o que cada parte fazia e como interpretar o resultado.
- Escopo autorizado: detalhar a seção `## Instruções de validação` do README do retrieval, sem alterar código ou comandos internos.
- Invariantes: Docker continua oficial; teste automatizado usa retriever fake; fluxo real usa PGVector; qualidade exige comparação com thresholds.
- Arquivos reais conferidos: `rastro-ai/evals/retrieval/README.md`, Compose e controles da 026.

## O que foi feito

- A seção de validação agora explica onde executar, o papel de cada trecho dos comandos, pré-requisitos e resultado esperado.
- Os dois cenários continuam separados: teste do código e avaliação da busca real.

## O que muda na aplicação

- Não há mudança de runtime, métricas ou dataset; somente a documentação foi detalhada.
- A pessoa usuária consegue distinguir “comando executou” de “qualidade do ranking foi aprovada”.
- Fora do escopo: thresholds automáticos e execução do corpus real.

## Jornada da aplicação nesta versão

Antes, a seção apresentava comandos compactos sem explicar seus mounts, dependências e limites. Agora, cada comando vem acompanhado de sua finalidade e do resultado que comprova.

## Como usar e validar a aplicação nesta versão

Leia a seção `## Instruções de validação` de `rastro-ai/evals/retrieval/README.md`; ela contém dois caminhos detalhados e a interpretação de sucesso técnico e de qualidade.

## Cobertura por comportamento

- Teste automatizado: comando Docker, mounts, retriever fake e saída `OK` explicados.
- Fluxo real: preparação dos serviços, comando do evaluator, pré-requisitos e JSON/thresholds explicados.
- Evidência unitária: os testes existentes continuam aprovados; integração real não foi executada.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`; o README explica cada opção.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d vector-db ai-indexer && docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m evals.retrieval.evaluate --dataset /app/evals/dataset/golden.json --ks 1,3,5`: esperado, JSON real quando o corpus estiver indexado; não executado nesta rodada.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v7/README.md handoffs/026-modulo-evaluation-retrieval/v7/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v8/README.md handoffs/026-modulo-evaluation-retrieval/v8/TIMELINE.md`: esperado, dezoito handoffs válidos.
