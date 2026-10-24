## Alteração: validar projectId no contrato HTTP de documentos

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/modules/documents/presentation/documents.controller.ts`
- Aplicação: `api`
- Localização: linhas 7–15, classe `CreateDocumentRequest`.
- Operação: `insert`
- Âncoras: inserir antes da propriedade `name` dentro de `CreateDocumentRequest` e manter a propriedade `content` como trecho posterior.
- O que o trecho faz: exige que a criação HTTP informe o projeto do documento.
- Motivo: alinhar o DTO com o contrato do domínio e preparar o filtro por projeto das tarefas seguintes.
- Impacto: `POST /api/v1/documents` sem `projectId` passa a retornar validação 400.
- Dependências: aplicar depois do caso de uso; `ValidationPipe` global já está configurado em `src/main.ts`.

### Localização exata

```text
Trecho anterior:
class CreateDocumentRequest {
  @IsString()
  @IsNotEmpty()
  name!: string;

Trecho posterior:
  @IsString()
  @IsNotEmpty()
  content!: string;
}
```

### Conteúdo copiável

```ts
  @IsString()
  @IsNotEmpty()
  projectId!: string;
```

### Explicação do trecho

- O código faz: aplica validação de string não vazia ao escopo do documento.
- Por que inserir: o controller deve rejeitar entradas incompletas antes de chamar o caso de uso.
- O que permanece inalterado: endpoints, repositório em memória e validações de `name` e `content`.

### Verificação

1. Aplicar o campo no DTO.
2. Executar `npm run build`.
3. Enviar `POST /api/v1/documents` sem `projectId` e confirmar HTTP 400.
4. Enviar o mesmo payload com `projectId` e confirmar HTTP 201/200 conforme o adaptador atual.
