# Timeline — 013/v7

## v7 — 2026-10-24 -03:00

- Status: `applied`.
- Arquivos reais conferidos: controller, README da API, fixture e logs do container.
- Mudança aplicada: comando corrigido para usar `file=@$PWD/...`; controller restaurado ao binding padrão.
- Problema resolvido: caminho enviado como texto causava `A file is required`.
- Verificação: rebuild da API e curl corrigido executados com sucesso; resposta HTTP `200` e `status: ready`.
