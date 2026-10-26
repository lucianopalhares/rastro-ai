# Timeline — 024 Langfuse para observabilidade da indexação

## 2026-10-26 -03:00 — abertura
- Status: `proposed`.
- Arquivos conferidos: Compose principal, `.env.example`, `pyproject.toml`, fachada de indexação, repository de embeddings, testes e controles da implementação 023.
- Decisão: usar o Compose oficial self-hosted em arquivo complementar, com UI na porta externa `38917`.
- Escopo: observar indexação e chamadas de embedding com metadados sanitizados; não alterar chunking, PGVector ou contratos HTTP.
- Evidência-base: 023 verificada; serviço Python possui boundary único para persistência e embeddings configuráveis por ambiente.
