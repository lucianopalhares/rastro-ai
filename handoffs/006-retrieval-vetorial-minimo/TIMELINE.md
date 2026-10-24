# Linha do tempo — 006 Retrieval vetorial mínimo

## v1 — Contrato e retrieval determinístico em memória

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: pacote `rastro-ai`, testes de extração/chunking, README e sequência da Fase 1.
- Mudanças aplicadas: adicionado metadado de projeto aos chunks, porta de store, ranking vetorial determinístico, caso de uso, fachada, documentação e testes.
- Problema: não havia consulta de chunks relevantes nem isolamento por projeto após a etapa de chunking.
- Impacto: retrieval local e reproduzível; embeddings reais, persistência PostgreSQL/pgvector, worker e API permanecem fora do escopo.
- Pendências: avaliar substituição por embeddings reais e store persistente em etapa posterior.
- Verificação: 11 testes, `compileall` e `validate-handoffs.sh` passaram.

## Finalização — verificação da implementação

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Arquivos reais conferidos: pacote `rastro-ai`, testes, README da aplicação e módulos de retrieval.
- Mudanças de finalização: atualizados status, sequência, resumo global e próximo `CURRENT.md`; nenhum runtime adicional foi alterado.
- Problema resolvido: ciclo da implementação 006 encerrado com evidência reproduzível.
- Pendências: embeddings reais, persistência vetorial, integração com API/worker e avaliação semântica permanecem futuras.
- Verificação: 11 testes passaram, `compileall` passou e o hook validou 4 arquivos de handoff.
- Próxima etapa: `007-respostas-com-citacoes`.
