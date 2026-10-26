# Contrato do modelo de estado, decisão e evidência

## Objetivo

Organizar o handoff em três camadas complementares para controlar mudanças feitas com apoio de agentes de IA.

## Camada 1 — Estado

Registra onde a tarefa está.

Campos mínimos:

- tarefa e iniciativa;
- status da implementação;
- versão atual;
- dependências;
- arquivos em escopo;
- pendências e bloqueios;
- próxima ação.

`CURRENT.md` aponta apenas para a tarefa aberta da iniciativa ativa. Uma implementação finalizada não deve continuar sendo tratada como tarefa aberta.

## Camada 2 — Decisão

Registra por que a mudança existe.

Campos mínimos quando aplicáveis:

- objetivo e problema;
- escopo autorizado;
- invariantes;
- decisão tomada;
- alternativas descartadas;
- riscos aceitos;
- condição de revisão;
- impacto esperado.

O agente pode organizar a decisão, mas não deve atribuir ao responsável uma escolha que não foi autorizada.

## Camada 3 — Evidência

Registra como a conclusão foi demonstrada.

Tipos de evidência:

- inspeção estrutural;
- teste unitário ou contratual;
- integração;
- smoke ou validação manual real;
- evaluation de qualidade, custo ou latência;
- diff, lista explícita de arquivos e commit.

Cada evidência deve informar comando ou ação, resultado observado, limite e se foi executada no estado atual.

## Relação entre as camadas

Uma tarefa não está completa apenas porque possui estado documentado. O estado precisa apontar para uma decisão compreensível e para evidências compatíveis com o risco da mudança.

| Camada | Pergunta | Falha quando |
| --- | --- | --- |
| Estado | Onde estamos? | não é possível identificar a tarefa aberta, a versão ou a pendência |
| Decisão | Por que estamos fazendo isso? | o motivo, as invariantes ou os limites foram perdidos |
| Evidência | Como sabemos que terminou? | o resultado não é reproduzível ou não corresponde ao risco |

## Critério de aceitação

Uma versão está documentada adequadamente quando as três camadas podem ser lidas em conjunto sem exigir a reconstrução integral da conversa com o agente.
