# 027 — Adaptar evaluation de retrieval para ranx
- Data/hora: 2026-10-27 -03:00 | Status: `verified`; aplicação: `rastro-ai`.
- Objetivo: substituir o cálculo manual das métricas clássicas do retrieval por `ranx`, preservando as regras específicas do projeto.
- Dependência/ordem: `026` verificada; v1 adicionou ranx, v2 separou grupos, v3 explicitou os nomes, v4 simplificou a leitura, v5 separou etapas internas, v6 atualizou o fluxo, v7 adicionou métricas operacionais e v8 adicionou filtros de saída.
- Decisão: manter o contrato dos relatórios e usar `ranx` para Recall, Precision, MRR e nDCG; isolamento, score e abstention permanecem próprios.
- Invariante: os testes controlados continuam sem banco, rede, OpenAI ou chamada LLM; os IDs `document_id:index` permanecem estáveis.
- Impacto: cálculo alinhado a uma biblioteca de ranking; custo de dependência e possível diferença de semântica em listas menores serão verificados.
- Critério: testes determinísticos, build/execução do container e documentação atualizada sem ocultar erros do retriever.
- Pasta: `handoffs/027-adaptar-evaluation-retrieval-ranx/`; tarefa verificada; próximos trabalhos: evaluation real contra PGVector e publicação Langfuse.
