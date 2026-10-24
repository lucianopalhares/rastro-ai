## Alteração: testes do ciclo de vida do documento

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/domain/document.spec.ts`
- Aplicação: `api`
- Localização: novo arquivo ao lado de `domain/document.ts`.
- Operação: insert
- Âncoras: arquivo inexistente; criar após a aplicação do agregado `Document`.
- O que o trecho faz: cobre criação com projeto, transições válidas e bloqueio de transições inválidas.
- Motivo: o novo contrato de status precisa de uma verificação determinística antes da indexação.
- Impacto: adiciona cobertura unitária sem alterar runtime ou dependências.
- Dependências: aplicar depois de `document.ts`; Jest já está configurado no `package.json`.

### Conteúdo copiável

```ts
import { Document } from './document';

describe('Document', () => {
  const createDocument = () =>
    Document.create({
      id: 'document-1',
      projectId: 'project-1',
      name: 'Meeting notes',
      content: 'The team chose PostgreSQL.',
    });

  it('creates a document in pending status with its project', () => {
    expect(createDocument().toJSON()).toMatchObject({
      projectId: 'project-1',
      status: 'pending',
    });
  });

  it('accepts the processing lifecycle', () => {
    const document = createDocument();

    document.changeStatus('processing');
    document.changeStatus('ready');

    expect(document.toJSON().status).toBe('ready');
  });

  it('allows failed documents to be reprocessed', () => {
    const document = createDocument();

    document.changeStatus('processing');
    document.changeStatus('failed');
    document.changeStatus('processing');

    expect(document.toJSON().status).toBe('processing');
  });

  it('rejects an invalid lifecycle transition', () => {
    const document = createDocument();

    expect(() => document.changeStatus('ready')).toThrow(
      'Invalid document status transition: pending -> ready',
    );
  });

  it('requires a project', () => {
    expect(() =>
      Document.create({
        id: 'document-1',
        projectId: ' ',
        name: 'Meeting notes',
        content: 'Content',
      }),
    ).toThrow('Document projectId is required');
  });
});
```

### Explicação do trecho

- O código faz: verifica o contrato principal sem depender de HTTP, banco ou modelo.
- Por que inserir: evita que tarefas posteriores de upload e indexação assumam estados não testados.
- O que permanece inalterado: não testa persistência, embeddings, retrieval ou autorização.

### Verificação

1. Criar o arquivo indicado após aplicar o domínio.
2. Executar `npm test -- --runInBand` em `/home/dev/dev/ia/rastro-ai/rastro-api`.
3. Confirmar que os casos passam e que o build TypeScript também passa.
