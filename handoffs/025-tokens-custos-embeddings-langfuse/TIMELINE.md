# Timeline — 025 tokens e custos de embeddings no Langfuse

## 2026-10-26 -03:00 — abertura

- Status: `proposed`.
- Dependência: implementação 024 verificada; código real conferido em `observability.py`, `indexing.py`, `openai_embedding_repository.py`, testes, Compose e configuração Python.
- Decisão: registrar tokens localmente via `tiktoken`, enviar `usage_details`, deixar custo inferido por modelo e suportar custo direto opcional.
- Pendência: aplicar a versão v1 e executar testes, Compose, smoke e verificação do painel.

## 2026-10-27 -03:00 — tentativa de finalização

- Status: `applied` (permanece não verificado).
- Evidência: Compose válido; testes `test_observability` e `test_openai_embedding_repository` passaram no container (`5` testes); hook estrutural validou os quatro handoffs.
- Limite de validação: execução completa no container encontrou erro de ambiente ao importar `evals` sem `PYTHONPATH=/app`; a execução local não possui dependências Python instaladas.
- Pendência bloqueadora: custo inferido ainda não foi confirmado no painel Langfuse; o fallback de custo direto permanece coberto por teste unitário, mas não houve confirmação integrada.
- Decisão: não atualizar `CURRENT.md`, não marcar `verified` e não gerar commit automático.

## 2026-10-27 -03:00 — finalização

- Status: `verified`.
- Evidência: Compose válido; 41 testes Python passaram no container com `PYTHONPATH=/app:/app/src` e `evals` montado; hook estrutural passou.
- Integração: usuário confirmou tokens e custo no Langfuse após configurar o preço direto por token.
- Resultado: modelo, usage e custo são registrados sem texto ou vetor no trace; fallback direto permanece disponível.
- Controle: `CURRENT.md` voltou a `idle`; `SEQUENCE.md` foi atualizado para `verified`.
