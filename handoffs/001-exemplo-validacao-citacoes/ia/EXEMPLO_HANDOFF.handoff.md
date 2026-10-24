# Exemplo de handoff de implementação

> Este arquivo é apenas demonstrativo. Os caminhos, linhas e trechos abaixo são fictícios e não devem ser aplicados no projeto.

## Objetivo do exemplo

Adicionar uma etapa de validação de citações ao fluxo do agente antes da resposta final.

O exemplo demonstra como documentar três tipos de alteração:

- `insert`: adicionar um novo bloco;
- `replace`: substituir um bloco existente;
- `remove`: excluir um bloco obsoleto.

## Ordem de aplicação

1. Aplicar o `insert` no arquivo do grafo.
2. Aplicar o `replace` no nó de resposta.
3. Aplicar o `remove` no helper obsoleto.
4. Executar os testes do agente e o evaluation de citações.

---

## Alteração 1 — inserir o nó de validação de citações

- Arquivo original: `/home/dev/dev/ia/rastro-ai/app/agent/graph.py`
- Aplicação: `ia`
- Localização aproximada: linha 42
- Ponto estrutural: função `build_agent_graph`
- Operação: `insert`
- Pré-requisitos: nenhum

### Trecho anterior

```python
    graph.add_node("generate_answer", generate_answer)
    graph.add_edge("retrieve_context", "generate_answer")
```

### Conteúdo copiável

```python
    graph.add_node("validate_citations", validate_citations)
    graph.add_edge("generate_answer", "validate_citations")
```

### Trecho posterior

```python
    graph.add_edge("generate_answer", END)
    return graph.compile()
```

### O que o trecho faz

Registra o novo nó `validate_citations` e conecta a resposta gerada a essa etapa antes da finalização do grafo.

### Por que inserir

A validação deve confirmar que as citações retornadas apontam para fontes recuperadas antes que a resposta seja entregue ao usuário.

### O que permanece inalterado

O retrieval e a geração da resposta continuam sendo executados pelos nós existentes. Apenas uma etapa de validação é adicionada ao fluxo.

### Verificação

Executar o teste que confirma que uma resposta com citação inexistente é rejeitada ou marcada para revisão.

---

## Alteração 2 — substituir a resposta sem evidência

- Arquivo original: `/home/dev/dev/ia/rastro-ai/app/agent/nodes/answer.py`
- Aplicação: `ia`
- Localização aproximada: linha 28
- Ponto estrutural: função `generate_answer`
- Operação: `replace`
- Pré-requisitos: aplicar a alteração 1

### Trecho anterior

```python
def generate_answer(state: AgentState) -> dict:
    prompt = ANSWER_PROMPT.format(
        question=state.question,
        context=state.context,
    )
    response = llm.invoke(prompt)
    return {"answer": response.content}
```

### Conteúdo atual a substituir

```python
    response = llm.invoke(prompt)
    return {"answer": response.content}
```

### Conteúdo novo copiável

```python
    if not state.context:
        return {
            "answer": "Não encontrei evidência suficiente nos documentos disponíveis.",
            "needs_review": True,
        }

    response = llm.invoke(prompt)
    return {"answer": response.content, "needs_review": False}
```

### Trecho posterior

```python
    return {"answer": response.content}


def validate_citations(state: AgentState) -> dict:
```

### O que o trecho faz

Impede que o modelo seja chamado quando não existe contexto recuperado e registra que a resposta precisa de revisão.

### Por que substituir

O comportamento anterior permitia que o modelo respondesse sem evidência. O novo comportamento reduz o risco de alucinação e torna a ausência de contexto explícita.

### O que permanece inalterado

Quando existe contexto, a chamada ao modelo continua usando o mesmo prompt e retorna a resposta gerada.

### Verificação

Adicionar ou executar casos de evaluation para:

- pergunta com fonte disponível;
- pergunta sem fonte disponível;
- resposta que deve declarar ausência de evidência.

---

## Alteração 3 — remover helper obsoleto

- Arquivo original: `/home/dev/dev/ia/rastro-ai/app/agent/prompts.py`
- Aplicação: `ia`
- Localização aproximada: linhas 8–12
- Ponto estrutural: função `format_context_for_prompt`
- Operação: `remove`
- Pré-requisitos: confirmar que nenhuma chamada ainda utiliza a função

### Trecho anterior

```python
from app.agent.context import RetrievedDocument


def format_context_for_prompt(documents: list[RetrievedDocument]) -> str:
```

### Conteúdo a remover

```python
def format_context_for_prompt(documents: list[RetrievedDocument]) -> str:
    return "\n\n".join(document.content for document in documents)
```

### Trecho posterior

```python
def build_answer_prompt(question: str, context: str) -> str:
    return ANSWER_TEMPLATE.format(question=question, context=context)
```

### O que o trecho faz

O helper antigo concatenava o texto dos documentos sem preservar identificadores ou metadados de citação.

### Por que remover

O novo formatter de contexto, usado pelo nó de retrieval, preserva `document_id`, posição do trecho e fonte. Manter os dois helpers poderia causar uso acidental do formato sem citações.

### O que permanece inalterado

A função `build_answer_prompt` e o template de resposta continuam no arquivo.

### Verificação

Pesquisar chamadas para `format_context_for_prompt` antes de remover. Depois, executar os testes de retrieval e de correção das citações.

---

## Resumo do handoff

| Alteração | Operação | Arquivo | Resultado |
| --- | --- | --- | --- |
| Nó de validação | `insert` | `app/agent/graph.py` | valida citações antes da resposta final |
| Ausência de contexto | `replace` | `app/agent/nodes/answer.py` | evita resposta sem evidência |
| Helper obsoleto | `remove` | `app/agent/prompts.py` | elimina formatter que não preserva citações |

Nenhuma alteração deve ser aplicada automaticamente. O responsável deve conferir os trechos atuais, aplicar cada operação na ordem indicada e executar os testes após a aplicação.
