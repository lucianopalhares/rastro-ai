# 005 — Extração e chunking

- Data/hora: 2026-10-24 -03:00 | Status: `verified`
- Aplicação afetada: IA (`rastro-ai`).
- Dependência/ordem: `004` verificada; etapa 3 da Fase 1; próxima etapa `006`.
- Objetivo: extrair texto UTF-8 de `.md`/`.txt` e gerar chunks determinísticos com offsets.
- Evolução: `v1` criou o módulo Python, testes padrão e configuração mínima do pacote; `v2` reorganizou a indexação em módulos DDD e preservou a fachada legada; `v3` documentou a arquitetura, impactos e validação na aplicação.
- Impactos: prepara a indexação; embeddings, fila, persistência vetorial e conexão com a API permanecem fora do escopo.
- Critério: sete testes unitários, compilação e hook estrutural passaram; implementação verificada.
- Pasta: `handoffs/005-extracao-e-chunking/` | Próxima ação: iniciar a etapa `006` de retrieval vetorial mínimo.
