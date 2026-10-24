# 002 — Regras de arquivos não versionáveis

Versão: `v5` | Versão-base: `v4` | Data/hora: 2026-10-23 -03:00 | Status: `proposed`
Arquivos conferidos: `/home/dev/dev/ia/rastro-ai/rastro-ai/package.json`, `/home/dev/dev/ia/rastro-ai/rastro-ai/.dockerignore`, `/home/dev/dev/ia/rastro-ai/docker-compose.yml` e a raiz do repositório.
Reconciliação: não existe `.gitignore`; `dist/`, `tsconfig.build.tsbuildinfo` e `graphify-out/` estão presentes como artefatos locais.
Pendência: aplicar manualmente o novo `.gitignore` da raiz; nenhuma alteração direta foi feita na aplicação.
Ordem: criar o arquivo antes do commit; critério: `git check-ignore` confirmar artefatos ignorados e preservar `.env.example`, código e handoffs.
