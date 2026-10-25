## v5 — Embeddings adaptados ao LangChain

- Data/hora: 2026-10-25 -03:00.
- Status: `applied`.
- Aplicação: serviço Python `rastro-ai` e imagens Docker.
- Mudança: `OpenAIEmbeddingRepository` delega embeddings em lote a `OpenAIEmbeddings`, mantendo o contrato local e validação de dimensão.
- Problema resolvido: remove o transporte HTTP manual e prepara a troca de provedor sem alterar os casos de uso.
- Verificação: 31 testes, evaluation `20/20`, compilação, build Docker, import no container e hook aprovados.
- Pendência: chamada real com OpenAI e medição de custo/latência aguardam credencial e finalização.
