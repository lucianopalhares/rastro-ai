## v2 — Nomenclatura semântica aplicada

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Arquivos reais: métodos de fachada, composition root, casos de uso, stores, adapter, serviço HTTP, testes, evaluation, README e arquitetura conferidos.
- Mudanças: nomes de persistência, busca, containers, casos de uso e stores substituídos por nomes orientados ao comportamento.
- Problema resolvido: `retrieval.index_chunks()` sugeria consulta, embora persistisse chunks, e os adapters não expressavam sua responsabilidade.
- Impacto: contrato HTTP e comportamento funcional preservados; imports externos dos nomes antigos deixam de funcionar.
- Verificação prevista: 36 testes, evaluation `20/20`, compilação, busca de referências e hook estrutural.

## v2 — Nomenclatura semântica verificada

- Data/hora: 2026-10-25 -03:00.
- Status: `verified`.
- Verificação: 36 testes, evaluation `20/20`, compilação, imports semânticos, ausência de referências ativas antigas e `git diff --check` aprovados.
- Pendências: imports externos dos nomes antigos precisam migrar; smoke HTTP/PGVector real não foi repetido nesta rodada.
