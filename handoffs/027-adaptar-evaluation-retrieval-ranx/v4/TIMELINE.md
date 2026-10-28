# Timeline — 027/v4 explicação simples das métricas

## 2026-10-27 23:15 -03:00 — aplicação da v4

- Status: `applied`.
- Arquivos reais conferidos: comentários das métricas, invariantes, adapter e README do retrieval.
- Mudanças: comentários reescritos com perguntas, interpretação de `0`/`1` e limites; tabela explicativa adicionada.
- Pendência: repetir compilação, suíte controlada e hook estrutural.

## 2026-10-27 23:20 -03:00 — exemplos de interpretação

- Status: `applied`.
- Mudanças: exemplos de listas, posições, ruído, isolamento e abstention adicionados aos comentários e README.
- Verificação pendente: repetir compilação, suíte controlada, diff e hook estrutural.

## 2026-10-27 23:35 -03:00 — evidência da v4

- Status: `applied`.
- Verificação: `compileall`, `git diff --check` e `./rastro-ai/evals/retrieval/run_evaluation.sh test` concluídos; 6 testes terminaram com `OK`.
- Limite: a v4 altera comentários e documentação; o fluxo real contra PGVector continua fora desta rodada.
