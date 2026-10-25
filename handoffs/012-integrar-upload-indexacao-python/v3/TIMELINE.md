# Linha do tempo — 012/v3 Chunking estrutural por tokens

## v3 — Chunking aplicado

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: serviço de domínio, caso de uso, fachadas, testes e README Python.
- Mudanças aplicadas: fronteiras de parágrafos/títulos, orçamento aproximado de 500 tokens, overlap de 60 e compatibilidade legada.
- Problema resolvido: cortes fixos por caracteres podiam separar unidades semânticas Markdown.
- Verificação: 25 testes Python, compilação, diff check e hook estrutural aprovados.
- Pendências: avaliar tamanhos/overlap com dataset real de retrieval após o smoke externo solicitado anteriormente.

## v3 — Smoke externo após o chunking

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Verificação real: upload curto retornou `ready` com 1 chunk; upload longo retornou `ready` com 2 chunks.
- Banco: `document_chunks` confirmou conteúdo não vazio, offsets, embeddings presentes e dimensão `384` nos dois chunks longos.
- Resultado: o chunking estrutural e o repository externo funcionam juntos no fluxo API → Python → OpenAI → pgvector.
- Limite: a qualidade semântica do ranking ainda não foi medida por evaluation; a validação realizada confirma estrutura, persistência e dimensão.
