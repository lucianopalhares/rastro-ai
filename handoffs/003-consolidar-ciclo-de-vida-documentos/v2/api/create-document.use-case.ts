## Alteração: propagar projectId na criação de documentos

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/application/create-document.use-case.ts`
- Aplicação: `api`
- Localização: linhas 6–9 e 15–19, interface `CreateDocumentInput` e chamada `Document.create`.
- Operação: replace
- Âncoras: `export interface CreateDocumentInput` e chamada `Document.create` antes de `await this.documentRepository.save`.
- O que o trecho faz: exige e encaminha o projeto ao agregado documental.
- Motivo: o domínio passa a exigir `projectId` para estabelecer o escopo mínimo do documento.
- Impacto: chamadas sem projeto deixam de satisfazer o contrato TypeScript e a validação de domínio.
- Dependências: aplicar depois de `document.ts`.

### Conteúdo atual

```ts
export interface CreateDocumentInput {
  name: string;
  content: string;
}

const document = Document.create({
  id: randomUUID(),
  name: input.name,
  content: input.content,
});
```

### Conteúdo copiável

```ts
export interface CreateDocumentInput {
  projectId: string;
  name: string;
  content: string;
}

const document = Document.create({
  id: randomUUID(),
  projectId: input.projectId,
  name: input.name,
  content: input.content,
});
```

### Explicação do trecho

- O código faz: mantém o caso de uso como ponto único de criação e adiciona o identificador do projeto ao comando.
- Por que substituir: evita que controllers ou futuros workers montem o agregado sem escopo.
- O que permanece inalterado: UUID, persistência pelo `DocumentRepository` e retorno serializado.

### Verificação

1. Aplicar os fragmentos nas posições indicadas.
2. Executar `npm run build` em `/home/dev/dev/ia/rastro-ai/rastro-api`.
3. Confirmar que o resultado criado contém `projectId` e status `pending`.
