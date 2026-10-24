## Alteração: restaurar content no DTO de criação

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/presentation/documents.controller.ts`
- Aplicação: `api`
- Localização: linhas 7–15, classe `CreateDocumentRequest`.
- Operação: replace
- Âncoras: substituir todo o corpo de `CreateDocumentRequest`, entre sua declaração e o fechamento imediatamente anterior a `@Controller('documents')`.
- O que o trecho faz: valida `projectId`, `name` e `content` antes de chamar o caso de uso.
- Motivo: a aplicação parcial inseriu `projectId`, mas removeu `content`, causando o erro `TS2345`.
- Impacto: o controller volta a satisfazer `CreateDocumentInput` e rejeita payloads incompletos.
- Dependências: aplicar depois de `document.ts`; o `ValidationPipe` global já está configurado.

### Conteúdo atual

```ts
class CreateDocumentRequest {
  @IsString()
  @IsNotEmpty()
  name!: string;

  @IsString()
  @IsNotEmpty()
  projectId!: string;
}
```

### Conteúdo copiável

```ts
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
```

### Explicação do trecho

- O código faz: alinha o DTO HTTP aos três campos exigidos pelo caso de uso.
- Por que substituir: sem `content`, `CreateDocumentRequest` não é atribuível a `CreateDocumentInput`.
- O que permanece inalterado: endpoints, repositório e fluxo de criação.

### Verificação

1. Aplicar a substituição no controller.
2. Executar `npm run build` em `/home/dev/dev/ia/rastro-ai/rastro-api`.
3. Enviar um POST com `projectId`, `name` e `content` e confirmar a criação.
4. Enviar um POST sem `content` e confirmar HTTP 400.
