# 013/v2 — Debug Docker com attach do VS Code

- Versão-base: `v1` aplicada; estado real reconciliado em 2026-10-24 -03:00.
- Status: `applied`; aplicações: raiz, `rastro-api` e `rastro-ai`.
- Arquivos conferidos: `docker-compose.yml`, `.vscode/launch.json`, `rastro-api/package.json`, `rastro-api/Dockerfile.dev`, `rastro-ai/Dockerfile`, `rastro-ai/README.md`; não havia README da API.
- Estado encontrado: v1 iniciava processos no host, mas o fluxo oficial usa Compose; não havia portas de inspector nem `debugpy` na imagem Python.

## O que foi feito

- `docker-compose.yml`: API inicia com `npm run start:debug` e publica `9229`; Python usa `Dockerfile.dev`, inicia `debugpy` em `5678` e publica essa porta.
- `rastro-api/package.json`: `start:debug` escuta o inspector em `0.0.0.0:9229`.
- `rastro-ai/Dockerfile.dev`: criado para instalar `debugpy` sem alterar a imagem de produção `Dockerfile`; o comando desativa módulos congelados para preservar breakpoints Python.
- `.vscode/launch.json`: adicionados os perfis Docker e o compound recomendado `Debug Docker: API + Python`, com mapeamentos host/container.
- `rastro-ai/README.md` e `rastro-api/README.md`: adicionados comandos de build, subida do Compose, attach do VS Code e health checks; o README da API foi criado porque estava ausente.

## O que muda na aplicação

- O debug recomendado usa os containers reais: API em `3039`, indexador em `18473`, inspector Node em `9229` e `debugpy` em `5678`.
- O container Python de desenvolvimento usa PostgreSQL e embeddings conforme o Compose; a produção continua usando `rastro-ai/Dockerfile` sem `debugpy`.
- O VS Code não inicia o Compose automaticamente: primeiro execute `docker compose build` e `docker compose up`; depois faça attach.
- O comportamento de negócio, contratos HTTP e persistência não foram alterados; somente a superfície de desenvolvimento foi ampliada.

## Jornada da aplicação nesta versão

Antes, o perfil principal iniciava processos no host e podia divergir do ambiente Docker. Agora, as imagens de desenvolvimento são construídas pelo Compose, os serviços iniciam com seus inspectores e o VS Code conecta os breakpoints aos arquivos locais. Um upload pode ser acompanhado da API NestJS até o handler Python e a indexação PostgreSQL.

## Como usar e validar a aplicação nesta versão

1. Defina `OPENAI_API_KEY` no `.env` se for executar upload com embeddings.
2. Na raiz, execute `docker compose build api ai-indexer`.
3. Na raiz, execute `docker compose up api ai-indexer vector-db`.
4. Abra a raiz no VS Code, selecione `Debug Docker: API + Python` e pressione `F5`.
5. Coloque breakpoints nos arquivos reais da API e IA e valide `/api/v1/health`, `/health` ou um upload.

## Cobertura por comportamento

- Inspector da API: `start:debug`, porta `9229` e attach Node; a integração é validada pelo build Docker.
- Breakpoints Python: `Dockerfile.dev` instala `debugpy`, o Compose escuta `5678` e o launch usa `/app/src` como remote root.
- Fluxo entre serviços: Compose mantém `AI_INDEXING_URL=http://ai-indexer:8000/index`; health checks e upload manual cobrem a comunicação HTTP.
- Documentação de uso: READMEs da API e IA registram os mesmos comandos copiáveis; não havia README da API antes desta rodada.

## Instruções de validação

- `python3 -m json.tool .vscode/launch.json`: esperado, JSON válido.
- `docker compose config`: esperado, configuração resolvida com `api` em `9229` e `ai-indexer` em `5678`.
- `docker compose build api ai-indexer`: aprovado; imagens construídas, incluindo `debugpy` e `-Xfrozen_modules=off`.
- `docker compose up -d vector-db ai-indexer api`: aprovado; containers iniciados com portas `3039`, `18473`, `9229` e `5678` disponíveis.
- `curl --fail http://127.0.0.1:3039/api/v1/health`: aprovado, HTTP `200`.
- `curl --fail http://127.0.0.1:18473/health`: aprovado, HTTP `200`.
- `curl --fail http://127.0.0.1:9229/json/list`: aprovado, inspector Node respondeu com alvo ativo.
- Ação manual no VS Code: executar `Debug Docker: API + Python`; pendente, requer sessão gráfica para confirmar attach e breakpoints.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v2/README.md handoffs/013-configurar-debug-python-api-vscode/v2/TIMELINE.md`: aprovado, quatro arquivos válidos.
