# 025/v1 — Tokens e custos de embeddings no Langfuse

- Versão: `v1`; versão-base: implementação `024` verificada; data: 2026-10-26 -03:00; status: `applied`.
- Estado-base: `embedding-generation` registra modelo apenas em input/metadata; painel mostra status, mas não usage nem cost.
- Escopo autorizado: adicionar modelo top-level, contagem local de tokens, `usage_details`, custo inferido e custo direto opcional.
- Invariantes: contagem não envia texto ao Langfuse; falhas de observabilidade não interrompem embeddings; implementação 024 permanece preservada.

## O que foi feito

- `observe_operation` agora aceita `model` no nível da observação, necessário para matching de modelos do Langfuse.
- A contagem local usa `tiktoken` e envia `usage_details` para embeddings sem enviar o texto.
- `LANGFUSE_EMBEDDING_INPUT_COST_PER_TOKEN` permite custo direto quando o preço não estiver no Langfuse; vazio mantém custo inferido.
- A rodada resolve o trace sem tokens/custo, mantendo custo inferido como padrão e sem hardcode de preço do provedor.

## O que muda na aplicação

- O painel poderá mostrar tokens de entrada e custo inferido para `text-embedding-3-small` após o modelo/preço estar configurado no Langfuse.
- Quando a variável de custo direto estiver preenchida, o trace enviará o custo calculado por token; quando vazia, o Langfuse inferirá o custo.
- Modelos sem tokenizer conhecido não interromperão a indexação, mas poderão ficar sem usage/cost até configuração explícita.
- Fora do escopo: custo de geração de respostas, alteração de preços no Langfuse, conteúdo textual e embeddings no trace.

## Jornada da aplicação nesta versão

Antes, a observação de embedding mostrava modelo, dimensão e quantidade de itens, mas não tokens nem custo. Depois, a mesma chamada enviará uso tokenizado e permitirá ao painel calcular o custo por modelo, sem alterar a indexação.

## Como usar e validar a aplicação nesta versão

Configure o modelo `text-embedding-3-small` em Project Settings > Models no Langfuse, ou defina `LANGFUSE_EMBEDDING_INPUT_COST_PER_TOKEN` no `.env` para custo direto, reinicie o `ai-indexer` e repita o cURL de indexação. Abra `embedding-generation` e confira usage e cost.

## Cobertura por comportamento

- Modelo top-level e usage: teste unitário com observation fake e execução sem rede.
- Custo direto: teste unitário com variável de ambiente e cálculo por token.
- Isolamento: testes existentes de modo desligado e falha de telemetria permanecem aprovados.
- Integração: Compose/health e cURL real devem confirmar os campos no painel; preço inferido depende do modelo configurado manualmente.

## Instruções de validação

- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml config`: esperado, composição válida.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml build ai-indexer`: esperado, imagem com dependências atuais.
- `docker compose -f docker-compose.yml -f docker-compose.langfuse.yml run --rm --no-deps -v "$PWD/rastro-ai/tests:/app/tests:ro" ai-indexer python -m unittest -q tests.test_observability tests.test_openai_embedding_repository`: esperado, testes de tracing e embeddings aprovados.
- `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/025-tokens-custos-embeddings-langfuse/README.md handoffs/025-tokens-custos-embeddings-langfuse/TIMELINE.md handoffs/025-tokens-custos-embeddings-langfuse/v1/README.md handoffs/025-tokens-custos-embeddings-langfuse/v1/TIMELINE.md`: esperado, handoffs válidos.
- `curl --fail-with-body --request POST --url http://127.0.0.1:18473/index --header 'content-type: application/json' --data '{"document":{"id":"debug-langfuse-cost-001","projectId":"debug-project","name":"langfuse-cost.md","content":"Documento para validar tokens e custos."}}'`: esperado, HTTP 200 e observation `embedding-generation` com usage/cost no painel.
- Resultado observado: HTTP 200, `chunks: 1`, backend PostgreSQL e health do indexador aprovado após recriação do container; tokens aparecem no trace, mas custo ainda não foi confirmado e permanece pendente a validação de matching/preço ou custo direto.
