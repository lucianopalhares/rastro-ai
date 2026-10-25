## v7 — Preparação do pipeline RAG

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai` e imagens Docker.
- Mudança: portas de reranking/geração, adapters LangChain, prompt reutilizável e workflow LangGraph opcional foram adicionados.
- Comportamento: resposta extrativa atual preservada; nenhuma chamada de modelo ou reranker ativada.
- Verificação: 35 testes, evaluation `20/20`, compilação, build Docker, import no container e hook aprovados.
- Pendências: escolher providers, ativar o grafo e medir qualidade, custo, latência e observabilidade.
