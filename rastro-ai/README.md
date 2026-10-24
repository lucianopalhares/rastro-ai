# Rastro AI — Indexação e retrieval de documentos

Esta aplicação extrai documentos UTF-8 `.md` e `.txt`, normaliza o conteúdo, gera chunks determinísticos com offsets e oferece retrieval local filtrado por projeto.

## O que foi implementado

O módulo `rastro_ai.document_indexing` usa uma organização DDD modular:

- `domain/`: entidade `DocumentChunk` e serviço puro de normalização/chunking;
- `application/`: portas `TextExtractor`/`VectorStore` e casos de uso de indexação/retrieval;
- `infrastructure/`: adaptador `Utf8FileTextExtractor` para arquivos locais;
- `infrastructure/retrieval/`: store vetorial determinístico em memória;
- `rastro_ai/indexing.py` e `rastro_ai/retrieval.py`: fachadas públicas de indexação e consulta.

O caso de uso não conhece o sistema de arquivos diretamente: recebe um extrator pela porta da aplicação. Isso permite trocar a origem futura por API, object storage ou worker sem alterar o domínio.

## O que muda na aplicação

- A lógica de negócio deixa de ficar concentrada em um único arquivo.
- O chunking continua com o mesmo comportamento: tamanho padrão de 800 caracteres, sobreposição de 120 e offsets sobre o texto normalizado.
- Chunks podem carregar `project_id`; `retrieve_chunks` filtra o projeto antes de ordenar por similaridade de cosseno sobre frequência de termos.
- Apenas `.md` e `.txt` em UTF-8 são aceitos; arquivos vazios ou formatos não suportados falham.
- O retrieval atual é síncrono, local e lexical; a aplicação ainda não inicia worker assíncrono, gera embeddings de modelo, persiste chunks ou usa PostgreSQL/pgvector.

## Como testar

Na raiz desta aplicação (`rastro-ai/`), execute:

```bash
python3 -m unittest discover -s tests -v
```

Resultado esperado: 11 testes aprovados.

Para verificar a compilação:

```bash
python3 -m compileall -q src tests
```

Para validar manualmente o caso de uso, importe `IndexDocumentUseCase`, injete `Utf8FileTextExtractor` e execute `execute(document_id, path)`. A resposta é uma tupla de `DocumentChunk` com `document_id`, `index`, `content`, `start_offset` e `end_offset`.

O próximo passo é conectar o retrieval ao processamento assíncrono e, posteriormente, avaliar embeddings reais e persistência vetorial.
