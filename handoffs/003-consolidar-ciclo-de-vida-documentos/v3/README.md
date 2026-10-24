# v3 — Correção da aplicação parcial

- Versão-base: `v2`; arquivos reais foram relidos após os erros de compilação.
- Data: 2026-10-23 | Status: `proposed`.
- Arquivos conferidos: domínio, caso de uso e controller em `rastro-api`.
- Já aplicado: `create-document.use-case.ts` está correto e não deve ser repetido.
- Divergências: domínio ainda sem `projectId`; DTO sem `content` após a aplicação parcial.
- Pendências: aplicar apenas os dois handoffs desta versão.
- Ordem: domínio → controller → build e testes.
- Verificação: hook, compilação, Jest e POST com payload completo.
