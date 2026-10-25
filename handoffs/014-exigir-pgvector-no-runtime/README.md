# 014 — Exigir pgvector no runtime
- Data/hora: 2026-10-25 -03:00 | Status: `verified`; aplicação: IA (`rastro-ai`).
- Objetivo: eliminar o fallback lexical silencioso e tornar embeddings/pgvector obrigatórios no runtime.
- Dependência/ordem: `013` verificada; alterar serviço Python, testes e documentação da IA.
- Motivo: impedir que um ambiente sem configuração aparente executar busca semântica usando apenas palavras.
- Impacto: falha explícita sem backend persistente; store em memória fica restrito a testes explícitos.
- Critério: indexação e consulta usam `PostgresVectorStore`, configuração inválida falha cedo e testes cobrem o contrato.
- Evolução: `v1` registrou o plano; `v2` removeu o fallback de runtime; `v3` confirmou upload, embeddings e persistência pgvector no smoke real.
- Pasta: `handoffs/014-exigir-pgvector-no-runtime/` | Próxima ação: nenhuma; tarefa verificada e pronta para commit.
