## v3 — Dependência Docker corrigida

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: imagens Docker de produção e desenvolvimento do serviço `rastro-ai`.
- Mudança: `langchain-text-splitters>=0.3,<1` foi incluído nos dois comandos de instalação das imagens.
- Problema resolvido: `ai-indexer` encerrava ao importar `LangChainTextChunker` por pacote ausente no container.
- Verificação: build sem cache, import no container, Compose saudável, 30 testes, evaluation 20/20, compilação e hook estrutural aprovados.
