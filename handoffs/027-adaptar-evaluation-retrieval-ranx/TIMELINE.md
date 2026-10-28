# Timeline — 027 adaptar evaluation de retrieval para ranx

## 2026-10-27 21:00 -03:00 — criação da implementação

- Status: `proposed`.
- Arquivos reais conferidos: evaluator, métricas, testes, dependências e Dockerfiles.
- Decisão: adotar `ranx` para métricas clássicas e preservar regras específicas do produto.
- Pendência: aplicação e validação da v1.

## 2026-10-27 21:30 -03:00 — aplicação da v1

- Status: `applied`.
- Arquivos reais alterados: `rastro-ai/pyproject.toml`, Dockerfiles, adapter ranx, métricas, evaluator e READMEs de evaluation.
- Resultado: Recall, Precision, MRR e nDCG passaram a usar `ranx`; isolamento, score ordering e abstention permanecem próprios.
- Verificação: build do `ai-indexer`, compilação Python, sintaxe do script e suíte controlada aprovados.

## 2026-10-27 22:00 -03:00 — evidência da implementação

- Status: `applied`.
- Evidência: 6 testes controlados terminaram com `OK`; hook estrutural validou 4 arquivos; compilação, sintaxe e diff passaram.
- Limite: o fluxo real PGVector não foi executado; a finalização e o commit aguardam comando explícito.

## 2026-10-27 22:15 -03:00 — aplicação da v2

- Status: `applied`.
- Resultado: ranking e invariantes agora têm diretórios próprios; `metrics/__init__.py` mantém compatibilidade.
- Verificação pendente: repetir testes, diff e hook após a reorganização.

## 2026-10-27 22:30 -03:00 — evidência da v2

- Status: `applied`.
- Resultado: compilação, diff, hook e suíte controlada concluídos; 6 testes terminaram com `OK`.
- Limite: evaluation real PGVector não executada; implementação permanece ativa até finalização explícita.

## 2026-10-27 22:45 -03:00 — aplicação da v3

- Status: `applied`.
- Resultado: nomes internos agora distinguem explicitamente métricas de ranking e invariantes, sem sugerir reranking no runtime.
- Verificação pendente: repetir compilação, suíte controlada, diff e hook após o rename.

## 2026-10-27 23:00 -03:00 — evidência da v3

- Status: `applied`.
- Resultado: compilação, diff e suíte controlada concluídos; 6 testes terminaram com `OK`.
- Limite: evaluation real PGVector não executada; implementação permanece ativa até finalização explícita.

## 2026-10-27 23:15 -03:00 — aplicação da v4

- Status: `applied`.
- Resultado: comentários e README agora explicam cada métrica por pergunta, interpretação e limite, sem alterar runtime.
- Verificação pendente: repetir compilação, suíte controlada, diff e hook após a documentação.

## 2026-10-27 23:35 -03:00 — evidência da v4

- Status: `applied`.
- Resultado: compilação, diff e suíte controlada concluídos; 6 testes terminaram com `OK`.
- Limite: a v4 altera comentários e documentação; evaluation real PGVector não executada.

## 2026-10-27 23:55 -03:00 — aplicação da v5

- Status: `applied`.
- Resultado: `evaluate.py` agora separa explicitamente invariantes, ranking e agregação, preservando o contrato do relatório.
- Verificação: compilação, diff e suíte controlada concluídos; 6 testes terminaram com `OK`.
- Limite: evaluation real PGVector não executada; implementação permanece ativa até finalização explícita.

## 2026-10-28 00:15 -03:00 — aplicação da v6

- Status: `applied`.
- Resultado: `docs/rag-evaluation-flow.md` agora explica o fluxo por setas e que as métricas devem ser escolhidas conforme o projeto.
- Verificação: conteúdo conferido com `rg`; diff estrutural será repetido após o registro.
- Limite: o arquivo está sob `docs/*` no `.gitignore` e não entra em commit automático.

## 2026-10-28 00:45 -03:00 — aplicação da v7

- Status: `applied`.
- Resultado: `HitRate@k` e indicadores operacionais foram adicionados sem remover as métricas anteriores.
- Verificação: compilação, diff e suíte controlada concluídos; 7 testes terminaram com `OK`.
- Limite: evaluation real PGVector e thresholds de produção não executados; implementação permanece ativa até finalização explícita.

## 2026-10-28 01:15 -03:00 — aplicação da v8

- Status: `applied`.
- Resultado: o CLI agora oferece resumo, somente falhas e seleção por métrica/grupo, preservando o relatório completo.
- Verificação: shell, compilação, ajuda, diff e suíte controlada concluídos; 8 testes terminaram com `OK`.
- Limite: publicação Langfuse e evaluation real não executadas; implementação permanece ativa até finalização explícita.

## 2026-10-28 01:30 -03:00 — finalização da implementação

- Status: `verified`.
- Verificações: 8 testes `OK`, compilação, `bash -n`, `--help`, validação de conflito entre flags, `git diff --check` e hook estrutural com 18 arquivos.
- Resultado: ranx, separação de métricas, indicadores operacionais, filtros de saída e documentação foram conferidos nas aplicações reais.
- Limites: evaluation real contra PGVector, thresholds de qualidade e publicação no Langfuse não fazem parte da evidência executada.
- Controle: `CURRENT.md` voltou para `idle`; `SEQUENCE.md` registra a implementação como `verified`.
- Commit: será registrado após o stage explícito dos arquivos rastreados da tarefa; `docs/*` permanece ignorado pelo Git.

## 2026-10-28 01:35 -03:00 — commit da implementação

- Status: `verified`.
- Commit: `06f96d7` — `Implementa avaliação de retrieval com ranx`.
- Arquivos: aplicação, testes, dependências e handoffs da tarefa; `docs/rag-evaluation-flow.md` permaneceu fora por estar ignorado pelo Git.
- Verificação pós-commit: commit criado com lista explícita; `CURRENT.md` está `idle`.
