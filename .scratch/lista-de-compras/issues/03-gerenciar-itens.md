# 03: Gerenciar itens da lista

**What to build:** adicionar, editar, marcar, desmarcar e remover itens dentro de uma lista, preservando ordem e validações.

**Blocked by:** 02: Gerenciar listas.

**Status:** done

- [x] Uma pessoa pode adicionar um nome obrigatório e uma quantidade opcional a uma lista.
- [x] Nomes de itens vazios ou acima de 100 caracteres são rejeitados.
- [x] Quantidades acima de 200 caracteres são rejeitadas.
- [x] Quantidades compostas apenas por espaços são persistidas como ausentes.
- [x] Itens equivalentes dentro da mesma lista são impedidos por caixa ou espaços externos.
- [x] Uma pessoa pode editar nome e quantidade sem transformar o item em duplicata.
- [x] Editar um item mantém seu estado comprado ou não comprado.
- [x] Conflitos de edição preservam os campos preenchidos no formulário.
- [x] Uma pessoa pode marcar um item como comprado e desmarcá-lo.
- [x] Itens comprados aparecem depois dos não comprados e com aparência riscada.
- [x] Os itens não comprados preservam sua ordem original de inserção.
- [x] Uma pessoa pode remover individualmente qualquer item sem confirmação.
- [x] Uma lista sem itens mostra orientação vazia e mantém a ação de adicionar item.
- [x] Testes do módulo de regras cobrem validação, unicidade, edição, estados, ordenação e remoção sem Flask ou HTTP.
