# 024/v1 — Langfuse self-hosted e observabilidade da indexação

- Versão: `v1`; versão-base: implementação `023` verificada; data: 2026-10-26 -03:00; status: `verified`.
- Estado-base: Rastro AI indexa com LangChain/OpenAI/PGVector; Compose principal não possui Langfuse; `CURRENT.md` apontava `idle`.
- Escopo autorizado: adicionar stack Langfuse complementar, configuração de SDK e observações sanitizadas de indexação/embeddings.
- Invariantes: indexação continua funcionando sem Langfuse; chaves ficam no `.env`; conteúdo de documentos e chunks não entra nos traces.

## O que foi feito

- Criado `docker-compose.langfuse.yml` com Web, Worker, PostgreSQL, ClickHouse, Redis e MinIO; UI em `38917`, mídia em `38918` e console MinIO local em `38919`.
- Adicionada a dependência `langfuse>=5,<6` ao `pyproject.toml` e aos Dockerfiles; o boundary opcional registra duração, status, projeto, documento, quantidade de chunks, modelo e dimensão.
- Instrumentados indexação e geração de embeddings com payload sanitizado; falhas de telemetria não interrompem o runtime.
- Atualizados `.env.example`, `docker-compose.yml` e README raiz com operação, chaves e aviso de uso local.
- A rodada resolve a ausência de visibilidade da indexação sem acoplar o processamento documental à disponibilidade do Langfuse.

## O que muda na aplicação

- Com `LANGFUSE_ENABLED=true` e chaves configuradas, a indexação aparecerá no painel em `http://localhost:38917`.
- Com Langfuse desligado, o comportamento funcional e o tempo de inicialização do Rastro AI permanecem preservados.
- Os traces terão metadados sanitizados; conteúdo, embeddings completos e chaves secretas ficam fora do payload.
- O stack self-hosted adiciona consumo local de CPU, memória, armazenamento e múltiplos containers; não há mudança no contrato da API de documentos.
- Agentes, tools, LangGraph, prompts e avaliações ficam fora do escopo desta rodada.

## Jornada da aplicação nesta versão

Antes, a indexação só podia ser diagnosticada por logs e inspeção do PostgreSQL. Depois, uma indexação iniciada pelo upload ou pelo endpoint Python poderá ser acompanhada no Langfuse, incluindo a operação principal e as chamadas de embedding, sem expor o texto documental.

## Como usar e validar a aplicação nesta versão

Suba a aplicação com os dois arquivos Compose, crie uma organização/projeto no Langfuse pela UI, copie as chaves para o `.env`, habilite `LANGFUSE_ENABLED=true`, reinicie o `ai-indexer` e execute o cURL de indexação. O trace deverá aparecer no projeto configurado; com a flag desligada, o mesmo cURL deverá continuar respondendo normalmente.

## Cobertura por comportamento

- Modo desligado: testes unitários do boundary de observabilidade confirmam que nenhuma chamada é feita e a indexação permanece funcional.
- Sanitização: testes confirmam que apenas identificadores, contagens, modelo, dimensão e status são enviados.
- Compose: `docker compose config` valida a composição complementar e smoke confirma Web/Worker/health.
- Integração real: cURL de indexação mais verificação visual do trace no Langfuse; o resultado esperado é uma observação sem conteúdo textual dos documentos.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml config`: aprovado, composição válida com os seis serviços Langfuse.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml up -d langfuse-postgres langfuse-clickhouse langfuse-redis langfuse-minio langfuse-worker langfuse-web`: aprovado, serviços iniciados e dependências healthy.
- `curl --fail-with-body --max-time 10 http://127.0.0.1:38917/api/public/health`: aprovado, HTTP `200` e `{"status":"OK"...}`.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml build ai-indexer`: aprovado, imagem instalada com `langfuse-5.0.4`.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -v "$PWD/rastro-ai/tests:/app/tests:ro" ai-indexer python -m unittest -q tests.test_observability tests.test_indexing tests.test_openai_embedding_repository tests.test_postgres_vector_store tests.test_retrieval tests.test_service tests.test_langchain_pipeline tests.test_answers tests.test_runtime_vector_store`: aprovado, 36 testes.
- `curl --fail --silent http://127.0.0.1:18473/health`: aprovado, `{"status": "ok"}` após recriar o indexador.
- `curl --fail-with-body --request POST --url http://127.0.0.1:18473/index --header 'content-type: application/json' --data '{"document":{"id":"debug-langfuse-001","projectId":"debug-project","name":"langfuse.md","content":"Documento usado para validar a observabilidade da indexação."}}'`: esperado, HTTP `200` e trace correspondente no painel, sem conteúdo documental no input do trace.
- A suíte no Python do host não foi usada como evidência porque o host não possui as dependências LangChain; a suíte equivalente foi executada dentro da imagem construída.
- Trace autenticado confirmado pelo usuário no painel após criar projeto/chaves, habilitar `LANGFUSE_ENABLED=true` e repetir o cURL; o campo de custo permanece vazio por não haver usage/preço configurado.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/024-langfuse-observabilidade-indexacao/README.md handoffs/024-langfuse-observabilidade-indexacao/TIMELINE.md handoffs/024-langfuse-observabilidade-indexacao/v1/README.md handoffs/024-langfuse-observabilidade-indexacao/v1/TIMELINE.md`: esperado, handoffs válidos.
