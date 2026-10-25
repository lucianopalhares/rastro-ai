# 015/v3 — Dependência LangChain nas imagens Docker

- Versão: `v3`; versão-base: `v2`; data: 2026-10-25 -03:00; status: `applied`.
- Aplicação: imagens `rastro-ai/Dockerfile` e `rastro-ai/Dockerfile.dev`; a versão-base foi comparada com os arquivos reais antes da alteração.
- Reconciliação: o `pyproject.toml` já declarava a dependência e o ambiente local passava, mas os Dockerfiles instalavam somente `psycopg`, `tiktoken` e, no desenvolvimento, `debugpy`.

## O que foi feito

- Alterados os comandos `pip install` de `rastro-ai/Dockerfile` e `rastro-ai/Dockerfile.dev` para incluir `langchain-text-splitters>=0.3,<1`.
- Mantidas as demais dependências e o comando `debugpy`; nenhuma alteração foi feita na API NestJS ou no fluxo do serviço.
- Corrigido o erro de inicialização observado no container: `ModuleNotFoundError: No module named 'langchain_text_splitters'`.

## O que muda na aplicação

- As imagens de produção e desenvolvimento passam a conter o pacote exigido pelo `LangChainTextChunker`.
- O `ai-indexer` poderá importar `rastro_ai` e iniciar o módulo `rastro_ai.service` após rebuild da imagem.
- O comportamento de chunking, contratos, embeddings e retrieval permanece inalterado; o custo do rebuild e a necessidade de reconstrução após mudança de dependência permanecem.
- Fora do escopo: deploy, migração, publicação externa e alteração do comando de debug.

## Jornada da aplicação nesta versão

Antes, a aplicação local funcionava porque a dependência estava instalada no ambiente virtual, mas o fluxo Docker falhava antes de iniciar o indexador. Agora, a mesma dependência é instalada nas imagens usadas pelo Compose, permitindo que o upload percorra API → `ai-indexer` sem falha de import. A próxima evolução é validar o smoke completo com o banco vetorial.

## Como usar e validar a aplicação nesta versão

Na raiz do projeto, reconstruir a imagem e iniciar o serviço com `docker compose build --no-cache ai-indexer && docker compose up -d ai-indexer`. O resultado observado foi container ativo e saudável, sem `ModuleNotFoundError`; o endpoint integrado completo continua fora desta rodada.

## Cobertura por comportamento

- Instalação de runtime: o Dockerfile é a evidência de configuração; build sem cache e import dentro do container passaram.
- Inicialização: o smoke manual via Compose confirmou `ai-indexer` ativo e saudável, sem `ModuleNotFoundError`.
- Regressão Python: os 30 testes e evaluation `20/20` da `v2` permanecem a evidência unitária/evaluation; nenhuma lógica Python foi alterada nesta `v3`.

## Instruções de validação

- `cd /home/dev/dev/ia/rastro-ai && docker compose build --no-cache ai-indexer`: esperado, build concluído instalando `langchain-text-splitters`.
- `cd /home/dev/dev/ia/rastro-ai && docker compose run --rm ai-indexer python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; import rastro_ai; print(RecursiveCharacterTextSplitter.__name__)"`: esperado, `RecursiveCharacterTextSplitter` impresso sem erro.
- `cd /home/dev/dev/ia/rastro-ai && docker compose up -d ai-indexer && docker compose ps ai-indexer`: observado, serviço ativo com healthcheck saudável e sem `ModuleNotFoundError`.
- `cd /home/dev/dev/ia/rastro-ai && REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/015-adaptar-chunking-para-langchain/README.md handoffs/015-adaptar-chunking-para-langchain/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v1/README.md handoffs/015-adaptar-chunking-para-langchain/v1/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v2/README.md handoffs/015-adaptar-chunking-para-langchain/v2/TIMELINE.md handoffs/015-adaptar-chunking-para-langchain/v3/README.md handoffs/015-adaptar-chunking-para-langchain/v3/TIMELINE.md`: esperado, handoffs válidos.
