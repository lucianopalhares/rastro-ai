
import { Module } from '@nestjs/common';
import { CreateDocumentUseCase } from './application/create-document.use-case';
import { DocumentFileStorage } from './application/document-file.storage';
import { DocumentRepository } from './application/document.repository';
import { UploadDocumentUseCase } from './application/upload-document.use-case';
import { InMemoryDocumentRepository } from './infrastructure/in-memory-document.repository';
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
      ) => new UploadDocumentUseCase(documentRepository, documentFileStorage),
      inject: ['DocumentRepository', 'DocumentFileStorage'],
    },
  ],
})
export class DocumentsModule {}

