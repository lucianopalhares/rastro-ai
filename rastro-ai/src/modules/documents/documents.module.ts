
import { Module } from '@nestjs/common';
import { CreateDocumentUseCase } from './application/create-document.use-case';
import { DocumentRepository } from './application/document.repository';
import { InMemoryDocumentRepository } from './infrastructure/in-memory-document.repository';
import { DocumentsController } from './presentation/documents.controller';

@Module({
  controllers: [DocumentsController],
  providers: [
    InMemoryDocumentRepository,
    {
      provide: 'DocumentRepository',
      useExisting: InMemoryDocumentRepository,
    },
    {
      provide: CreateDocumentUseCase,
      useFactory: (documentRepository: DocumentRepository) =>
        new CreateDocumentUseCase(documentRepository),
      inject: ['DocumentRepository'],
    },
  ],
})
export class DocumentsModule {}

