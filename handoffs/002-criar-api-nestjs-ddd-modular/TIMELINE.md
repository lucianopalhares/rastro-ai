## v5 — Regras de arquivos não versionáveis

- Data/hora: 2026-10-23 -03:00
- Status: `proposed`
- Versão-base: `v4`
- Arquivos conferidos: raiz do repositório, `rastro-ai/package.json`, `rastro-ai/.dockerignore` e `docker-compose.yml`.
- Itens aplicados/parciais/divergentes/ausentes: `.gitignore` ausente; artefatos `dist/`, `*.tsbuildinfo` e `graphify-out/` presentes; nenhum trecho anterior aplicável.
- Mudança proposta: criar `.gitignore` na raiz com regras para dependências, builds, ambientes locais, logs, editores e análise gerada.
- Problema resolvido: reduzir arquivos derivados e sensíveis no controle de versão; pendência: aplicação manual e validação com `git check-ignore`.
- Verificação: handoff validado pelo hook; testes funcionais pendentes após aplicação.

## Finalização — aplicação confirmada

- Data/hora: 2026-10-23 -03:00
- Status: `applied`
- Versão-base: `v5`
- Arquivos conferidos: handoffs das versões `v1` a `v5`; aplicação confirmada pelo responsável.
- Itens aplicados/parciais/divergentes/ausentes: aplicação declarada concluída; testes e verificações ainda não evidenciados.
- Mudança proposta: encerrar a implementação como aplicada, preservando a pendência de validação técnica.
- Problema resolvido: ciclo de aplicação manual concluído; pendência: promover a `verified` após os testes.
- Verificação: validação estrutural do handoff `v5` aprovada; build, testes e `git check-ignore` pendentes.
