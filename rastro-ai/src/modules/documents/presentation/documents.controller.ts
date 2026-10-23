
import { Body, Controller, Get, Inject, Post } from '@nestjs/common';
import { IsNotEmpty, IsString } from 'class-validator';
import { CreateDocumentUseCase } from '../application/create-document.use-case';
import { DocumentRepository } from '../application/document.repository';

class CreateDocumentRequest {
  @IsString()
  @IsNotEmpty()
  name!: string;

  @IsString()
  @IsNotEmpty()
  content!: string;
}

@Controller('documents')
export class DocumentsController {
  constructor(
    private readonly createDocumentUseCase: CreateDocumentUseCase,
    @Inject('DocumentRepository')
    private readonly documentRepository: DocumentRepository,
  ) {}

  @Post()
  create(@Body() request: CreateDocumentRequest) {
    return this.createDocumentUseCase.execute(request);
  }

  @Get()
  async findAll() {
    const documents = await this.documentRepository.findAll();
    return documents.map((document) => document.toJSON());
  }
}
