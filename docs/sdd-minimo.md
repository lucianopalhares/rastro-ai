# SDD mínimo integrado aos handoffs

## Objetivo

O SDD mínimo registra somente a intenção necessária para orientar uma implementação antes da alteração no código. Ele reduz decisões prematuras, evita documentação duplicada e mantém a execução baseada no estado real do projeto.

O SDD não substitui o handoff. Ele é uma seção opcional da primeira versão (`v1`) de uma implementação.

## Relação entre as fontes

Cada fonte tem uma responsabilidade diferente:

- SDD mínimo: define o resultado esperado, os limites e os critérios de aceite.
- Handoff: registra aplicação, reconciliação, arquivos, decisões, impacto e verificações.
- Código e testes: confirmam o comportamento real atual.
- Timeline: preserva a evolução histórica.

Em caso de conflito, o código e os testes vencem para o comportamento atual. A diferença entre o SDD e o código deve ser registrada como reconciliação ou pendência; não deve ser resolvida por inferência silenciosa.

## Quando usar

- `small`: não exige SDD; basta registrar objetivo, arquivos, motivo, impacto e validação.
- `normal`: usar quando houver contrato, comportamento novo ou decisão relevante.
- `large`: usar obrigatoriamente antes da aplicação, especialmente quando houver várias etapas, aplicações, dependências ou consumidores.
- Correções e continuações: reutilizar a especificação existente e registrar somente a diferença necessária.

## Estrutura mínima

O SDD deve ficar no `v1/README.md` da implementação, antes da seção de reconciliação:

```md
## Especificação mínima

- Objetivo: resultado que precisa ser alcançado.
- Problema: situação atual que será resolvida.
- Requisitos: comportamentos obrigatórios.
- Fora do escopo: comportamentos que não serão implementados nesta rodada.
- Contrato ou comportamento esperado: entradas, saídas, estados, eventos ou regras observáveis.
- Critérios de aceite: condições objetivas para considerar a tarefa concluída.
- Riscos e decisões abertas: pontos que dependem de evidência ou decisão posterior.
```

Cada campo deve ser curto e verificável. Não descreva detalhes de implementação que ainda não sejam necessários para definir o resultado.

## Reconciliação obrigatória

Depois de registrar a especificação mínima, leia os arquivos reais e acrescente:

```md
## Reconciliação

- Arquivos reais conferidos: caminhos dos arquivos e testes analisados.
- Estado encontrado: comportamento existente confirmado.
- Diferenças: itens confirmados, parciais, divergentes, ausentes ou pendentes.
- Mudança mínima necessária: alteração que será realmente aplicada.
- Decisões tomadas: decisões derivadas da leitura do código ou dos testes.
- O que não deve ser repetido: trechos já aplicados ou decisões descartadas.
```

A aplicação deve seguir a reconciliação, e não uma proposta antiga que tenha divergido do código real.

## Ordem do fluxo

```text
Especificação mínima, quando necessária
        ↓
Leitura do código e dos testes reais
        ↓
Reconciliação da especificação com o estado atual
        ↓
Aplicação da menor mudança necessária
        ↓
Testes e validações
        ↓
Registro de decisões, pendências e próxima ação
```

O SDD não deve ser tratado como um plano imutável. Se a implementação revelar uma restrição nova, atualize a reconciliação e registre a decisão na versão correspondente.

## Critérios de eficiência

O SDD mínimo deve:

- definir o resultado sem antecipar toda a arquitetura;
- evitar repetir código, handoff ou documentação existente;
- permitir que os critérios de aceite sejam testados;
- registrar somente decisões necessárias para a rodada;
- deixar decisões irreversíveis ou incertas explícitas;
- reduzir releitura e retrabalho entre planejamento e execução.

Não use o SDD para prever detalhes que dependem de inspeção, testes ou validação externa. Esses detalhes devem ser decididos durante a reconciliação e registrados como decisões da implementação.

## Exemplo

```md
## Especificação mínima

- Objetivo: permitir upload de arquivos textuais associados a um projeto.
- Problema: a API só aceita criação de documentos por JSON.
- Requisitos: aceitar `.md` e `.txt`, rejeitar conteúdo vazio e retornar o documento pendente.
- Fora do escopo: extração, chunking, embeddings e object storage.
- Contrato ou comportamento esperado: `POST /documents/upload` com multipart e campo `projectId`.
- Critérios de aceite: upload válido retorna `201`; extensão inválida retorna `400`; o arquivo é armazenado e associado ao documento.
- Riscos e decisões abertas: armazenamento local é temporário e deverá ser substituído em etapa futura.
```

Após a leitura do código, o handoff deve registrar quais contratos já existiam, quais arquivos foram realmente alterados, quais decisões foram ajustadas e quais verificações confirmaram os critérios de aceite.

## Regra resumida

> Use o SDD mínimo para definir intenção e aceite; use o handoff para executar, reconciliar e preservar memória; use código e testes para confirmar o comportamento real.
