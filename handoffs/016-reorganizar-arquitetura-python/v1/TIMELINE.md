## v1 — Composition root do serviço Python

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: `rastro-ai/src/rastro_ai/bootstrap/container.py`, `indexing.py`, `retrieval.py` e `tests/test_runtime_vector_store.py`.
- Mudanças: containers explícitos para indexação e retrieval; remoção de instâncias globais das fachadas; validação de backend deslocada para a construção do container; cobertura de importação segura.
- Problema resolvido: import de retrieval dependia de configuração externa e construía recursos antes do uso.
- Verificação prevista: unittest, evaluation `20/20`, import sem configuração, compilação e hook estrutural.
- Pendências: nenhuma nesta etapa aplicada; as próximas etapas dependem da finalização de `016`.

## v1 — Verificação concluída

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Verificação: 36 testes, evaluation `20/20`, importação segura, compilação, `git diff --check` e hook estrutural aprovados.
- Pendências: nenhuma dentro da etapa; não houve smoke externo, deploy ou migração.
