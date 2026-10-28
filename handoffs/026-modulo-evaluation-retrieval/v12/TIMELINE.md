# Timeline — 026/v12 debug da avaliação real

## 2026-10-27 -03:00 — aplicação v12

- Status: `applied`.
- Versão-base: `v11` aplicada; o comando normal e os arquivos de debug foram conferidos.
- Mudanças: README do retrieval atualizado com comando `debugpy`, `--wait-for-client`, publicação da porta 5678 e mapeamento de `/app/evals`.
- Problema resolvido: breakpoint em `evaluate.py` não era atingido porque o comando original executava o módulo sem iniciar debugger.
- Evidência: documentação revisada; testes automatizados e hook estrutural serão executados nesta rodada.
- Pendência: validação interativa do attach do VS Code depende da execução manual com serviços, corpus e credenciais disponíveis.
