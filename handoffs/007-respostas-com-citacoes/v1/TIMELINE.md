# Linha do tempo — 007 v1 Respostas com citações

## v1 — Registro da aplicação

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Arquivos reais conferidos: caso de uso de retrieval, store, entidades, fachada, testes e README da aplicação.
- Mudanças: contrato de resposta e citação, resposta extrativa, fachada pública, testes de evidência/ausência/isolamento e documentação.
- Problema: perguntas não tinham resposta citável nem negativa segura quando o retrieval não encontrava resultados.
- Pendências: evaluation, LLM, LangGraph, validação de citações geradas e observabilidade permanecem fora desta rodada.
- Verificação: 14 testes passaram; compilação passou; hook estrutural será executado com os quatro arquivos presentes.

## Ajuste de cobertura de validação

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Mudanças: adicionada a matriz de cobertura por comportamento ao README da versão, distinguindo testes unitários e smoke da fachada.
- Motivo: tornar explícita a diferença entre evidência automatizada e validação integrada real, sem alterar o runtime.
- Verificação: hook padrão e hook estrito com `REQUIRE_BEHAVIOR_COVERAGE=1` validaram os quatro arquivos da implementação.

## Complemento do teste integrado reproduzível

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Mudanças: substituída a ação manual resumida por um comando Python completo que extrai, gera chunks, indexa e consulta a resposta.
- Problema resolvido: a tarefa agora contém instrução copiável para validar o fluxo real, além dos testes unitários.
- Verificação: comando integrado executado com sucesso; resultado `smoke integrado de indexação e resposta: OK`.

## Inclusão da jornada e do uso da aplicação

- Data/hora: 2026-10-24 -03:00 | Status: `applied`.
- Mudanças: adicionadas ao README da versão a jornada antes/agora/próxima e as instruções de uso disponíveis e indisponíveis no produto.
- Problema resolvido: a versão passa a explicar para uma pessoa usuária como a tarefa evolui o propósito da aplicação e quais limites permanecem.
- Verificação: README ordena Jornada, Como usar, Cobertura e Instruções; hook estrito passou com 4 arquivos.

## Finalização — v1 verificada

- Data/hora: 2026-10-24 -03:00 | Status: `verified`.
- Arquivos reais conferidos: código da IA, testes, documentação da aplicação e registros da versão.
- Mudanças de finalização: status da versão atualizado sem alteração adicional de runtime.
- Problema resolvido: evidência unitária, integração local, jornada de uso e limites da aplicação ficaram registrados.
- Verificação: 14 testes, compilação, smoke integrado e hook estrito passaram.
