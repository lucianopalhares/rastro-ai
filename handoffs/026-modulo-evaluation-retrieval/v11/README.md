# 026/v11 — Sequência exata de chamadas

- Versão: `v11`; versão-base: `026/v10` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: a documentação listava métodos e classes, mas ainda não os apresentava em uma única sequência de execução.
- Escopo autorizado: reorganizar a árvore e a explicação no README do retrieval, sem alterar código ou fluxo.
- Invariantes: a ordem documentada deve corresponder ao código atual; comandos, métricas, dataset e runtime permanecem inalterados.
- Arquivo real conferido: `rastro-ai/evals/retrieval/README.md` e cadeia de chamadas do retrieval.

## O que foi feito

- Adicionada uma sequência numerada de `main()` até `EvaluationResult.as_dict()`.
- Abaixo da árvore, cada método/classe é explicado na mesma ordem em que é chamado.

## O que muda na aplicação

- Não há mudança de runtime; a documentação agora representa chamadas sequenciais, não apenas agrupamentos conceituais.
- A geração de resposta, API NestJS e DeepEval continuam fora do fluxo descrito.

## Jornada da aplicação nesta versão

Antes, a pessoa precisava inferir a ordem dentro da árvore. Agora, cada número corresponde a uma chamada ou etapa real e possui uma explicação imediatamente abaixo.

## Como usar e validar a aplicação nesta versão

Leia a seção `Sequência exata de chamadas` do README do retrieval para acompanhar o comando real. A integração PGVector continua manual.

## Cobertura por comportamento

- Ordem de chamadas: árvore numerada e lista explicativa no README.
- Evidência unitária: testes automatizados existentes permanecem aprovados.
- Evidência integrada: não se aplica à alteração documental; o fluxo real continua não executado nesta rodada.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v7/README.md handoffs/026-modulo-evaluation-retrieval/v7/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v8/README.md handoffs/026-modulo-evaluation-retrieval/v8/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v9/README.md handoffs/026-modulo-evaluation-retrieval/v9/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v10/README.md handoffs/026-modulo-evaluation-retrieval/v10/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v11/README.md handoffs/026-modulo-evaluation-retrieval/v11/TIMELINE.md`: esperado, vinte e quatro handoffs válidos.
