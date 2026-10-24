import {
  BadRequestException,
  Body,
  Controller,
  Get,
  Inject,
  Post,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { IsNotEmpty, IsString } from 'class-validator';
import { CreateDocumentUseCase } from '../application/create-document.use-case';
import { DocumentRepository } from '../application/document.repository';
import { UploadDocumentUseCase } from '../application/upload-document.use-case';

class CreateDocumentRequest {
  @IsString()
  @IsNotEmpty()
  projectId!: string;

  @IsString()
  @IsNotEmpty()
  name!: string;

  @IsString()
  @IsNotEmpty()
  content!: string;
}

class UploadDocumentRequest {
  @IsString()
  @IsNotEmpty()
  projectId!: string;
}

/* Representa somente os dados do multipart usados pela aplicação, sem acoplar o domínio ao Express. */
interface UploadedDocumentFile {
  originalname: string;
  mimetype: string;
  size: number;
  buffer: Buffer;
}

@Controller('documents')
export class DocumentsController {
  constructor(
    private readonly createDocumentUseCase: CreateDocumentUseCase,
    private readonly uploadDocumentUseCase: UploadDocumentUseCase,
    @Inject('DocumentRepository')
    private readonly documentRepository: DocumentRepository,
  ) {}

  @Post()
  create(@Body() request: CreateDocumentRequest) {
    return this.createDocumentUseCase.execute(request);
  }

  /* Recebe o arquivo e mantém o limite inicial do MVP explícito no endpoint. */
  @Post('upload')
  @UseInterceptors(
    FileInterceptor('file', {
      limits: { fileSize: 5 * 1024 * 1024 },
    }),
  )
  async upload(
    @Body() request: UploadDocumentRequest,
    @UploadedFile() file?: UploadedDocumentFile,
  ) {
    if (!file) {
      throw new BadRequestException('A file is required');
    }

    try {
      return await this.uploadDocumentUseCase.execute({
        projectId: request.projectId,
        originalName: file.originalname,
        mimeType: file.mimetype,
        sizeBytes: file.size,
        content: file.buffer,
      });
    } catch (error) {
      throw new BadRequestException(error instanceof Error ? error.message : 'Invalid file');
    }
  }

  @Get()
  async findAll() {
    const documents = await this.documentRepository.findAll();
    return documents.map((document) => document.toJSON());
  }
}
