# Timeline — 027/v6 documentação do fluxo e escolha de métricas

## 2026-10-28 00:15 -03:00 — aplicação da v6

- Status: `applied`.
- Arquivo real alterado: `docs/rag-evaluation-flow.md`.
- Mudanças: fluxo com setas, escolha por risco, ordem de aplicabilidade, regras de uso e interpretação por projeto, métricas adicionais possíveis e limites entre retriever, contexto e resposta.
- Verificação: conteúdo conferido com `rg`; `git diff --check` e hook estrutural serão repetidos antes da entrega.
- Limite: `docs/*` está no `.gitignore`; a documentação existe no workspace, mas não entra em commit automático.

## 2026-10-28 00:25 -03:00 — evidência da v6

- Status: `applied`.
- Verificação: `rg` confirmou seções, setas, árvore de decisão, ordem de aplicabilidade e regras por métrica; `git diff --check` passou.
- Hook: 14 arquivos de handoff válidos.
- Limite: não houve teste de runtime porque a v6 altera somente documentação.
