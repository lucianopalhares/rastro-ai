# Linha do tempo — 011 v1

## v1 — Aplicação e verificações locais

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais: Compose, schema PostgreSQL, configuração e módulos Python, README e testes conferidos.
- Mudanças: persistência pgvector, embeddings multilíngues, consulta cosine, seleção por ambiente e testes do adapter.
- Verificação: 21 testes Python, compilação, `docker compose config` e `git diff --check` aprovados.
- Pendência: validação manual do schema e fluxo real depende de iniciar o container pgvector.
