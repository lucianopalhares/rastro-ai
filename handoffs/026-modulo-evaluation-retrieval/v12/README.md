# 026/v12 — Debug da avaliação real

- Versão: `v12`; versão-base: `026/v11` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: o README explicava o comando normal, mas não informava que ele não inicia `debugpy` nem como conectar o VS Code ao evaluator.
- Escopo autorizado: atualizar a documentação do retrieval e o registro da rodada; não alterar runtime, Compose ou configuração do VS Code.
- Invariantes: o comando normal continua executando `python -m evals.retrieval.evaluate`; a variante de debug deve executar o mesmo módulo com `debugpy` e aguardar o attach.
- Arquivos reais conferidos: `rastro-ai/evals/retrieval/README.md`, `docker-compose.yml`, `rastro-ai/Dockerfile.dev` e `.vscode/launch.json`.

## O que foi feito

- Documentada a diferença entre executar o evaluator e executá-lo sob `debugpy`.
- Adicionado comando copiável com `--listen`, `--wait-for-client` e `-p 5678:5678`.
- Documentado o attach `Docker: Python AI service`, o mapeamento `/app/evals` e os sinais de execução sem debugger.
- Documentado o conflito quando o `ai-indexer` permanente já ocupa a porta 5678 e as alternativas `stop ai-indexer` ou `5679:5678`.

## O que muda na aplicação

- Não há mudança de runtime, métricas, dataset ou fluxo de retrieval.
- A documentação agora permite depurar `main()`, `run_evaluation()` e as métricas do evaluator dentro do container temporário.
- O comando normal continua sem debugger; o comando de debug é uma alternativa explícita para investigação.
- Quando o serviço normal permanece ativo, o debugger usa uma porta diferente no host, sem alterar a porta interna do container.

## Jornada da aplicação nesta versão

O comando de debug cria um container temporário, publica uma porta livre do host para a porta 5678 interna, aguarda o attach do VS Code e então executa o mesmo `evals.retrieval.evaluate`; nenhum método de retrieval foi alterado.

## Como usar e validar a aplicação nesta versão

Use a execução normal para medir o retrieval e a execução com `debugpy` somente quando precisar acompanhar o código. Se o `ai-indexer` estiver ativo, escolha uma porta livre no host, como `5679`, e configure o attach do VS Code para a mesma porta.

## Cobertura por comportamento

- Execução normal: o evaluator continua sendo executado sem debugger pelo comando `python -m evals.retrieval.evaluate`.
- Execução depurável: `debugpy` escuta na porta 5678, aguarda o VS Code e executa o mesmo módulo de avaliação.
- Breakpoints do evaluator: o mapeamento `/app/evals` relaciona o arquivo do container ao arquivo aberto localmente.
- Runtime: nenhuma lógica de retrieval, métrica, dataset ou configuração de produção foi alterada.

## Instruções de validação

- Conferir `rastro-ai/evals/retrieval/README.md`: esperado, existir uma seção de debug com o comando completo, `--wait-for-client`, attach do VS Code e mapeamento `/app/evals`.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`; a alteração é documental, mas o contrato das métricas deve permanecer preservado.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- Validação manual integrada: não executada nesta rodada; exige VS Code conectado, `vector-db` ativo, corpus indexado e credenciais OpenAI, e a alteração desta rodada é somente documental.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/026-modulo-evaluation-retrieval/README.md handoffs/026-modulo-evaluation-retrieval/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v1/README.md handoffs/026-modulo-evaluation-retrieval/v1/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v2/README.md handoffs/026-modulo-evaluation-retrieval/v2/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v3/README.md handoffs/026-modulo-evaluation-retrieval/v3/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v4/README.md handoffs/026-modulo-evaluation-retrieval/v4/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v5/README.md handoffs/026-modulo-evaluation-retrieval/v5/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v6/README.md handoffs/026-modulo-evaluation-retrieval/v6/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v7/README.md handoffs/026-modulo-evaluation-retrieval/v7/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v8/README.md handoffs/026-modulo-evaluation-retrieval/v8/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v9/README.md handoffs/026-modulo-evaluation-retrieval/v9/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v10/README.md handoffs/026-modulo-evaluation-retrieval/v10/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v11/README.md handoffs/026-modulo-evaluation-retrieval/v11/TIMELINE.md handoffs/026-modulo-evaluation-retrieval/v12/README.md handoffs/026-modulo-evaluation-retrieval/v12/TIMELINE.md`: esperado, todos os handoffs válidos.
