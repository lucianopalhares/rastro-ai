# 012 — Integrar upload da API à indexação Python
- Data/hora: 2026-10-25 -03:00 | Status: `verified` | Aplicação: API, IA e raiz.
- Objetivo: encaminhar arquivos recebidos pela API para indexação na aplicação Python.
- Evolução: `v1` implementou a ponte HTTP API → Python; `v2` reutiliza o modelo `Document` e adiciona repository externo de embeddings OpenAI; `v3` melhora o chunking estrutural; `v4` usa `tiktoken` para contar tokens reais; `v5` ajusta o timeout da chamada externa; `v6` separa o Python por capacidades.
- Dependência/ordem: upload e contrato da API antes do processamento Python; persistência vetorial `011` já verificada.
- Impacto: o upload envia o modelo `Document`; o indexador usa chunks estruturais por tokens e o vector store PostgreSQL grava embeddings externos em lote quando `OPENAI_API_KEY` está configurada.
- Pendências: retry, idempotência explícita, processamento assíncrono e remoção futura dos wrappers legados permanecem fora desta rodada.
- Critério: testes da API/Python, contrato do repository, schema pgvector, Compose, hook estrutural e smoke real com embeddings foram executados com sucesso.
- Pasta: `handoffs/012-integrar-upload-indexacao-python/` | Próxima ação: nenhuma tarefa sucessora foi ativada; aguardar nova autorização explícita.
