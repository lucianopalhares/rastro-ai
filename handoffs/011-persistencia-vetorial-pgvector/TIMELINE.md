# Linha do tempo — 011 Persistência vetorial com pgvector

## v1 — Aplicação do backend persistente

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: Compose, schema, configuração Python, portas, retrieval, embeddings, README e testes.
- Mudanças aplicadas: serviço `vector-db` com volume, schema `vector(384)`, provider Sentence Transformers, store PostgreSQL, seleção por ambiente e testes unitários.
- Problema resolvido: retrieval persistente e semântico disponível sem remover o backend de memória.
- Verificação: compilação, suíte Python e `docker compose config`; integração real com banco ainda pendente.
- Pendências: iniciar manualmente o container, validar schema e executar fluxo real com dependências instaladas.

## v1 — Verificações locais

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Resultado: 21 testes Python aprovados, compilação aprovada, `docker compose config` aprovado e `git diff --check` sem erros.
- Limite: container pgvector não foi iniciado automaticamente; schema e persistência real permanecem pendentes de validação manual.

## Finalização — v1 verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Verificação real: container saudável em `localhost:55432`, extensão `vector`, tabela, chave, índices e adapter real aprovados.
- Verificação complementar: 21 testes Python, compilação, `docker compose config`, `git diff --check` e hook estrutural aprovados.
- Resultado: implementação 011 encerrada; `CURRENT.md` avança para `009`, que permanece proposto/standby.
- Pendências: integração automática do upload com worker de indexação e geração por LLM permanecem futuras.
- Commit: `e8dad04` — `Finalizar persistência vetorial com pgvector`.
- Verificação do commit: lista explícita de 16 arquivos da tarefa; alterações não relacionadas permaneceram fora do índice.
