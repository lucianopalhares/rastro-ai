# Timeline — 023/v1 Busca semântica determinística pela API

## 2026-10-26 -03:00 — rodada v1
- Status: `applied`.
- Arquivos reais conferidos antes da aplicação: `rastro-api/src/modules/documents/*`, `rastro-ai/src/rastro_ai/service.py`, retrieval, testes, READMEs e Compose.
- Mudanças aplicadas: contratos, proxy e endpoints HTTP; validações de payload/limite; serialização de score, offsets e citação; testes e documentação.
- Evidência preliminar: OpenAI respondeu embedding de 384 dimensões; fluxo direto de persistência respondeu; smoke do indexador respondeu HTTP `200` após reinício.
- Evidência posterior: 37 testes Python, 12 testes NestJS, build TypeScript, smoke direto/API HTTP `200`, limite inválido HTTP `400` e projeto sem dados retornando lista vazia.
- Verificação final: hook estrutural passou após alinhar `SEQUENCE.md`; implementação permanece `applied` até finalização formal.

## 2026-10-26 -03:00 — finalização
- Status: `verified`.
- Evidência: todos os testes, build, smoke e validações de contrato descritos no README passaram.
- Resultado: v1 encerrada; código real e documentação permanecem nas aplicações, sem cópia para o handoff.
