# 026/v13 — Porta do attach do debugger

- Versão: `v13`; versão-base: `026/v12` aplicada; data: 2026-10-27 -03:00; status: `applied`.
- Estado-base: o comando de debug usava a porta 5679 no host, mas o `launch.json` ainda fazia attach na 5678 e não mapeava `/app/evals`.
- Escopo autorizado: ajustar a configuração local do VS Code e alinhar a documentação; não alterar runtime ou Compose.
- Invariantes: `debugpy` continua escutando na porta 5678 dentro do container; somente a porta publicada e o attach do host usam 5679.
- Arquivos reais alterados: `.vscode/launch.json` e `rastro-ai/evals/retrieval/README.md`.

## O que foi feito

- Alterada a configuração `Docker: Python AI service` para conectar em `127.0.0.1:5679`.
- Adicionado o mapeamento local `rastro-ai/evals` para `/app/evals`.
- Atualizada a documentação para informar que a configuração já está pronta para a porta 5679.

## O que muda na aplicação

- Não há mudança no runtime da aplicação ou no fluxo de avaliação.
- O VS Code passa a conectar automaticamente na porta publicada pelo comando temporário de debug.
- Breakpoints em `evaluate.py` passam a ter mapeamento explícito entre host e container.

## Jornada da aplicação nesta versão

O container temporário publica `5679:5678`, o `debugpy` escuta internamente em 5678 e a configuração do VS Code conecta no host em 5679, preservando também o mapeamento de `/app/src` e adicionando `/app/evals`.

## Como usar e validar a aplicação nesta versão

Execute o comando de debug documentado no README do retrieval, mantenha o terminal aguardando o attach e pressione `F5` com `Docker: Python AI service` selecionado.

## Cobertura por comportamento

- Porta do host: attach configurado em `5679`, evitando conflito com o `ai-indexer` permanente.
- Porta interna: `debugpy` permanece em `0.0.0.0:5678`.
- Breakpoints: `/app/evals` mapeado para `rastro-ai/evals`.
- Runtime: nenhuma lógica de retrieval ou métrica alterada.

## Instruções de validação

- Conferir `.vscode/launch.json`: esperado, `Docker: Python AI service` usa `port: 5679` e possui mapeamento `/app/evals`.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -e PYTHONPATH=/app:/app/src -v "$PWD/rastro-ai/tests:/app/tests:ro" -v "$PWD/rastro-ai/evals:/app/evals:ro" ai-indexer python -m unittest -q tests.test_retrieval_evaluation`: esperado, `OK`.
- Evidência unitária: os 4 testes de `tests.test_retrieval_evaluation` devem terminar com `OK`; essa evidência confirma que o contrato das métricas permanece preservado.
- Validação manual integrada: pendente de execução pelo VS Code com `vector-db`, corpus indexado e credenciais configuradas; o critério é o attach em 5679 e o breakpoint em `evaluate.py`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh` com todos os README/TIMELINE da implementação 026: esperado, todos os handoffs válidos.
