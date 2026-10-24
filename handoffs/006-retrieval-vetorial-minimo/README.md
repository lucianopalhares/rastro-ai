# 006 — Retrieval vetorial mínimo

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: IA (`rastro-ai`).
- Dependência/ordem: `005` verificada; etapa 4 da Fase 1; antecede `007`.
- Objetivo: indexar chunks em memória e consultar resultados relevantes isolados por projeto.
- Evolução: `v1` adicionou contrato, store vetorial determinístico, caso de uso, fachada, documentação e testes.
- Impactos: prepara retrieval sem modelo, banco, embeddings externos ou alteração no fluxo de extração.
- Critério: testes de ranking, filtro por projeto, validação de entrada, compilação e hook passaram; implementação verificada.
- Pasta: `handoffs/006-retrieval-vetorial-minimo/` | Próxima ação: iniciar `007-respostas-com-citacoes`.
