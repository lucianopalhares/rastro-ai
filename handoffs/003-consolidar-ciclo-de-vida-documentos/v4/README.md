# v4 — Corrigir caminho da API no Compose

- Versão-base: `v3`; criada após o Compose procurar `Dockerfile.dev` na pasta antiga.
- Data: 2026-10-23 | Status: `proposed`.
- Arquivo conferido: `docker-compose.yml`; Dockerfile real confirmado em `rastro-api/Dockerfile.dev`.
- Já aplicado: correções TypeScript da `v3` são independentes e não são repetidas.
- Divergência: contexto de build e volume ainda apontam para `rastro-ai`.
- Pendência: aplicar o handoff de raiz e reconstruir o serviço `api`.
- Ordem: aplicar Compose → validar configuração → executar build e health check.
- Verificação: `docker compose config` e `docker compose up --build`.
