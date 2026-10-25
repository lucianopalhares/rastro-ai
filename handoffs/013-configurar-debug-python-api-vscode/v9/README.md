# 013/v9 — Consolidar o fluxo de validação no README raiz

- Versão-base: `v8` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicação: raiz.
- Arquivos conferidos: `rastro-api/README.md`, `rastro-ai/README.md`, `docker-compose.yml`, `.vscode/launch.json` e endpoints reais.
- Estado encontrado: as instruções estavam distribuídas entre os projetos; faltava um roteiro raiz com ordem, health checks e requests.

## O que foi feito

- Criado `/home/dev/dev/ia/rastro-ai/README.md` com build, subida ordenada dos serviços, portas, health checks, indexação direta Python, upload pela API, breakpoints e encerramento.
- Os comandos usam os caminhos e portas reais do Compose, incluindo `file=@$PWD/...` no multipart.
- O fluxo diferencia o teste isolado Python (`POST /index`) do fluxo integrado API → Python (`POST /api/v1/documents/upload`).

## O que muda na aplicação

- Não há mudança de runtime; a raiz passa a oferecer um roteiro único e copiável para validação local.
- Os READMEs específicos continuam válidos e passam a ser referências detalhadas por aplicação.

## Jornada da aplicação nesta versão

Antes, era necessário juntar instruções espalhadas entre API, IA e handoff. Agora, a pessoa inicia os serviços, verifica a API e o Python, testa primeiro a indexação isolada e depois o upload integrado, podendo conectar breakpoints entre as etapas.

## Como usar e validar a aplicação nesta versão

1. Na raiz, execute os comandos da seção `Fluxo local com Docker`.
2. Siga a seção `Verificações HTTP na ordem correta`.
3. Se necessário, conecte o VS Code pelo compound Docker antes de executar os requests.

## Cobertura por comportamento

- Ordem de inicialização: conferida contra `docker-compose.yml` e suas dependências de saúde.
- Contratos HTTP: requests `GET /health`, `POST /index` e `POST /api/v1/documents/upload` documentados com payloads reais.
- Debug: portas e mapeamentos conferidos contra `.vscode/launch.json`.
- Smoke/manual integrado: os health checks, a indexação Python e o upload API foram executados durante as versões anteriores; esta rodada consolida os comandos e não altera runtime.

## Instruções de validação

- `python3 -m json.tool .vscode/launch.json`: esperado, JSON válido.
- `docker compose config`: esperado, serviços e portas resolvidos.
- Executar sequencialmente os comandos HTTP da seção `Verificações HTTP na ordem correta`: esperado, health checks HTTP `200`, indexação Python HTTP `200` e upload API HTTP `200` com `status: ready` quando embeddings estiverem configurados.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v9/README.md handoffs/013-configurar-debug-python-api-vscode/v9/TIMELINE.md`: esperado, quatro arquivos válidos.
