# 026/v10 — Métodos e classes do fluxo real

- Versão: `v10`; versão-base: `026/v9` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: a árvore explicava componentes, mas não nomeava todos os métodos e classes chamados pelo comando real.
- Escopo autorizado: detalhar a árvore e explicar os métodos/classes no README do retrieval, sem alterar código.
- Invariantes: fluxo, comandos, métricas, dataset e runtime permanecem inalterados.
- Arquivo real conferido: `rastro-ai/evals/retrieval/README.md` e cadeia real de retrieval Python.

## O que foi feito

- A árvore agora apresenta `main`, `run_evaluation`, fachada, composition root, casos de uso, store PGVector, embeddings e métricas.
- Cada função/classe recebeu uma explicação curta de responsabilidade e posição no fluxo.

## O que muda na aplicação

- Não há mudança de runtime; a documentação permite seguir o fluxo pelo nome real dos símbolos.
- A geração de respostas, API NestJS e DeepEval continuam explicitamente fora desse caminho.

## Jornada da aplicação nesta versão

Antes, a árvore mostrava apenas etapas genéricas. Agora, uma pessoa consegue sair do comando e acompanhar os métodos/classes até o JSON de métricas.

## Como usar e validar a aplicação nesta versão

Leia a seção `Árvore com os métodos e classes chamados` do README do retrieval antes de executar o comando real. A integração continua manual.

## Cobertura por comportamento

- Fluxo documentado: árvore com símbolos reais e explicação abaixo.
- Evidência unitária: testes automatizados existentes permanecem aprovados.
- Evidência integrada: não se aplica à alteração documental; o fluxo real continua não executado nesta rodada.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v7/README.md handoffs/026-modulo-evaluation-retrieval/v7/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v8/README.md handoffs/026-modulo-evaluation-retrieval/v8/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v9/README.md handoffs/026-modulo-evaluation-retrieval/v9/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v10/README.md handoffs/026-modulo-evaluation-retrieval/v10/TIMELINE.md`: esperado, vinte e dois handoffs válidos.
