# Rastro AI — Indexação de documentos

Esta aplicação contém a primeira capacidade de indexação do Rastro AI: extrai documentos UTF-8 `.md` e `.txt`, normaliza o conteúdo e gera chunks determinísticos com offsets.

## O que foi implementado

O módulo `rastro_ai.document_indexing` usa uma organização DDD modular:

- `domain/`: entidade `DocumentChunk` e serviço puro de normalização/chunking;
- `application/`: porta `TextExtractor` e caso de uso `IndexDocumentUseCase`;
- `infrastructure/`: adaptador `Utf8FileTextExtractor` para arquivos locais;
- `rastro_ai/indexing.py`: fachada de compatibilidade para `extract_text`, `chunk_text` e `index_document`.

O caso de uso não conhece o sistema de arquivos diretamente: recebe um extrator pela porta da aplicação. Isso permite trocar a origem futura por API, object storage ou worker sem alterar o domínio.

## O que muda na aplicação

- A lógica de negócio deixa de ficar concentrada em um único arquivo.
- O chunking continua com o mesmo comportamento: tamanho padrão de 800 caracteres, sobreposição de 120 e offsets sobre o texto normalizado.
- Apenas `.md` e `.txt` em UTF-8 são aceitos; arquivos vazios ou formatos não suportados falham.
- A aplicação ainda não inicia worker assíncrono, gera embeddings, persiste chunks ou usa PostgreSQL/pgvector.

## Como testar

Na raiz desta aplicação (`rastro-ai/`), execute:

```bash
python3 -m unittest discover -s tests -v
```

Resultado esperado: 7 testes aprovados.

Para verificar a compilação:

```bash
python3 -m compileall -q src tests
```

Para validar manualmente o caso de uso, importe `IndexDocumentUseCase`, injete `Utf8FileTextExtractor` e execute `execute(document_id, path)`. A resposta é uma tupla de `DocumentChunk` com `document_id`, `index`, `content`, `start_offset` e `end_offset`.

O próximo passo é conectar este caso de uso ao processamento assíncrono disparado pelo upload da API.
