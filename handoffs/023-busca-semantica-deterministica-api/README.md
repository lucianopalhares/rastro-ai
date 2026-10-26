# 023 — Busca semântica determinística pela API
- Data/hora: 2026-10-26 -03:00 | Status: `verified`; aplicações: `rastro-api` e `rastro-ai`.
- Objetivo: expor busca semântica filtrada por projeto, limite, score e citações pela API NestJS.
- Dependência/ordem: `011`, `014`, `015`, `017` verificadas; API publica o contrato antes do proxy Python.
- Evolução: `v1` adicionou `/api/v1/documents/search`, `/search` no Rastro AI e validações do contrato.
- Decisão/invariante: LangChain/PGVector continua responsável por embeddings e ranking; nenhum agente foi introduzido.
- Diagnóstico: a chave e o embedding funcionam; o timeout observado veio de processo HTTP preso/requisições anteriores, limpo no smoke após restart.
- Evidência: 37 testes Python, 12 testes NestJS, build TypeScript, smoke API → Python → PostgreSQL e hook estrutural aprovados.
- Resultado: implementação verificada, sem bloqueio técnico; duplicatas de dados de teste permanecem como risco conhecido fora do escopo.
- Pasta/próxima ação: `handoffs/023-busca-semantica-deterministica-api/`; nenhuma etapa seguinte ativa.
