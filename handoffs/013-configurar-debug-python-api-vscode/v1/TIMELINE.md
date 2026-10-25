# Timeline — 013/v1

## v1 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: `.vscode/launch.json` ausente; `rastro-api/package.json`, `rastro-api/src/main.ts`, `rastro-ai/src/rastro_ai/service.py` e `docker-compose.yml`.
- Mudanças aplicadas: compound do VS Code para Python/NestJS e script `start:debug` da API.
- Problema resolvido: ausência de breakpoint reproduzível nos dois processos do fluxo API → Python.
- Pendências: validações de build, compilação Python, hook de handoff e smoke manual do VS Code.

## Verificações da v1 — 2026-10-24 -03:00

- `json.tool`, manifest Node, `docker compose config`, compilação Python e `git diff --check`: aprovados.
- Hook `validate-handoffs.sh`: aprovado com quatro arquivos válidos.
- `npm run build` da API: pendente, pois `rastro-api/node_modules/.bin/nest` não está disponível neste ambiente.
- Smoke manual no VS Code: pendente, depende da execução local com as extensões Python/Debugger instaladas.
