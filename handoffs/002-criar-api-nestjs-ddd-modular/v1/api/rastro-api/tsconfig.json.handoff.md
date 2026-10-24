## Alteração: configuração TypeScript

- Arquivo original: `/home/dev/dev/ia/rastro-ai/rastro-api/tsconfig.json`
- Aplicação: `api`
- Localização: arquivo novo na raiz da aplicação
- Operação: `insert`
- Âncoras: arquivo inexistente; criar antes do primeiro build.
- Motivo: habilitar decorators do NestJS e aliases internos para a estrutura modular.
- Impacto: compila `src` para `dist` com checagem estrita.
- Pré-requisitos: nenhum.

### Código copiável

```json
{
  "compilerOptions": {
    "module": "commonjs",
    "declaration": true,
    "removeComments": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "allowSyntheticDefaultImports": true,
    "target": "ES2023",
    "sourceMap": true,
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": true,
    "skipLibCheck": true,
    "strict": true,
    "strictNullChecks": true,
    "noImplicitAny": true,
    "strictBindCallApply": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "paths": {
      "@/*": ["src/*"]
    }
  }
}
```

### Verificação

`npx tsc --noEmit` deve concluir sem erros depois que os demais arquivos forem aplicados.
