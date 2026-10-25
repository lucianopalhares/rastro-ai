# 012/v5 — Timeout da chamada de embeddings

- Versão-base: `v4` aplicada; falha observada no smoke real em 2026-10-25.
- Status: `applied`; aplicação: `docker-compose.yml`.
- Estado encontrado: upload longo com embeddings externos ultrapassou o timeout API padrão de 10 segundos e terminou como `failed`.
- Decisão: configurar `AI_INDEXING_TIMEOUT_MS=60000` no serviço API, preservando o timeout de 10 segundos como padrão para outros ambientes.

## O que foi feito

Foi ampliado o timeout da integração no Compose para acomodar chamadas externas de embeddings sem fechar a conexão antes da resposta. Nenhum segredo ou dado persistente foi alterado.

## O que muda na aplicação

No Compose, a API aguardará até 60 segundos pela confirmação do indexador Python; o fluxo continua síncrono e falhas posteriores continuam resultando em `failed`. O smoke confirmou chunks e embeddings após a correção.

## Jornada da aplicação nesta versão

Antes, um documento longo podia ser marcado como falho quando a chamada externa demorava mais de 10 segundos. Agora, o Compose permite tempo suficiente para concluir a chamada e retornar `ready`, sem alterar o algoritmo de chunking ou o provider.

## Como usar e validar a aplicação nesta versão

Execute `docker compose up -d vector-db ai-indexer api`, envie um documento longo por `curl` ao endpoint de upload e consulte `document_chunks`; espere `ready`, múltiplos chunks e embeddings presentes.

## Cobertura por comportamento

- Timeout da integração: configuração de Compose revisada; smoke API → Python → OpenAI → PostgreSQL confirmou o fluxo integrado.
- Chunking e embeddings: testes unitários das versões anteriores permanecem válidos e não são repetidos nesta correção.
- Falha anterior: o timeout de 10 segundos foi reproduzido no smoke e registrado antes da correção.

## Instruções de validação

- `docker compose config`: esperado, API com `AI_INDEXING_TIMEOUT_MS=60000`.
- `docker compose up -d vector-db ai-indexer api`: esperado, três serviços saudáveis.
- Upload multipart de documento longo e consulta SQL em `document_chunks`: confirmado, `status: "ready"`, 3 chunks, conteúdo não vazio e `vector_dims(embedding)=384`.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/012-integrar-upload-indexacao-python/README.md handoffs/012-integrar-upload-indexacao-python/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v1/README.md handoffs/012-integrar-upload-indexacao-python/v1/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v2/README.md handoffs/012-integrar-upload-indexacao-python/v2/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v3/README.md handoffs/012-integrar-upload-indexacao-python/v3/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v4/README.md handoffs/012-integrar-upload-indexacao-python/v4/TIMELINE.md handoffs/012-integrar-upload-indexacao-python/v5/README.md handoffs/012-integrar-upload-indexacao-python/v5/TIMELINE.md`: esperado, 12 arquivos válidos.
