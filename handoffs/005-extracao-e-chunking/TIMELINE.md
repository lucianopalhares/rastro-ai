# Linha do tempo — 005 Extração e chunking

## v1 — Extração e chunking determinísticos

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: `rastro-ai/` vazio de código; `rastro-api` com upload de `.md`/`.txt` e fixture `meeting.md`.
- Mudanças: criado o pacote Python com normalização UTF-8, validação de extensão, chunks com sobreposição e offsets, além de cinco testes padrão.
- Problema resolvido: ausência de uma capacidade executável de extração e divisão antes da futura indexação assíncrona.
- Pendências: integrar worker/job, embeddings, armazenamento vetorial e métricas de evaluation nas próximas etapas.
- Verificação: `python3 -m unittest discover -s tests -v` passou com 5 testes; `pytest` não está instalado e não é necessário.

## Finalização — verificação da implementação

- Data/hora: 2026-10-24 18:28 -03:00 | Status: `verified`.
- Arquivos reais conferidos: pacote `rastro-ai`, testes unitários e README da aplicação.
- Mudanças de finalização: atualizados status, sequência e próximo `CURRENT.md`; nenhum runtime foi alterado.
- Problema resolvido: ciclo da implementação 005 encerrado com evidência reproduzível.
- Pendências: integração com worker, embeddings, vector store, evaluation e observabilidade permanecem nas próximas etapas.
- Verificação: 7 testes unitários passaram, `compileall` passou e o hook validou 8 arquivos.
- Próxima etapa: `006-retrieval-vetorial-minimo`.
- Commit: `a214430` — `Finalizar extração e chunking`.
