# 013/v1 — Debug composto no VS Code

- Versão-base: nova implementação; `012` estava `verified` e foi preservada.
- Data: 2026-10-24 -03:00 | Status: `applied`.
- Aplicações reais conferidas: `/home/dev/dev/ia/rastro-ai/.gitignore`, `/home/dev/dev/ia/rastro-ai/rastro-api/package.json`, `/home/dev/dev/ia/rastro-ai/rastro-api/src/main.ts`, `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/service.py`, `/home/dev/dev/ia/rastro-ai/docker-compose.yml`.
- Estado encontrado: o Python executa por `python -m rastro_ai.service`, a API usa `npm run start:dev`, não havia `.vscode/launch.json` nem script de debug NestJS.

## O que foi feito

- Foi criado `/home/dev/dev/ia/rastro-ai/.vscode/launch.json` com as configurações `Python: AI service`, `API: NestJS` e o compound `Debug: API + Python`.
- Foi inserido o script `start:debug` em `rastro-api/package.json`, ancorado na chave `scripts`, usando `nest start --debug --watch`.
- Foram adicionadas exceções específicas no `/home/dev/dev/ia/rastro-ai/.gitignore` para versionar a configuração do VS Code sem liberar outros arquivos do diretório.
- O debug Python usa `PYTHONPATH=src`, `127.0.0.1:8000` e backend em memória; a API usa `AI_INDEXING_URL=http://127.0.0.1:8000/index` para atravessar a chamada local.
- A alteração resolve a ausência de uma forma reproduzível de iniciar os dois processos e posicionar breakpoints no upload, no cliente HTTP, no handler Python e na indexação.
- JSON e package manifest não suportam JSDoc; a exceção foi registrada aqui, com as âncoras estruturais e a decisão documentadas.

## O que muda na aplicação

- No VS Code, `Debug: API + Python` inicia os dois processos e encerra ambos ao parar a sessão; breakpoints podem ser usados nos arquivos reais das duas aplicações.
- O runtime de produção, o `docker-compose.yml`, as portas publicadas pelo Compose e o backend PostgreSQL não foram alterados.
- O perfil padrão usa armazenamento em memória para evitar exigir banco ou credencial durante o debug; para depurar pgvector, os valores de ambiente podem ser ajustados localmente.
- O inspector da NestJS é habilitado somente pelo novo script de desenvolvimento; nenhum inspector é ativado em `start` ou `start:prod`.

## Jornada da aplicação nesta versão

Antes, era necessário iniciar a API e o serviço Python separadamente e configurar manualmente o endereço do indexador. Agora, a pessoa seleciona `Debug: API + Python`, envia um upload e acompanha o caminho API → POST `/index` → `index_document_in_store`. O resultado continua sendo o documento `ready` ou `failed`, sujeito às mesmas regras funcionais e ao backend escolhido.

## Como usar e validar a aplicação nesta versão

1. Instale as extensões Python e Python Debugger, caso ainda não estejam instaladas.
2. No VS Code, abra `/home/dev/dev/ia/rastro-ai`, selecione `Debug: API + Python` na aba Run and Debug e inicie com `F5`.
3. Coloque breakpoints em `rastro-api/src/modules/documents/application/upload-document.use-case.ts`, `rastro-api/src/modules/documents/infrastructure/http-document-indexer.ts`, `rastro-ai/src/rastro_ai/service.py` ou `rastro-ai/src/rastro_ai/indexing.py`.
4. Para o PostgreSQL, execute separadamente `docker compose up vector-db` e altere localmente as variáveis do perfil Python; isso não é necessário para validar o perfil padrão em memória.

## Cobertura por comportamento

- Breakpoint no serviço Python: configuração `debugpy` inicia o módulo real `rastro_ai.service` com `PYTHONPATH` explícito; evidência adicional: `python -m compileall -q src tests`.
- Breakpoint na API: script `start:debug` habilita o inspector do NestJS com watch e source maps; evidência adicional: `npm run build` e validação do manifest.
- Fluxo API → Python: `AI_INDEXING_URL` aponta para `127.0.0.1:8000/index`; smoke manual com upload multipart é recomendado quando as dependências estiverem instaladas.
- Não houve mudança de regra de negócio, contrato HTTP ou persistência; testes funcionais existentes permanecem a evidência dessas áreas.

## Instruções de validação

- `python3 -m json.tool .vscode/launch.json`: esperado, JSON formatado sem erro.
- `node -e "const p=require('./rastro-api/package.json'); if (p.scripts['start:debug'] !== 'nest start --debug --watch') process.exit(1); console.log('debug-script-ok')"`: esperado, `debug-script-ok`.
- `cd rastro-api && npm run build`: esperado, compilação NestJS concluída; nesta rodada ficou pendente porque `rastro-api/node_modules/.bin/nest` não está disponível.
- `cd rastro-ai && PYTHONPATH=src python3 -m compileall -q src tests`: esperado, conclusão sem saída e código `0`.
- Ação manual no VS Code: executar `Debug: API + Python`; esperado, dois processos iniciados, API em `http://127.0.0.1:3000/api/v1/health` e Python em `http://127.0.0.1:8000/health`, com breakpoints atingíveis.
- `git diff --check`: esperado, nenhuma falha de whitespace.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/013-configurar-debug-python-api-vscode/README.md handoffs/013-configurar-debug-python-api-vscode/TIMELINE.md handoffs/013-configurar-debug-python-api-vscode/v1/README.md handoffs/013-configurar-debug-python-api-vscode/v1/TIMELINE.md`: executado com sucesso, quatro arquivos válidos.
