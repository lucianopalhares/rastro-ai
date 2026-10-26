
import { Module } from '@nestjs/common';
import { CreateDocumentUseCase } from './application/create-document.use-case';
import { DocumentFileStorage } from './application/document-file.storage';
import { DocumentRepository } from './application/document.repository';
import { UploadDocumentUseCase } from './application/upload-document.use-case';
import { InMemoryDocumentRepository } from './infrastructure/in-memory-document.repository';
import { HttpDocumentIndexer } from './infrastructure/http-document-indexer';
import { HttpSemanticSearcher } from './infrastructure/http-semantic-searcher';
import { LocalDocumentFileStorage } from './infrastructure/local-document-file.storage';
import { DocumentsController } from './presentation/documents.controller';

/**
 * Registra o domínio documental, o repositório e o armazenamento de arquivos.
 *
 * v1 = conectou o caso de uso de upload ao adaptador local.
 */
@Module({
  controllers: [DocumentsController],
  providers: [
    InMemoryDocumentRepository,
    LocalDocumentFileStorage,
    HttpDocumentIndexer,
    {
      provide: 'SemanticSearcher',
      useClass: HttpSemanticSearcher,
    },
    {
      provide: 'DocumentRepository',
      useExisting: InMemoryDocumentRepository,
    },
    {
      provide: 'DocumentFileStorage',
      useExisting: LocalDocumentFileStorage,
    },
    {
      provide: CreateDocumentUseCase,
      useFactory: (documentRepository: DocumentRepository) =>
        new CreateDocumentUseCase(documentRepository),
      inject: ['DocumentRepository'],
    },
    {
      provide: UploadDocumentUseCase,
      useFactory: (
        documentRepository: DocumentRepository,
        documentFileStorage: DocumentFileStorage,
        documentIndexer: HttpDocumentIndexer,
      ) => new UploadDocumentUseCase(documentRepository, documentFileStorage, documentIndexer),
      inject: ['DocumentRepository', 'DocumentFileStorage', HttpDocumentIndexer],
    },
  ],
})
export class DocumentsModule {}

