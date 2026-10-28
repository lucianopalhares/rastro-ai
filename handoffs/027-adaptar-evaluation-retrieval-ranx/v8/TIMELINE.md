# Timeline — 027/v8 modos de saída e seleção

## 2026-10-28 01:15 -03:00 — aplicação da v8

- Status: `applied`.
- Arquivos reais alterados: script, evaluator, report, testes e READMEs de retrieval/fluxo.
- Mudanças: `--summary`, `--only-failures`, `--metrics` por grupo ou nome, com invariantes sempre executadas.
- Verificação: shell (`bash -n`), compilação, ajuda, diff e suíte controlada; 8 testes terminaram com `OK`.
- Correção: montagem do report ajustada após teste inicial detectar ausência indevida de `failures` e `cases`.
- Limite: publicação Langfuse e evaluation real continuam fora da rodada; finalização aguarda comando explícito.
