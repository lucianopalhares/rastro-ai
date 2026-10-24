# Rastro AI — Indexação, retrieval e respostas fundamentadas

Esta aplicação extrai documentos UTF-8 `.md` e `.txt`, normaliza o conteúdo, gera chunks determinísticos com offsets, oferece retrieval local filtrado por projeto e responde de forma extrativa com citações.

## O que foi implementado

O módulo `rastro_ai.document_indexing` usa uma organização DDD modular:

- `domain/`: entidade `DocumentChunk` e serviço puro de normalização/chunking;
- `application/`: portas `TextExtractor`/`VectorStore` e casos de uso de indexação/retrieval;
- `infrastructure/`: adaptador `Utf8FileTextExtractor` para arquivos locais;
- `infrastructure/retrieval/`: store vetorial determinístico em memória;
- `infrastructure/retrieval/postgres_vector_store.py`: store persistente compatível com pgvector/Supabase;
- `infrastructure/embeddings/`: embeddings locais multilíngues para a busca semântica;
- `application/use_cases/answer_question.py`: resposta extrativa e citações verificáveis;
- `rastro_ai/indexing.py` e `rastro_ai/retrieval.py`: fachadas públicas de indexação e consulta.

O caso de uso não conhece o sistema de arquivos diretamente: recebe um extrator pela porta da aplicação. Isso permite trocar a origem futura por API, object storage ou worker sem alterar o domínio.

## O que muda na aplicação

- A lógica de negócio deixa de ficar concentrada em um único arquivo.
- O chunking continua com o mesmo comportamento: tamanho padrão de 800 caracteres, sobreposição de 120 e offsets sobre o texto normalizado.
- Chunks podem carregar `project_id`; `retrieve_chunks` filtra o projeto antes de ordenar por similaridade de cosseno sobre frequência de termos.
- `answer_question` reproduz somente os trechos recuperados, inclui documento, índice e offsets nas citações e declara ausência de evidência quando nada é encontrado.
- Apenas `.md` e `.txt` em UTF-8 são aceitos; arquivos vazios ou formatos não suportados falham.
- O backend padrão continua síncrono e em memória; com `VECTOR_STORE_BACKEND=postgres`, chunks e embeddings são persistidos no PostgreSQL/pgvector e consultados semanticamente.
- A integração automática do upload da API com a indexação, workers, geração por LLM e observabilidade continuam fora desta etapa.

## Como testar

Na raiz desta aplicação (`rastro-ai/`), execute:

```bash
python3 -m unittest discover -s tests -v
```

Resultado esperado: 18 testes aprovados.

Para verificar a compilação:

```bash
python3 -m compileall -q src tests
```

Para validar manualmente o caso de uso, importe `IndexDocumentUseCase`, injete `Utf8FileTextExtractor` e execute `execute(document_id, path)`. A resposta é uma tupla de `DocumentChunk` com `document_id`, `index`, `content`, `start_offset` e `end_offset`.

Para usar o backend persistente local, execute `docker compose up -d vector-db`, defina `DATABASE_URL=postgresql://rastro:rastro@localhost:55432/rastro` e `VECTOR_STORE_BACKEND=postgres`. O modelo padrão é baixado pelo Sentence Transformers na primeira execução. `SUPABASE_DB_URL` pode substituir `DATABASE_URL` sem mudar o schema ou as consultas; `VECTOR_DB_PORT` pode alterar a porta publicada.

O baseline determinístico de evaluation está versionado em `evals/`; geração por LLM, validação de citações geradas e persistência vetorial permanecem evoluções futuras.

## Evaluation

O diretório `evals/` contém 20 casos versionados e um baseline determinístico para retrieval, respostas, citações, ausência de evidência e isolamento por projeto. Execute `PYTHONPATH=src python3 -m evals.evaluate` para comparar o fluxo atual com `evals/baseline.json`; métricas semânticas por DeepEval, LLM-as-judge, API e observabilidade permanecem fora desta etapa.
