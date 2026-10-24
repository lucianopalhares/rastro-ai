# v2 — Reconciliação após reorganização das aplicações

- Versão-base: `v1`; a aplicação real foi conferida novamente após a API ser movida para `rastro-api`.
- Data: 2026-10-23 | Status: `proposed`.
- Arquivos conferidos: domínio `Document`, caso de uso, controller e bootstrap em `rastro-api`.
- Já aplicado: nenhum trecho desta implementação; `v1` permanece preservada como histórico.
- Divergência resolvida: os caminhos de `v1` apontavam para `rastro-ai`, que agora é o destino da IA.
- Pendências: aplicar os quatro handoffs desta versão e executar build, testes e validação HTTP.
- Ordem: domínio → caso de uso → controller → teste de domínio.
- Verificação: hook estrutural, Jest e compilação TypeScript.
