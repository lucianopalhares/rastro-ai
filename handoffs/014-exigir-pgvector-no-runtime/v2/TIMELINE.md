## v2 — Aplicação do backend persistente obrigatório

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais conferidos: fachada `retrieval.py`, handler `service.py`, adaptadores de retrieval, testes de indexação/retrieval/evaluation, README da IA, Compose e schema pgvector.
- Mudanças aplicadas: `retrieval.py` rejeita backend ausente ou diferente de `postgres`; serviço reporta backend persistente; store em memória foi documentado como double explícito; testes e README foram ajustados.
- Problema resolvido: o runtime não degrada silenciosamente de embeddings/pgvector para ranking lexical em memória.
- Verificação: 28 testes, `compileall`, `docker compose config`, containers saudáveis e hook estrutural passaram; import sem backend falhou explicitamente como esperado.
- Pendências: executar smoke HTTP com `OPENAI_API_KEY`; depois promover a versão para `verified`.
