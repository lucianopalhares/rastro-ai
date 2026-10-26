# Timeline — 023 Busca semântica determinística pela API

## 2026-10-26 -03:00 — 023-v1
- Status: `applied`.
- Arquivos reais conferidos: controller/módulo da API, adapter HTTP, serviço Python, retrieval/PGVector, testes e READMEs.
- Mudanças: criado contrato e proxy da busca na API; criado POST `/search` no Rastro AI; documentação e testes adicionados.
- Problema resolvido: a busca vetorial existia apenas como fachada interna e não era consumível pela API.
- Diagnóstico: chamada OpenAI direta e fluxo Python → PGVector responderam; processo HTTP foi reiniciado antes do smoke bem-sucedido.
- Evidência: 37 testes Python, 12 testes NestJS, build TypeScript, smoke direto/API e filtro de projeto sem resultados cruzados aprovados.
- Verificação: sequência alinhada com a tarefa ativa; hook estrutural passou nos quatro arquivos do handoff.

## 2026-10-26 -03:00 — finalização
- Status: `verified`.
- Evidência: testes Python/NestJS, build, smoke API → Rastro AI → PostgreSQL, validação de limite/isolamento e hook estrutural aprovados.
- Resultado: endpoint de busca semântica determinística entregue; duplicatas existentes no banco de teste registradas como risco fora do escopo.
- Controle: `CURRENT.md` passou a `idle` e `SEQUENCE.md` marcou a implementação como `verified`.
