# Timeline — 013/v2

## v2 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: `docker-compose.yml`, `.vscode/launch.json`, `rastro-api/package.json`, `rastro-ai/Dockerfile.dev`, `rastro-ai/README.md` e `rastro-api/README.md`.
- Mudanças aplicadas: debug Docker da API via inspector Node, debug Python via `debugpy`, Dockerfile de desenvolvimento Python, perfis attach e documentação dos comandos.
- Problema resolvido: v1 usava processos no host enquanto a execução oficial ocorre no Compose.
- Pendências: build Docker, health checks e attach manual do VS Code.

## Ajuste de breakpoints — 2026-10-24 -03:00

- O log Python indicou módulos congelados; os comandos Docker foram ajustados com `-Xfrozen_modules=off`.
- A imagem `ai-indexer` deve ser reconstruída antes do próximo smoke para validar o ajuste.

## Verificações da v2 — 2026-10-24 -03:00

- `docker compose build api ai-indexer`: aprovado.
- `docker compose up -d vector-db ai-indexer api`: aprovado; API, IA e PostgreSQL ficaram saudáveis.
- Health checks API/Python e inspector Node: aprovados com HTTP `200` e resposta em `9229/json/list`.
- JSON, Compose config, `git diff --check` e hook estrutural: aprovados.
- Attach visual no VS Code: pendente de execução manual pelo usuário.
