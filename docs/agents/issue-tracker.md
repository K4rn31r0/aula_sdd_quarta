# Issue tracker: Local Markdown

Issues e specs deste repo ficam como arquivos markdown em `.scratch/`.

## Convenções

- Uma feature por diretório: `.scratch/<feature-slug>/`
- A spec é `.scratch/<feature-slug>/spec.md`
- Issues de implementação são um arquivo por ticket em `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numerados a partir de `01`
- A linha `Status:` fica próximo ao início de cada issue
- Comentários e histórico de conversa são acrescentados ao fim do arquivo sob o título `## Comments`

## Quando uma skill disser para publicar no issue tracker

Crie um novo arquivo em `.scratch/<feature-slug>/` e o diretório necessário.

## Quando uma skill disser para buscar um ticket

Leia o arquivo no caminho informado. O usuário normalmente passa o caminho ou o número da issue diretamente.

## Como fechar uma issue

Ao concluir uma issue:

- marque os critérios de aceite com `[x]`
- troque a linha `Status` para `done`
