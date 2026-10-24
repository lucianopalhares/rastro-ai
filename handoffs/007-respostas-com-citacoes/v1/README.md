# v1 — Respostas com citações

- Versão: `v1` | Versão-base: `006/v1` (`verified`) | Data: 2026-10-24 -03:00 | Status: `verified`.
- Contexto: retrieval real já retorna `RetrievedChunk` com documento, índice, offsets, projeto e conteúdo; não existia contrato de resposta.
- Arquivos reais conferidos: `/home/dev/dev/ia/rastro-ai/rastro-ai/src/rastro_ai/document_indexing/application/use_cases/retrieve_chunks.py`, `retrieval.py`, `entities.py`, testes e README.
- Arquivos alterados: `rastro-ai/src/rastro_ai/document_indexing/application/use_cases/answer_question.py`, `application/use_cases/__init__.py`, `rastro-ai/src/rastro_ai/retrieval.py`, `rastro-ai/tests/test_answers.py` e `rastro-ai/README.md`.
- Operações e âncoras: `insert` no caso de uso e testes; `replace` nos exports, fachada e README; âncoras `AnswerQuestionUseCase`, `answer_question` e seção de comportamento da aplicação.

## O que foi feito

- Criado `AnswerQuestionUseCase`, com porta de retrieval, `Answer` e `Citation` contendo documento, índice, offsets e trecho exato.
- Respostas positivas reproduzem somente os chunks retornados e identificam cada fonte como `[document_id#chunk_index]`; respostas sem resultados declaram ausência de evidência.
- Mantido o filtro por projeto delegado ao retrieval e adicionada cobertura para evidência, ausência e isolamento entre projetos.
- Problema resolvido: conectar pergunta, retrieval e fonte citável sem inventar conteúdo ou introduzir dependência de modelo.

## O que muda na aplicação

- A fachada `rastro_ai.retrieval.answer_question` passa a responder de modo extrativo e determinístico a partir dos chunks previamente indexados.
- Não há LLM, prompt, LangGraph, chamada externa, alteração de custo ou latência de inferência; qualidade semântica, avaliação, validação de citações geradas e resposta natural ficam fora do escopo.
- Risco conhecido: a resposta é uma composição de trechos, não uma síntese; o próximo baseline deve medir relevância, faithfulness e correção das citações.

## Jornada da aplicação nesta versão

- Propósito: permitir que o Rastro transforme documentos em respostas fundamentadas e fontes conferíveis.
- Antes: a aplicação extraía, dividia, indexava e recuperava trechos, mas não apresentava uma resposta citável para uma pergunta.
- Agora: uma pergunta sobre o projeto pode retornar os trechos encontrados, identificando documento e posição; sem correspondência, a aplicação informa que não há evidência suficiente.
- Resultado percebido: a pessoa consegue conferir qual trecho sustentou a resposta, embora a capacidade ainda esteja no serviço Python.
- Ainda falta: não há endpoint, tela ou worker conectado para executar essa pergunta pelo produto completo.
- Próxima evolução: integrar a resposta à API e ao frontend e depois medir a qualidade com evaluation.

## Como usar e validar a aplicação nesta versão

- Caminho disponível nesta versão: executar o smoke da seção `## Instruções de validação`, que percorre arquivo, extração, chunking, indexação e pergunta usando os módulos reais de `rastro-ai`.
- Uso pelo produto completo: indisponível nesta etapa, pois não existe request HTTP nem tela frontend para a pergunta; não inventar uma URL ou ação de interface.
- Resultado esperado: o comando retorna uma citação do documento indexado e uma resposta sem citações quando a consulta não possui evidência lexical.

## Cobertura por comportamento

| Comportamento | Teste unitário/contrato | Integração ou smoke/manual real | Resultado esperado |
| --- | --- | --- | --- |
| Resposta com citação | `tests/test_answers.py::test_answer_contains_retrieved_excerpt_and_citation` | Smoke da fachada `index_chunks` → `answer_question` | `Answer.citations` contém documento, índice, offsets e trecho recuperado |
| Ausência de evidência | `tests/test_answers.py::test_answer_declares_absence_of_evidence` | Smoke da fachada com consulta sem termo compartilhado | `citations == ()` e mensagem explícita de ausência |
| Isolamento por projeto | `tests/test_answers.py::test_answer_does_not_cite_other_projects` | Não há endpoint ou worker integrado nesta aplicação Python; o smoke da fachada cobre o contrato público local | Nenhuma citação de outro projeto |

## Instruções de validação

1. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && python3 -m unittest discover -s tests -p 'test_*.py' -v`; resultado esperado: 14 testes aprovados.
2. Execute `cd /home/dev/dev/ia/rastro-ai/rastro-ai && python3 -m compileall -q src tests`; resultado esperado: conclusão sem erro.
3. Execute `REQUIRE_BEHAVIOR_COVERAGE=1 .agents/hooks/validate-handoffs.sh handoffs/007-respostas-com-citacoes/README.md handoffs/007-respostas-com-citacoes/TIMELINE.md handoffs/007-respostas-com-citacoes/v1/README.md handoffs/007-respostas-com-citacoes/v1/TIMELINE.md`; resultado esperado: `handoffs válidos: 4 arquivo(s)`.
4. Execute o smoke integrado reproduzível:

   ```bash
   cd /home/dev/dev/ia/rastro-ai && PYTHONPATH=rastro-ai/src python3 - <<'PY'
   from pathlib import Path
   from tempfile import TemporaryDirectory

   from rastro_ai.indexing import index_document
   from rastro_ai.retrieval import answer_question, index_chunks

   with TemporaryDirectory() as directory:
       path = Path(directory) / "meeting.txt"
       path.write_text("A equipe escolheu PostgreSQL por causa do suporte transacional.", encoding="utf-8")
       chunks = index_document("meeting-1", path, project_id="project-1")
       index_chunks(chunks)
       answer = answer_question("project-1", "Por que escolheram PostgreSQL?")
       assert answer.citations
       assert answer.citations[0].document_id == "meeting-1"
       assert answer.citations[0].excerpt in answer.text
       assert answer_question("project-1", "orçamento").citations == ()
   print("smoke integrado de indexação e resposta: OK")
   PY
   ```

   Resultado esperado: `smoke integrado de indexação e resposta: OK`, com citação do documento indexado e ausência de citação para uma consulta sem evidência lexical.
