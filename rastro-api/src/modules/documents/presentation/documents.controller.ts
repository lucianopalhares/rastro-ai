
import {
  BadRequestException,
  Body,
  Controller,
  Get,
  Inject,
  Post,
  Query,
  UploadedFile,
  UseInterceptors,
} from '@nestjs/common';
import { FileInterceptor } from '@nestjs/platform-express';
import { Type } from 'class-transformer';
import { IsInt, IsNotEmpty, IsOptional, IsString, Max, Min } from 'class-validator';
import { CreateDocumentUseCase } from '../application/create-document.use-case';
import { DocumentRepository } from '../application/document.repository';
import { SemanticSearcher } from '../application/semantic-searcher';
import { UploadDocumentUseCase } from '../application/upload-document.use-case';

/**
 * Define o payload JSON usado na criação direta de documentos.
 *
 * v1 = preservou o contrato existente durante a inclusão do upload.
 */
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

/**
 * Define os campos textuais recebidos no formulário multipart.
 *
 * v1 = adicionou o vínculo obrigatório com o projeto.
 */
class UploadDocumentRequest {
  @IsString()
  @IsNotEmpty()
  projectId!: string;
}

/**
 * Define os parâmetros da consulta semântica pública.
 * Histórico: 023-v1 — valida projeto, pergunta e limite antes do proxy Python.
 */
class SemanticSearchRequest {
  @IsString()
  @IsNotEmpty()
  projectId!: string;

  @IsString()
  @IsNotEmpty()
  query!: string;

  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(50)
  limit = 5;
}

/**
 * Mantém somente os dados do arquivo necessários para a aplicação.
 *
 * v1 = criou um tipo local para evitar acoplamento do domínio ao Express.
 */
interface UploadedDocumentFile {
  originalname: string;
  mimetype: string;
  size: number;
  buffer: Buffer;
}

/**
 * Expõe criação, upload e consulta dos documentos.
 *
 * v1 = adicionou o endpoint multipart sem remover o endpoint JSON existente.
 * 023-v1 = adicionou a consulta semântica determinística por projeto.
 */
@Controller('documents')
export class DocumentsController {
  /**
   * Recebe os casos de uso e o repositório usados pelos endpoints.
   *
   * v1 = adicionou a dependência do caso de uso de upload.
   */
  constructor(
    private readonly createDocumentUseCase: CreateDocumentUseCase,
    private readonly uploadDocumentUseCase: UploadDocumentUseCase,
    @Inject('DocumentRepository')
    private readonly documentRepository: DocumentRepository,
    @Inject('SemanticSearcher')
    private readonly semanticSearcher: SemanticSearcher,
  ) {}

  /**
   * Cria um documento a partir de um payload JSON.
   *
   * v1 = preservou o contrato JSON anterior.
   */
  @Post()
  create(@Body() request: CreateDocumentRequest) {
    return this.createDocumentUseCase.execute(request);
  }

  /**
   * Recebe um arquivo textual e cria o documento do projeto.
   *
   * v1 = adicionou multipart com limite de 5 MiB para `.md` e `.txt`.
   * v5/v6 = tentaram contornar um comando curl sem o marcador de arquivo;
   * v7 restaura o binding padrão após corrigir o comando.
   */
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

  /**
   * Lista os documentos mantidos pelo repositório atual.
   *
   * v1 = preservou a consulta e passou a expor a origem quando houver.
   */
  @Get()
  async findAll() {
    const documents = await this.documentRepository.findAll();
    return documents.map((document) => document.toJSON());
  }

  /**
   * Busca semanticamente os chunks de um projeto e retorna suas citações.
   * Histórico: 023-v1 — publica o contrato determinístico do Rastro AI na API.
   */
  @Get('search')
  search(@Query() request: SemanticSearchRequest) {
    return this.semanticSearcher.search(request.projectId, request.query, request.limit);
  }
}
