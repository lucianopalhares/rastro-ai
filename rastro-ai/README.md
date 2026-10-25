# Rastro AI — Indexação, retrieval e respostas fundamentadas

Esta aplicação extrai documentos UTF-8 `.md` e `.txt`, normaliza o conteúdo, gera chunks determinísticos com offsets, oferece retrieval local filtrado por projeto e responde de forma extrativa com citações.

## O que foi implementado

O módulo `rastro_ai.document_indexing` usa uma organização DDD modular:

- `domain/`: entidade `DocumentChunk` e serviço puro de normalização/chunking;
- `application/`: portas `TextExtractor`/`VectorStore` e casos de uso de indexação/retrieval;
- `infrastructure/`: adaptador `Utf8FileTextExtractor` para arquivos locais;
- `infrastructure/retrieval/`: store vetorial determinístico em memória;
- `infrastructure/retrieval/postgres_vector_store.py`: store persistente compatível com pgvector/Supabase;
- `infrastructure/embeddings/`: repository agnóstico e adaptador OpenAI para embeddings externos;
- `application/use_cases/answer_question.py`: resposta extrativa e citações verificáveis;
- `rastro_ai/indexing.py` e `rastro_ai/retrieval.py`: fachadas públicas de indexação e consulta.

O caso de uso não conhece o sistema de arquivos diretamente: recebe um extrator pela porta da aplicação. Isso permite trocar a origem futura por API, object storage ou worker sem alterar o domínio.

## Organização dos módulos

- `document_indexing/`: namespace canônico atual para entidades, portas, casos de uso e adapters;
- `bootstrap/`: composition root que monta os fluxos de indexação e retrieval;
- `indexing.py` e `retrieval.py`: fachadas públicas mantidas para o runtime e consumidores do pacote.

Os namespaces duplicados `chunking`, `documents`, `document_ingestion`, `embeddings` e `semantic_search` foram removidos nesta reorganização; consumidores externos devem migrar para as fachadas públicas ou para `document_indexing`.

## O que muda na aplicação

- A lógica de negócio deixa de ficar concentrada em um único arquivo.
- O chunking padrão agora privilegia títulos/parágrafos Markdown, usa `tiktoken` com orçamento real de 500 tokens, overlap de 60 tokens e preserva offsets; parâmetros legados `chunk_size`/`overlap` continuam disponíveis.
- Chunks podem carregar `project_id`; `search_relevant_chunks` filtra o projeto antes de ordenar por similaridade de cosseno sobre frequência de termos.
- `answer_question` reproduz somente os trechos recuperados, inclui documento, índice e offsets nas citações e declara ausência de evidência quando nada é encontrado.
- Apenas `.md` e `.txt` em UTF-8 são aceitos; arquivos vazios ou formatos não suportados falham.
- O backend de runtime é síncrono e exige `VECTOR_STORE_BACKEND=postgres`; chunks e embeddings do `text-embedding-3-small` são persistidos no PostgreSQL/pgvector e consultados semanticamente. O store em memória permanece somente em testes e evaluation determinística explícita.
- A integração automática do upload da API com a indexação, workers, geração por LLM e observabilidade continuam fora desta etapa.

## Como testar

Na raiz desta aplicação (`rastro-ai/`), execute:

```bash
python3 -m unittest discover -s tests -v
```

Resultado esperado: 18 testes aprovados.

## Debug com Docker e VS Code

Na raiz do repositório, construa as imagens de desenvolvimento:

```bash
docker compose build api ai-indexer
```

Inicie os serviços e o banco vetorial:

```bash
docker compose up api ai-indexer vector-db
```

Com os containers em execução, no VS Code abra a raiz do repositório, selecione `Debug Docker: API + Python` e pressione `F5`. O VS Code fará attach à API na porta `9229` e ao Python via `debugpy` na porta `5678`.

Breakpoints podem ser colocados em `src/rastro_ai/service.py`, `src/rastro_ai/indexing.py` e nos casos de uso chamados pelo endpoint `/index`. O serviço Python usa o backend PostgreSQL do Compose e requer `OPENAI_API_KEY` para gerar embeddings.

Para verificar a compilação:

```bash
python3 -m compileall -q src tests
```

Para validar manualmente o caso de uso, importe `ExtractAndChunkDocumentUseCase`, injete `Utf8FileTextExtractor` e execute `execute(document_id, path)`. A resposta é uma tupla de `DocumentChunk` com `document_id`, `index`, `content`, `start_offset` e `end_offset`. Para o fluxo completo, use `extract_chunk_and_persist_document(...)`, que também gera embeddings e persiste no PGVector.

Para usar o backend persistente, defina `OPENAI_API_KEY`, `DATABASE_URL=postgresql://rastro:rastro@localhost:55432/rastro`, `VECTOR_STORE_BACKEND=postgres`, `EMBEDDING_MODEL=text-embedding-3-small` e `EMBEDDING_DIMENSIONS=384`. O custo publicado do modelo é US$0,02 por 1 milhão de tokens; `SUPABASE_DB_URL` pode substituir `DATABASE_URL` sem mudar o schema ou as consultas.

O baseline determinístico de evaluation está versionado em `evals/`; geração por LLM, validação de citações geradas e persistência vetorial permanecem evoluções futuras.

## Evaluation

O diretório `evals/` contém 20 casos versionados e um baseline determinístico para retrieval, respostas, citações, ausência de evidência e isolamento por projeto. Execute `PYTHONPATH=src python3 -m evals.evaluate` para comparar o fluxo atual com `evals/baseline.json`; métricas semânticas por DeepEval, LLM-as-judge, API e observabilidade permanecem fora desta etapa.
