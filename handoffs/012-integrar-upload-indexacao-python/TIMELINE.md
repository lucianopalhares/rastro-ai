# Linha do tempo — 012 Integração do upload com a indexação Python

## v1 — Abertura da tarefa

- Data/hora: 2026-10-24 -03:00 | Status: `proposed`.
- Arquivos reais conferidos: `rastro-api/src/modules/documents`, `rastro-ai/src/rastro_ai/document_indexing`, `rastro-ai/src/rastro_ai/indexing.py` e `rastro-ai/src/rastro_ai/retrieval.py`.
- Mudanças aplicadas: criação dos registros da implementação e ativação de `CURRENT.md` para `012`.
- Problema registrado: o upload salva o arquivo e retorna `pending`, mas ainda não dispara a indexação Python.
- Escopo inicial: contrato API/Python, processamento, transições de estado, idempotência, retry, testes e smoke ponta a ponta.
- Pendências: definir transporte e execução do worker sem copiar código para os handoffs.
- Verificação: estrutura dos handoffs e consistência dos arquivos de controle; nenhuma alteração de runtime nesta rodada.

## v1 — Implementação aplicada

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais alterados: gateway e caso de uso de upload da API, módulo de documentos, serviço HTTP Python, fachada de indexação, Compose e testes.
- Mudanças aplicadas: POST JSON API → Python, endpoint `/health`/`/index`, persistência dos chunks e estados `processing`, `ready` e `failed`.
- Problema resolvido: o upload deixou de permanecer somente em `pending` e passou a disparar a indexação Python.
- Verificação: API com 10 testes e build aprovados; Python com 23 testes e compilação aprovados; smoke HTTP, Compose e diff check aprovados.
- Pendências: retry, idempotência explícita, processamento assíncrono e validação com pgvector real permanecem para evolução posterior.

## v2 — Repository externo e modelo Document

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais alterados: contrato/gateway API, serviço Python, ports, repository OpenAI, store PostgreSQL, Dockerfile, Compose, README e testes.
- Mudanças aplicadas: `Document.toJSON()` enviado em `{ document }`; embeddings externos em lote com `text-embedding-3-small`, `dimensions=384`; porta externa `18473`.
- Problema resolvido: o payload não reutilizava o modelo existente e a persistência dependia de provider local/memória.
- Verificação: testes API/Python, build da imagem sem CUDA, schema/Compose e hook aprovados.
- Pendência: ausência de `OPENAI_API_KEY` impede smoke externo e confirmação de uma linha real em `document_chunks` nesta sessão.

## v3 — Chunking estrutural por tokens

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais alterados: serviço de chunking, caso de uso, fachadas, testes, README e handoff v3.
- Mudanças aplicadas: cortes preferenciais em parágrafos/títulos Markdown, orçamento aproximado de 500 tokens e overlap de 60 tokens.
- Problema resolvido: janela fixa de caracteres podia fragmentar contexto semântico.
- Verificação: testes e hook serão executados após a alteração; API, embeddings e banco permanecem inalterados.
- Pendência: avaliar recall/precisão com dataset real depois da validação externa.

## v4 — Tokenizer real no chunking

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais alterados: dependências, Dockerfile, serviço de chunking, testes, README e handoff v4.
- Mudanças aplicadas: `tiktoken` calcula tokens reais de `text-embedding-3-small`, mantendo cortes estruturais e offsets.
- Problema resolvido: a estimativa por palavras podia divergir da tokenização do modelo.
- Verificação: testes, compilação, build e hook serão executados após a aplicação.
- Pendência: nenhuma mudança na integração externa; não repetir smoke de OpenAI/pgvector para alteração isolada de tokenizer.

## v5 — Timeout externo

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Arquivo real alterado: `docker-compose.yml`.
- Mudança aplicada: timeout da API para o indexador configurado em `60000ms` no Compose.
- Problema resolvido: smoke longo excedeu o timeout padrão de 10 segundos e terminou como `failed`.
- Verificação: upload longo retornou `ready`; consulta confirmou 3 chunks e embeddings com dimensão `384`.

## v6 — Separação modular

- Data/hora: 2026-10-25 -03:00 | Status: `applied`.
- Arquivos reais alterados: estrutura de `rastro-ai/src/rastro_ai`, imports de produção, README e handoff v6.
- Mudanças aplicadas: limites por capacidade para documentos, ingestão, chunking, embeddings e busca semântica; compatibilidade antiga preservada.
- Problema resolvido: responsabilidades distintas estavam concentradas em `document_indexing`.
- Verificação: import smoke, 26 testes, compilação, build e hook aprovados.
- Pendência: retirar wrappers legados após migração dos consumidores.

## Finalização — 012 verificada

- Data/hora: 2026-10-25 -03:00 | Status: `verified`.
- Versões conferidas: `v1` a `v6`, todas aplicadas e preservadas.
- Arquivos reais conferidos: API de upload/indexação, serviço Python, módulos de documentos, ingestão, chunking, embeddings, busca semântica, Compose, Dockerfile, dependências, testes e configurações de ambiente.
- Verificação: upload curto e longo em Compose retornaram `ready`; o banco registrou respectivamente 1 e 3 chunks com embeddings não vazios e dimensão `384`; testes API/Python, compilação, build, imports modulares, configuração Compose, diff e hook estrito passaram.
- Problema resolvido: confirmação de que o arquivo enviado pela API é indexado pelo Python e gravado no banco vetorial com chunks e embeddings.
- Pendências: retry, idempotência explícita, processamento assíncrono e remoção dos wrappers legados.
- Commit: commit de finalização criado nesta rodada; o identificador final é informado na entrega.
