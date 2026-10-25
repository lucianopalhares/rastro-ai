# Linha do tempo — 012/v4 Tokenizer real no chunking

## v4 — tiktoken aplicado

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: serviço de chunking, fachadas, dependências, Dockerfile, testes e README Python.
- Mudanças aplicadas: `tiktoken` para contagem real, offsets Unicode, teste específico e imagem Python atualizada.
- Problema resolvido: o orçamento de tokens era estimado por palavras e podia divergir do modelo de embedding.
- Verificação: 26 testes Python, compilação, build da imagem com `tiktoken`, diff check e hook estrutural aprovados.
- Pendência: nenhuma mudança de API, provider ou banco; smoke externo permanece coberto pela v3.
