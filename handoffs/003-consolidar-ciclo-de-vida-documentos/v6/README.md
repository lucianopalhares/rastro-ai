# v6 — Corrigir execução dos testes da API

- Versão-base: `v4`; a `v5` foi descartada antes da aplicação.
- Data: 2026-10-23 | Status: `proposed`.
- Arquivos conferidos: `/home/dev/dev/ia/rastro-ai/rastro-api/package.json`, `/home/dev/dev/ia/rastro-ai/rastro-api/tsconfig.json` e `/home/dev/dev/ia/rastro-ai/rastro-api/src/modules/documents/domain/document.spec.ts`.
- Reconciliação: o teste de domínio já existe e permanece inalterado; `jest` e `nest` não estavam disponíveis e o pacote misturava Jest 30 com `ts-jest` 29.
- Pendências: aplicação manual e execução dos testes/build dentro do serviço Docker da API.

## Arquivo: `api/package.json`

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/package.json`
- Operação: `replace`
- Localização: `scripts.test`, `devDependencies.jest` e `devDependencies.@types/jest`.
- Âncoras: conteúdo completo do arquivo `package.json`.
- Motivo: alinhar Jest 29 com `ts-jest` 29 e declarar a configuração de transformação TypeScript.
- Impacto: instala um conjunto compatível e executa `document.spec.ts`; o código de produção permanece inalterado.
- Comentários: JSON estrito não aceita comentários; a alteração está documentada neste README.

## Arquivo: `api/jest.config.js`

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/jest.config.js`
- Operação: `insert`
- Localização: novo arquivo na raiz da API.
- Âncoras: arquivo inexistente; criar ao lado de `package.json`.
- Motivo: configurar `ts-jest` para transformar os testes TypeScript.
- Impacto: habilita a execução dos testes unitários em ambiente Node sem alterar o runtime.
- Comentário no código: uma explicação simples antecede o bloco novo e importante.

## Ordem e verificação

1. Aplicar `api/package.json`.
2. Aplicar `api/jest.config.js`.
3. Reconstruir a imagem com `docker compose build api`.
4. Executar `docker compose run --rm --no-deps api npm test -- --runInBand`.
5. Executar `docker compose run --rm --no-deps api npm run build`.
