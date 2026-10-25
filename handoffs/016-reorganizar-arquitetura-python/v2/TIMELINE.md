## v2 — Duplicações removidas e verificação concluída

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Arquivos reais: aliases dos namespaces removidos, provider Sentence Transformer, fachadas públicas, README e imports internos conferidos.
- Mudanças: implementações duplicadas removidas; imports internos consolidados em `document_indexing`; documentação atualizada com o impacto de compatibilidade.
- Verificação: 36 testes, evaluation `20/20`, compilação e busca de referências residuais aprovados.
- Pendências: confirmar consumidores externos dos aliases antes do commit/finalização; não houve deploy ou alteração externa.

## v2 — Imports antigos rejeitados

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Verificação adicional: imports canônicos (`rastro_ai`, `indexing`, `retrieval`, `document_indexing` e `bootstrap`) carregaram; os seis imports removidos falharam com `ModuleNotFoundError`.
- Correção: diretórios vazios remanescentes foram removidos, pois estavam sendo tratados como namespace packages mesmo sem arquivos Python.
- Resultado: nenhum alias removido permanece importável no workspace atual.
