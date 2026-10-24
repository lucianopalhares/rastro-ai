# Linha do tempo — 007 Respostas com citações

## v1 — Resposta extrativa com evidências

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: `rastro-ai` inteiro, retrieval, entidades, testes, README e referências da Fase 1.
- Mudanças aplicadas: caso de uso `AnswerQuestionUseCase`, contratos `Answer`/`Citation`, fachada `answer_question`, testes e documentação.
- Problema: o retrieval retornava chunks, mas não havia resposta citável nem negativa explícita sem evidência.
- Impacto: respostas reproduzem trechos recuperados e preservam isolamento por projeto; LLM, LangGraph, validação generativa e observabilidade ficam fora do escopo.
- Pendências: baseline de evaluation, geração por modelo, validação de citações geradas e integração assíncrona permanecem futuras.
- Verificação: 14 testes passaram; compilação e hook estrutural pendentes nesta rodada.

## Finalização — v1 verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Arquivos reais conferidos: fontes, testes, README da aplicação, jornada de uso e registros da implementação.
- Mudanças de finalização: status atualizado, critérios e validações consolidados; nenhuma alteração adicional de runtime.
- Problema resolvido: resposta com citações e ausência de evidência confirmadas no fluxo integrado local.
- Pendências: API, frontend, worker, LLM, evaluation e observabilidade permanecem fora da implementação 007.
- Verificação: 14 testes, `compileall`, smoke integrado e hook estrito passaram.
- Próxima etapa: `008-evaluation-baseline`.
