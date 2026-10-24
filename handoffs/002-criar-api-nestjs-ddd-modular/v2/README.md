# 002 — Corrigir instalação Docker sem lockfile

Versão: `v2` | Versão-base: `v1` | Data/hora: 2026-10-23 -03:00 | Status: `proposed`
Arquivos conferidos: `/home/dev/dev/ia/rastro-ai/rastro-ai/Dockerfile.dev`, `package.json`, `docker-compose.yml`; proposta anterior: instalação via `npm install` já existente em v1, mas ausente no arquivo real.
Reconciliação: a composição e o pacote estão aplicados; o `Dockerfile.dev` real diverge e usa `npm ci`, sem `package-lock.json` ou `npm-shrinkwrap.json`.
Pendência: aplicar o handoff de `api/Dockerfile.dev`; não inclui lockfile nesta rodada.
Ordem: aplicar o trecho e executar `docker compose config` e `docker compose build api`; critério: build sem erro EUSAGE do `npm ci`.
