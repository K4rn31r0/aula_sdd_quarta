# Domain Docs

Como as engineering skills devem consumir a documentação de domínio deste repositório durante a exploração do código.

## Antes de explorar, leia

- **`GLOSSARY.md`** na raiz, se existir
- **`GLOSSARY-MAP.md`** na raiz, se existir: aponta para um `GLOSSARY.md` por contexto
- **`docs/adr/`**: leia os ADRs relacionados à área em que vai trabalhar

Em repos com contexto único, não precisa verificar diretórios de ADR por contexto.

Se esses arquivos não existirem, prossiga silenciosamente. Não informe a ausência nem sugira criá-los antecipadamente. A skill `/domain-modeling`, acessada por `/grill-with-docs` e `/improve-codebase-architecture`, cria esses arquivos somente quando termos ou decisões forem efetivamente resolvidos.

## Estrutura

Repositório single-context:

```text
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── app/
```

## Use o vocabulário do glossary

Quando a saída nomear um conceito de domínio (em título de issue, proposta de refatoração, hipótese ou nome de teste), use o termo definido em `GLOSSARY.md`. Não troque por sinônimos que o glossary explicitamente evita.

Se o conceito necessário ainda não estiver no glossary, isso pode indicar falta de um termo. Não invente linguagem que o projeto não usa; registre a lacuna para `/domain-modeling`.

## Informe conflitos com ADRs

Se a saída contradizer um ADR existente, deixe o conflito explícito em vez de sobrescrevê-lo silenciosamente.
