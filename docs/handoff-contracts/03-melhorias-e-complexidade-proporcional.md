# Contrato das melhorias evolutivas e da complexidade proporcional

## Objetivo

Definir as melhorias prioritárias do fluxo e impedir que o próprio handoff se torne uma burocracia desproporcional.

## Melhorias obrigatórias

1. Manter uma única tarefa ativa por iniciativa.
2. Representar explicitamente o estado `idle`, quando não houver tarefa aberta.
3. Validar automaticamente a consistência entre `CURRENT.md`, `SEQUENCE.md`, README, versões e timelines.
4. Separar status de implementação de maturidade da capacidade.
5. Manter decisões permanentes e riscos vivos em local recuperável.
6. Criar novas versões apenas para mudanças semânticas, reconciliações ou novas evidências relevantes.
7. Preservar alterações não relacionadas fora do escopo e do commit.
8. Aplicar uma trilha proporcional para tarefas pequenas, médias e grandes.

## Classificação proporcional

### `small`

Use para alteração isolada, de baixo risco, sem dependência entre aplicações e com validação simples.

Registro mínimo:

- objetivo;
- arquivos afetados;
- mudança aplicada;
- validação executada;
- resultado e pendência.

Não exige sequência nova, cobertura extensa ou jornada detalhada, salvo quando a alteração atingir contrato, segurança, IA ou operação crítica.

### `normal`

Use para uma capacidade única com impacto comportamental ou mais de um arquivo relacionado.

Registro obrigatório:

- handoff numerado com `v1`;
- estado, decisão e evidência;
- invariantes e impacto;
- testes aplicáveis;
- README e timeline da versão;
- validação reproduzível.

### `large`

Use para múltiplas aplicações, contratos, dependências, riscos ou validações independentes.

Registro obrigatório:

- sequência de etapas;
- dependências e critérios de avanço;
- uma tarefa ativa por vez;
- versões por rodada significativa;
- cobertura por comportamento;
- evaluation, observabilidade ou smoke quando aplicável;
- commit explícito por etapa.

## Promoção de complexidade

Se uma tarefa `small` adquirir dependência, alteração de contrato, risco operacional, mudança de IA, múltiplos consumidores ou validação independente, ela deve ser promovida para `normal` ou `large`. O registro inicial permanece como histórico; a nova versão documenta a promoção e o motivo.

## Critério de aceitação

O processo é proporcional quando uma alteração pequena consegue ser registrada e verificada rapidamente, enquanto uma alteração média ou grande não consegue avançar sem estado, decisão, evidência e controle de escopo suficientes.
