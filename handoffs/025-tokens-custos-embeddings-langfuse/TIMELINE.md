# Timeline — 025 tokens e custos de embeddings no Langfuse

## 2026-10-26 -03:00 — abertura

- Status: `proposed`.
- Dependência: implementação 024 verificada; código real conferido em `observability.py`, `indexing.py`, `openai_embedding_repository.py`, testes, Compose e configuração Python.
- Decisão: registrar tokens localmente via `tiktoken`, enviar `usage_details`, deixar custo inferido por modelo e suportar custo direto opcional.
- Pendência: aplicar a versão v1 e executar testes, Compose, smoke e verificação do painel.
