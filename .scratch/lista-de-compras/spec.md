# Especificação: Lista de Compras

Status: ready-for-agent

## Problem Statement

Usuários precisam organizar suas compras sem depender de serviços externos, autenticação ou banco de dados. Precisam criar várias listas, controlar os produtos necessários, diferenciar o que já foi comprado e reutilizar listas anteriores em novas compras.

Na ausência da funcionalidade, o usuário não tem uma forma simples de manter listas separadas, evitar produtos repetidos, acompanhar o progresso da compra e reaproveitar uma lista já utilizada.

## Solution

O aplicativo permitirá criar, abrir, renomear, copiar e excluir listas de compras em uma interface web simples e adaptada a dispositivos móveis.

Cada lista conterá itens únicos com nome e quantidade opcional. O usuário poderá adicionar, editar, marcar, desmarcar e remover itens, além de limpar todos os itens já comprados ou reutilizar a lista desmarcando todos os itens.

Os dados serão persistidos apenas em arquivo JSON local. A interface será construída com Flask e templates Jinja2, sem JavaScript de framework e sem biblioteca de componentes. As regras das listas deverão existir em um módulo independente da interface HTTP.

## User Stories

1. Como usuária, quero criar uma lista informando seu nome, para organizar uma compra separada.
2. Como usuário, quero ver todas as minhas listas na tela inicial, para escolher rapidamente a compra que vou fazer.
3. Como usuária, quero abrir uma lista, para visualizar e administrar seus itens.
4. Como usuário, quero renomear uma lista, para corrigir ou atualizar seu propósito.
5. Como usuária, quero excluir uma lista, para remover uma compra que não desejo mais manter.
6. Como usuário, quero confirmar antes de excluir uma lista, para evitar remoções acidentais.
7. Como usuária, quero impedir o uso de nomes vazios em listas, para manter todas elas identificáveis.
8. Como usuário, quero impedir nomes de listas com mais de 100 caracteres, para manter a interface legível.
9. Como usuária, quero impedir duas listas com nomes iguais, para evitar ambiguidade.
10. Como usuário, quero que nomes como “Mercado” e “ mercado ” sejam considerados o mesmo nome, para impedir duplicatas com diferença apenas de caixa ou espaço externo.
11. Como usuária, quero que nomes sejam comparados sem diferenciar maiúsculas e minúsculas, para evitar duplicidades involuntárias.
12. Como usuário, quero continuar vendo os dados preenchidos quando uma operação tiver conflito de nome, para corrigir o formulário sem perder minha entrada.
13. Como usuária, quero receber uma mensagem clara quando tentar usar um nome de lista já existente, para entender por que a operação não foi concluída.
14. Como usuário, quero copiar uma lista antiga, para reutilizar sua estrutura em uma nova compra sem alterar a original.
15. Como usuária, quero que os itens da cópia comecem como não comprados, para realizar uma compra nova do zero.
16. Como usuário, quero que a cópia mantenha o nome da lista original seguido de “(cópia)”, para identificar sua origem.
17. Como usuária, quero que nomes sequenciais de cópias sejam únicos, para distinguir várias cópias da mesma lista.
18. Como usuário, quero que uma segunda cópia se chame “Nome (cópia 2)”, uma terceira “Nome (cópia 3)” e assim por diante, para ter nomes previsíveis.
19. Como usuária, quero reutilizar uma lista diretamente, para fazer uma nova compra sem criar outra lista.
20. Como usuário, quero que reutilizar desmarque todos os itens da lista original, para iniciar uma nova passagem pelos itens.
21. Como usuária, quero confirmar antes de reutilizar uma lista, para evitar a perda acidental do progresso da compra atual.
22. Como usuário, quero limpar os itens comprados de uma lista, para remover o que já foi adquirido sem perder os itens pendentes.
23. Como usuária, quero confirmar antes de limpar todos os itens comprados, para evitar remoções em massa acidentais.
24. Como usuário, quero remover um item comprado individualmente sem confirmação adicional, para agilizar a manutenção da lista.
25. Como usuária, quero adicionar um item informando nome e quantidade opcional, para registrar o que preciso comprar.
26. Como usuário, quero que o nome do item seja obrigatório, para evitar entradas sem identificação.
27. Como usuária, quero impedir nomes de itens com mais de 100 caracteres, para manter a leitura consistente.
28. Como usuário, quero informar uma quantidade como texto livre, para registrar formatos como “2 kg”, “1 caixa” ou “3”.
29. Como usuária, quero que o campo de quantidade aceite até 200 caracteres, para permitir descrições úteis sem campos excessivamente grandes.
30. Como usuário, quero que uma quantidade composta apenas por espaços seja tratada como quantidade ausente, para não criar dados sem significado.
31. Como usuária, quero impedir itens repetidos dentro da mesma lista, para evitar duplicidade durante a compra.
32. Como usuário, quero que “Arroz” e “ arroz ” sejam considerados o mesmo item, para impedir duplicatas apenas por caixa ou espaços externos.
33. Como usuária, quero que um item não possa ser duplicado por diferença de maiúsculas ou minúsculas, para manter a unicidade previsível.
34. Como usuário, quero receber uma mensagem clara ao tentar adicionar ou editar um item já existente, para corrigir o conflito.
35. Como usuária, quero editar o nome e a quantidade de um item, para corrigir informações sem criar outro registro.
36. Como usuário, quero que editar um item mantenha seu estado comprado ou não comprado, para não perder o progresso.
37. Como usuária, quero preservar o nome e a quantidade preenchidos quando a edição tiver um conflito, para corrigir apenas o dado necessário.
38. Como usuário, quero cancelar a edição de um item, para descartar alterações não desejadas.
39. Como usuária, quero marcar um item como comprado, para acompanhar o progresso durante o mercado.
40. Como usuário, quero desmarcar um item comprado, para corrigir um clique ou acrescentar o produto novamente à compra pendente.
41. Como usuária, quero remover um item diretamente, para excluí-lo sem fluxo de confirmação adicional.
42. Como usuário, quero que os itens não comprados mantenham a ordem original em que foram adicionados, para comprar de forma previsível.
43. Como usuária, quero que cada item marcado como comprado seja movido visualmente para o fim da lista, para separar o que já foi adquirido.
44. Como usuário, quero que itens comprados continuem visíveis com aparência riscada, para saber o que já foi comprado sem perder a lista.
45. Como usuária, quero poder desmarcar um item comprado mesmo após ele ter sido movido ao fim da lista, para corrigir seu estado.
46. Como usuário, quero ver uma orientação na tela inicial quando não houver listas, para entender imediatamente como começar.
47. Como usuária, quero ver uma ação clara para criar minha primeira lista, para não precisar descobrir o fluxo por tentativa.
48. Como usuário, quero ver uma orientação vazia na tela de uma lista sem itens, para saber que ela está pronta para receber produtos.
49. Como usuária, quero continuar vendo o formulário ou botão de adicionar item quando a lista estiver vazia, para iniciar o preenchimento rapidamente.
50. Como usuário, quero receber uma mensagem breve após criar uma lista, para confirmar que a operação foi concluída.
51. Como usuária, quero receber uma mensagem breve após renomear uma lista, para confirmar a alteração.
52. Como usuário, quero receber uma mensagem breve após copiar uma lista, para localizar o novo nome.
53. Como usuária, quero receber uma mensagem breve após reutilizar uma lista, para confirmar que todos os itens foram desmarcados.
54. Como usuário, quero receber uma mensagem breve após excluir uma lista ou limpar itens comprados, para confirmar a conclusão.
55. Como usuária, quero cancelar a criação ou renomeação de uma lista, para voltar sem alterar os dados existentes.
56. Como usuário, quero navegar pelo aplicativo em uma tela pequena, para usar o aplicativo enquanto faço compras.
57. Como usuária, quero encontrar ações principais com poucos passos, para concluir tarefas com rapidez.
58. Como usuário, quero usar o aplicativo sem login, para começar imediatamente.
59. Como usuária, quero que os dados permaneçam após recarregar a página, para não perder minhas listas em uma nova visita.
60. Como usuário, quero que apenas uma pessoa usando o aplicativo no ambiente local veja as listas persistidas, para manter o comportamento simples do MVP.

## Implementation Decisions

- O produto terá o conceito de lista e o conceito de item como entidades distintas.
- Uma lista terá nome obrigatório e único, com até 100 caracteres.
- O nome da lista será normalizado para validação aparando espaços nas extremidades e ignorando diferenças de maiúsculas e minúsculas.
- Nomes vazios, depois da normalização, serão inválidos.
- Ao persistir nomes válidos, preservar-se-á a entrada original sem espaços externos.
- Um item pertencerá a uma única lista e terá nome obrigatório e único dentro dessa lista.
- O nome do item terá até 100 caracteres e seguirá a mesma normalização usada para nomes de listas.
- O nome do item não poderá ficar vazio após a aparagem de espaços.
- Um item poderá ter quantidade opcional com até 200 caracteres.
- A quantidade será texto livre.
- Uma quantidade composta apenas por espaços será normalizada como ausência de quantidade.
- Itens repetidos dentro da mesma lista serão rejeitados pela regra de nome normalizado.
- A mesma operação de edição não pode tornar dois itens de uma lista equivalentes pelo nome normalizado.
- A edição de um item deve preservar seu estado comprado.
- Itens manterão uma posição ou ordem de inserção original.
- Os itens não comprados aparecerão antes dos comprados e cada novo estado comprado o moverá para o final dos itens comprados.
- Desmarcar um item comprado fará com que ele seja considerado não comprado e retorne à região de itens pendentes, preservando a ordem de inserção original.
- A interface inicial mostrará as listas existentes e uma ação principal para criação.
- Abrir uma lista mostrará seus itens e as ações de edição, exclusão, marcação e reutilização.
- Criar e renomear listas terá formulários simples com salvar e cancelar.
- Criar uma lista exigirá nome válido e único.
- Renomear uma lista exigirá nome válido e único, excluindo a própria lista da comparação.
- Adicionar um item exigirá nome válido e único dentro da lista.
- Editar um item exigirá nome válido e único dentro da lista, excluindo o próprio item da comparação.
- Conflitos de unicidade ou limites não devem alterar os dados persistidos e devem retornar ao usuário uma mensagem específica.
- Ao ocorrer conflito em criação ou edição, os campos preenchidos deverão permanecer no formulário.
- Copiar uma lista criará uma nova lista com todos os itens da origem, mas todos os itens ficarão como não comprados.
- A cópia não modificará nem excluirá a lista original.
- O nome-base da cópia será o nome da origem seguido de “(cópia)”.
- O sistema escolherá o menor sufixo disponível para evitar duplicidade: “(cópia)”, “(cópia 2)”, “(cópia 3)” e assim por diante.
- A operação de cópia deverá validar o nome sugerido contra todas as listas existentes antes de persistir.
- Reutilizar uma lista alterará somente os estados dos itens da lista original para não comprado.
- Reutilizar não criará uma nova lista, não renomeará a lista e não removerá itens.
- Limpar comprados removerá todos os itens cujo estado seja comprado e preservará todos os itens não comprados.
- Excluir uma lista removerá a lista e todos os itens nela contidos.
- Remover um item individual removerá apenas aquele item.
- Exclusão de lista, reutilização e limpeza de comprados exigirão confirmação na interface.
- A remoção individual de item será imediata.
- A tela vazia de listas oferecerá uma ação para criar a primeira lista.
- A tela vazia de uma lista oferecerá uma orientação e manterá disponível a ação de adicionar item.
- A operação bem-sucedida exibirá uma mensagem breve de feedback.
- Após cada operação de confirmação positiva, o usuário deverá permanecer em uma tela coerente com o novo estado, sem fluxo extra além da ação solicitada.
- Cancelar qualquer criação ou edição levará de volta à tela anterior sem salvar alteração.
- Não haverá autenticação, login ou separação de dados por usuário.
- Não haverá banco de dados.
- Não haverá limites globais arbitrários além dos limites explícitos de nomes e quantidades.
- O produto não implementará busca, filtros por categoria, compartilhamento, histórico de compras, sugestões, ordens de mercado ou funcionalidades de acessibilidade avançada além do uso básico de HTML semântico.
- Persistência ocorrerá em um único arquivo JSON local no diretório da aplicação.
- A interface usará Flask, templates Jinja2 e CSS próprio.
- O HTML será renderizado no servidor.
- Não será utilizado framework JavaScript nem biblioteca de componentes de interface.

## Testing Decisions

- A principal seam de testes será o módulo de regras das listas, sem inicializar Flask e sem realizar requisições HTTP.
- Os testes deverão chamar operações do módulo de regras e verificar o estado devolvido ou persistido, incluindo retornos de validação e conflitos.
- As mensagens exibidas pela interface não serão consideradas prova suficiente da regra: testes de regras verificarão diretamente nomes duplicados, estados e dados resultantes.
- O módulo de regras deverá ser testado com dados isolados e sem depender do arquivo real do usuário.
- Os testes deverão cobrir a interface externa e comportamental do módulo, não detalhes internos de coleções ou funções auxiliares.
- Um bom teste cria um conjunto mínimo de listas ou itens, executa uma operação e afirma o estado observável após essa operação.
- Os testes não deverão depender da implementação específica de JSON, exceções internas ou da estrutura completa das classes internas.
- Quando houver persistência envolvida, o teste deverá separar a carga e a gravação, usando uma fonte temporária controlada, sem acessar o arquivo real da aplicação.

Casos essenciais de testes:

- Criar uma lista com nome válido.
- Impedir lista sem nome ou formada apenas por espaços.
- Impedir lista com nome acima de 100 caracteres.
- Impedir nome de lista duplicado por caixa ou espaços externos.
- Renomear uma lista preservando o nome original em caso de conflito.
- Copiar uma lista mantendo itens e estados como não comprados.
- Gerar “(cópia)”, “(cópia 2)” e “(cópia 3)” quando os nomes já existirem.
- Reutilizar uma lista desmarcando todos os itens sem remover nem renomear.
- Limpar comprados removendo apenas os itens marcados.
- Excluir uma lista removendo também seus itens.
- Adicionar um item válido com quantidade opcional.
- Impedir item sem nome ou formado apenas por espaços.
- Impedir item com nome acima de 100 caracteres.
- Impedir item com quantidade acima de 200 caracteres.
- Normalizar quantidade formada apenas por espaços como ausente.
- Impedir dois itens equivalentes na mesma lista por caixa ou espaços externos.
- Editar um item sem criar duplicata e mantendo seu estado comprado.
- Impedir editar um item para o nome de outro item da mesma lista.
- Marcar um item e movê-lo após os itens não comprados.
- Desmarcar um item e retorná-lo à região não comprada.
- Preservar a ordem de inserção dos itens não comprados.
- Remover individualmente um item sem afetar os demais.
- Exibir valores vazios ou inválidos sem alterar o estado persistido.
- Garantir que operações sobre uma lista inexistente não corrompam nem criem dados.

O desenho da suíte deverá preferir o menor número possível de pontos de montagem. A única seam esperada é o módulo de regras das listas. Testes externos de navegador e HTTP não são necessários para a especificação das regras.

## Out of Scope

- Login, cadastro e perfil de usuário.
- Banco de dados ou armazenamento remoto.
- Sincronização entre dispositivos.
- Compartilhamento de listas.
- Trabalho colaborativo.
- Histórico de alterações e desfazer geral.
- Categorias e ordenação automática por categoria.
- Busca e filtros.
- Sugestões automáticas de produtos.
- Quantidades com unidades estruturadas ou validação numérica.
- Conversão de unidades.
- API pública.
- Aplicativo móvel nativo.
- Framework JavaScript ou biblioteca de interface.
- Tema claro/escuro.
- Animações complexas.
- Acessibilidade além das práticas básicas de HTML semântico e interface utilizável por teclado.

## Further Notes

- Se houver divergência entre a especificação e uma implementação futura, prevalecerá o comportamento descrito neste documento.
- A normalização de nomes será usada apenas para unicidade e validação; a lista deverá apresentar ao usuário o texto escolhido, sem espaços externos.
- A comparação não diferencia maiúsculas e minúsculas, mas não deverá realizar transliterações ou substituições além da aparagem e da normalização de caixa disponível na plataforma.
- O aplicativo deverá falhar de forma segura em dados ausentes ou inválidos do arquivo JSON local, sem introduzir comportamentos de conta ou banco de dados.
- Qualquer interface criada posteriormente deverá continuar recebendo os conflitos e validações emitidos pelo módulo de regras, em vez de reimplementar regras de unicidade ou limite.
- Os estados de confirmação pertencem à interface: o módulo de regras aceitará a operação já confirmada pelo usuário e realizará apenas a alteração solicitada.
