# Linha do tempo — 012/v6 Separação modular da aplicação Python

## v6 — Limites por capacidade aplicados

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Arquivos reais conferidos: árvore `rastro-ai/src/rastro_ai`, imports de produção e suíte Python.
- Mudanças aplicadas: módulos `documents`, `chunking`, `embeddings`, `semantic_search` e `document_ingestion`; fachadas de produção migradas; compatibilidade preservada.
- Problema resolvido: namespace agregado dificultava substituir chunking, provider de embeddings ou vector store isoladamente.
- Verificação: import smoke, 26 testes, compilação, build da imagem, diff check e hook estrutural aprovados; smoke API → OpenAI → pgvector confirmou 1 chunk curto e 3 chunks longos com embeddings `384`.
- Pendência: remover o namespace legado somente após migrar consumidores externos.
