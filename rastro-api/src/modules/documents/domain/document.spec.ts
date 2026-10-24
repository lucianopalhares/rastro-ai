
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

