# v1 — Consolidação do ciclo de vida documental

- Versão-base: estado real da API; não há `v0` nem handoff anterior desta tarefa.
- Data: 2026-10-23 | Status: `proposed`.
- Arquivos conferidos: domínio `Document`, caso de uso de criação, controller e bootstrap da API.
- Já aplicado: nenhum trecho desta implementação; a implementação `002` é apenas dependência histórica.
- Divergências: o código atual usa somente `pending`/`ready` e não recebe `projectId`.
- Pendências: aplicar os quatro handoffs e confirmar testes; não inclui banco, upload ou IA.
- Ordem: domínio → caso de uso → controller → teste de domínio.
- Verificação: build, Jest e requisições HTTP com validação de escopo.
