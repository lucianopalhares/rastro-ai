# v1 — Retrieval vetorial mínimo

- Versão: `v1` | Versão-base: `005/v3` (`verified`) | Data: 2026-10-24 -03:00 | Status: `verified`.
- Contexto: extração e chunking já estão verificados; não existia store nem consulta e o código real não possui divergências locais.
- Arquivos reais: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/document_indexing/domain/entities.py`, `application/ports.py`, `application/use_cases/retrieve_chunks.py`, `infrastructure/retrieval/in_memory_vector_store.py`, `retrieval.py` e `/home/dev/dev/ia/rastro-ai/rastro-ai/tests/test_retrieval.py`.
- Operações: `replace` na entidade, serviços e fachadas para incluir projeto; `insert` nos módulos de retrieval, documentação e testes; âncoras são `DocumentChunk`, `application ports` e fachadas.

## O que foi feito

- Implementar contrato de consulta, representação de resultado e store em memória com vetores de frequência de termos e similaridade de cosseno.
- Criar caso de uso que valida projeto, consulta e limite, filtra por projeto antes do ranking e expor fachada `retrieve_chunks`/`index_chunks`.
- Cobrir ranking, isolamento entre projetos, limite, entradas inválidas e consulta sem correspondência.

## O que muda na aplicação

- Chunks passam a carregar `project_id` e podem ser indexados e consultados de forma síncrona, determinística e local.
- Não há embeddings de modelo, persistência, chamadas HTTP, worker ou alteração do fluxo de extração; qualidade semântica, custo e latência de LLM permanecem inalterados.
- Risco conhecido: o ranking lexical não representa semântica; a substituição por embeddings reais exige nova avaliação e observabilidade.

## Instruções de validação

1. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && python3 -m unittest discover -s tests -p 'test_*.py' -v`; resultado esperado: 11 testes aprovados.
2. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && python3 -m compileall -q src tests`; resultado esperado: conclusão sem erro.
3. Execute `.agents/hooks/validate-handoffs.sh handoffs/006-retrieval-vetorial-minimo/README.md handoffs/006-retrieval-vetorial-minimo/TIMELINE.md handoffs/006-retrieval-vetorial-minimo/v1/README.md handoffs/006-retrieval-vetorial-minimo/v1/TIMELINE.md`; resultado esperado: `handoffs válidos: 4 arquivo(s)`.
