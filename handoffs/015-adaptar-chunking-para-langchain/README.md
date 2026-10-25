# 015 — Adaptar chunking para LangChain
- Data/hora: 2026-10-25 -03:00 | Status: `verified`; aplicação: IA (`rastro-ai`).
- Objetivo: substituir o acoplamento direto do caso de uso ao chunker por um adaptador compatível com LangChain.
- Dependência/ordem: `014` verificada; preservar `DocumentChunk`, offsets, projeto, índice e baseline antes da troca.
- Motivo: preparar a evolução para LangChain sem colocar dependência externa dentro do domínio.
- Impacto: futura estratégia de chunking configurável; custo/latência de execução permanecem fora até a validação da biblioteca.
- Critério: `IndexDocumentUseCase` usa `TextChunker`, implementação LangChain é isolada na infraestrutura e testes/evaluation preservam o contrato.
- Evolução: `v1` registrou o plano; `v2` aplicou chunking; `v3` corrigiu Docker; `v4` unificou a fachada; `v5` adaptou embeddings; `v6` adaptou PGVector; `v7` preparou RAG; `v8` documentou o splitter; `v9` removeu o schema vetorial legado.
- Pasta: `handoffs/015-adaptar-chunking-para-langchain/` | Próxima ação: nenhuma; implementação finalizada nesta rodada.
