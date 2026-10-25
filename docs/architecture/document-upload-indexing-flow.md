# Fluxo de upload e indexação de documentos

Este documento descreve a sequência de chamadas iniciada pelo upload de um
arquivo Markdown na API e concluída na persistência dos chunks no PostgreSQL
com pgvector.

## Entrada

```bash
curl --fail-with-body --request POST \
  --url http://127.0.0.1:3039/api/v1/documents/upload \
  --header 'accept: application/json' \
  --form 'projectId=debug-project' \
  --form "file=@$PWD/rastro-api/test/fixtures/upload/meeting.md;type=text/markdown"
```

`127.0.0.1:3039` é a porta publicada pelo container da API, cujo processo
NestJS escuta na porta `3000`. O arquivo é recebido pelo Multer em memória; a
API envia o conteúdo textual para o indexador Python, além de salvar uma cópia
local no armazenamento configurado.

## Árvore completa de chamadas

```text
curl
└── POST /api/v1/documents/upload
    └── rastro-api:3000
        └── DocumentsController.upload()
            ├── FileInterceptor('file')
            │   └── Multer -> file.buffer
            │
            └── UploadDocumentUseCase.execute()
                ├── getSupportedExtension()
                │   └── valida .md ou .txt
                ├── LocalDocumentFileStorage.save()
                │   └── storage/documents/{documentId}.md
                ├── Document.create()
                ├── document.changeStatus('processing')
                ├── HttpDocumentIndexer.index()
                │   └── POST http://ai-indexer:8000/index
                │       └── body: { document: DocumentProperties }
                ├── document.changeStatus('ready' | 'failed')
                ├── DocumentRepository.save()
                │   └── InMemoryDocumentRepository.save()
                └── retorna o documento serializado
```

### Explicação simples da etapa da API

1. `DocumentsController.upload()` — recebe o arquivo e o identificador do projeto.
2. `FileInterceptor('file')` — retira o arquivo do formulário enviado pelo `curl`.
3. `UploadDocumentUseCase.execute()` — organiza e executa o processo de upload.
4. `getSupportedExtension()` — verifica se o arquivo é `.md` ou `.txt`.
5. `LocalDocumentFileStorage.save()` — salva uma cópia do arquivo no disco da API.
6. `Document.create()` — cria o documento dentro da aplicação.
7. `document.changeStatus('processing')` — marca que o documento começou a ser processado.
8. `HttpDocumentIndexer.index()` — envia o documento para o serviço Python.
9. `document.changeStatus('ready' | 'failed')` — marca sucesso ou falha no processamento.
10. `DocumentRepository.save()` — solicita que o documento seja guardado.
11. `InMemoryDocumentRepository.save()` — implementação atual que guarda o documento em memória.

## Chamadas no serviço Python

```text
IndexingRequestHandler.do_POST()
├── _read_payload()
├── _required_string(document, 'id')
├── _required_string(document, 'projectId')
├── _required_string(document, 'name')
├── _required_string(document, 'content')
├── tempfile.NamedTemporaryFile()
│
└── extract_chunk_and_persist_document()
    ├── extract_and_chunk_document()
    │   ├── bootstrap.build_indexing_container()
    │   │   ├── Utf8FileTextExtractor()
    │   │   ├── LangChainTextChunker()
    │   │   └── ExtractAndChunkDocumentUseCase(extractor, chunker)
    │   └── ExtractAndChunkDocumentUseCase.execute()
    │       ├── Utf8FileTextExtractor.extract()
    │       │   ├── lê UTF-8
    │       │   └── normalize_text()
    │       └── LangChainTextChunker.chunk()
    │           ├── normalize_text()
    │           ├── RecursiveCharacterTextSplitter(...)
    │           ├── splitter.create_documents(...)
    │           └── DocumentChunk(...)
    │
    └── persist_document_chunks()
        └── bootstrap.build_semantic_search_container()
            ├── valida VECTOR_STORE_BACKEND=postgres
            ├── OpenAIEmbeddingRepository.from_environment()
            ├── PostgresChunkVectorStore.from_environment(...)
            └── PostgresChunkVectorStore.upsert()
                ├── OpenAIEmbeddingRepository.embed()
                │   └── OpenAIEmbeddings.embed_documents()
                │       └── provider OpenAI /v1/embeddings
                ├── valida dimensão 384 e project_id
                ├── monta metadata do chunk
                ├── cria ID determinístico SHA-256
                └── PGVector.add_embeddings()
                    └── PostgreSQL + pgvector
```

### Explicação simples da etapa Python

1. `IndexingRequestHandler.do_POST()` — recebe o documento enviado pela API.
2. `_read_payload()` — lê os dados JSON da requisição.
3. `_required_string()` — verifica se cada informação obrigatória existe.
4. `tempfile.NamedTemporaryFile()` — cria um arquivo temporário para leitura.
5. `extract_chunk_and_persist_document()` — coordena a extração, a criação dos pedaços e a gravação dos vetores.
6. `extract_and_chunk_document()` — solicita ao composition root as dependências de extração e chunking.
7. `build_indexing_container()` — monta extractor, chunker e `ExtractAndChunkDocumentUseCase` sem acessar banco ou provider externo.
8. `ExtractAndChunkDocumentUseCase.execute()` — organiza a extração e a divisão do documento.
9. `Utf8FileTextExtractor.extract()` — abre o arquivo e lê seu conteúdo como texto.
10. `normalize_text()` — limpa e padroniza o texto.
11. `LangChainTextChunker.chunk()` — divide o texto em pedaços menores.
12. `RecursiveCharacterTextSplitter` — escolhe os melhores pontos para separar o texto.
13. `splitter.create_documents()` — produz os documentos menores.
14. `DocumentChunk` — representa um pedaço do documento dentro da aplicação.
15. `persist_document_chunks()` — solicita ao composition root as dependências de persistência.
16. `build_semantic_search_container()` — valida o backend PostgreSQL e monta embeddings, vector store e casos de uso.
17. `PostgresChunkVectorStore.upsert()` — prepara e grava os pedaços no banco vetorial.
18. `OpenAIEmbeddingRepository.embed()` — pede os vetores para o provider de embeddings.
19. `OpenAIEmbeddings.embed_documents()` — usa o LangChain para fazer essa chamada.
20. `provider OpenAI /v1/embeddings` — transforma cada texto em uma lista de números.
21. `PGVector.add_embeddings()` — salva textos, vetores e informações extras no PostgreSQL.

As fachadas `indexing.py` e `retrieval.py` não mantêm instâncias globais. A importação dos módulos é segura; a configuração do PostgreSQL e a criação do vector store acontecem somente quando o fluxo de persistência ou consulta é executado.

## Repository e provider

```text
PostgresChunkVectorStore
└── LangChainEmbeddingAdapter
    └── OpenAIEmbeddingRepository
        └── LangChain OpenAIEmbeddings
            └── provider externo OpenAI
```

### Explicação simples da relação entre repository e provider

1. `PostgresChunkVectorStore` — controla a gravação e a busca dos chunks vetorizados.
2. `LangChainEmbeddingAdapter` — faz a ponte entre o PGVector e o contrato local de embeddings.
3. `OpenAIEmbeddingRepository` — organiza a chamada ao serviço de embeddings.
4. `LangChain OpenAIEmbeddings` — componente do LangChain que executa a integração.
5. `provider externo OpenAI` — serviço que converte textos em vetores numéricos.

Na API, `DocumentRepository` é atualmente fornecido por
`InMemoryDocumentRepository`, portanto os metadados do documento permanecem
em memória durante a execução do processo. A persistência vetorial acontece no
serviço Python por meio de `PostgresChunkVectorStore`, que recebe os embeddings do
`OpenAIEmbeddingRepository` e delega a gravação ao `PGVector` do LangChain.

O `OpenAIEmbeddingRepository` mantém as validações da aplicação, enquanto o
`OpenAIEmbeddings` abstrai o transporte, batching e integração com o provider.
O `PostgresChunkVectorStore` mantém o isolamento por `project_id`, offsets,
dimensão, metadata e IDs determinísticos antes de chamar o PGVector.

## Fora deste fluxo

O upload não executa prompts, chains, reranking ou LangGraph. Esses componentes
podem participar posteriormente do fluxo de perguntas e respostas, mas a
indexação atual termina em:

```text
arquivo -> texto -> chunks -> embeddings -> PGVector/PostgreSQL
```

## Arquivos de referência

- API: [`documents.controller.ts`](../../rastro-api/src/modules/documents/presentation/documents.controller.ts), [`upload-document.use-case.ts`](../../rastro-api/src/modules/documents/application/upload-document.use-case.ts), [`http-document-indexer.ts`](../../rastro-api/src/modules/documents/infrastructure/http-document-indexer.ts).
- Indexação: [`service.py`](../../rastro-ai/src/rastro_ai/service.py), [`indexing.py`](../../rastro-ai/src/rastro_ai/indexing.py), [`container.py`](../../rastro-ai/src/rastro_ai/bootstrap/container.py), [`extract_and_chunk_document.py`](../../rastro-ai/src/rastro_ai/document_indexing/application/use_cases/extract_and_chunk_document.py), [`langchain_text_chunker.py`](../../rastro-ai/src/rastro_ai/document_indexing/infrastructure/chunking/langchain_text_chunker.py).
- Embeddings e vector store: [`openai_embedding_repository.py`](../../rastro-ai/src/rastro_ai/document_indexing/infrastructure/embeddings/openai_embedding_repository.py), [`postgres_vector_store.py`](../../rastro-ai/src/rastro_ai/document_indexing/infrastructure/retrieval/postgres_vector_store.py), [`retrieval.py`](../../rastro-ai/src/rastro_ai/retrieval.py).

## Observação operacional

O serviço Python precisa iniciar corretamente antes do upload. A imagem deve
possuir `langchain-text-splitters`, `langchain-openai`, `langchain-postgres` e
`langgraph`, conforme o `pyproject.toml` e os Dockerfiles. O endpoint Python
`/index` usa o backend persistente quando `VECTOR_STORE_BACKEND=postgres`, a
URL do banco e `OPENAI_API_KEY` estão configuradas.
