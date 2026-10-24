# 011 — Persistência vetorial com pgvector
- Data/hora: 2026-10-24 -03:00 | Status: `verified` | Aplicação: raiz e IA.
- Dependência/ordem: `008` verificada; `011` verificada; `009` e `010` permanecem em standby.
- Objetivo: adicionar PostgreSQL/pgvector com volume e adaptar indexação/retrieval semântico persistente.
- Evolução: `v1` criou container, schema Supabase-compatível, embeddings locais, store PostgreSQL, seleção por ambiente, testes e documentação.
- Impacto: backend `memory` permanece padrão; `postgres` exige banco, dependências Python e download inicial do modelo.
- Critério: configuração Compose, suíte Python, schema pgvector e adapter real validados.
- Pendências: conectar upload da API a um worker de indexação e introduzir geração por LLM em etapas posteriores.
- Pasta: `handoffs/011-persistencia-vetorial-pgvector/` | Próxima ação: manter `009` em standby até autorização.
