# 02: Gerenciar listas

**What to build:** criar, abrir, renomear e excluir listas pela interface, com nomes únicos e persistência em arquivo JSON local.

**Blocked by:** 01: Criar esqueleto do aplicativo.

**Status:** done

- [x] Uma pessoa pode criar uma lista com nome obrigatório e único.
- [x] Nomes de listas vazios, com apenas espaços ou acima de 100 caracteres são rejeitados.
- [x] Espaços externos são removidos antes da persistência.
- [x] Diferenças de caixa e espaços externos não permitem nomes equivalentes.
- [x] Uma pessoa pode renomear uma lista sem aceitar o nome de outra lista.
- [x] Uma pessoa pode abrir uma lista pelo nome ou identificação visível na tela inicial.
- [x] Uma pessoa pode excluir uma lista somente após confirmar.
- [x] Conflitos de criação e renomeação preservam os dados digitados no formulário.
- [x] Mensagens claras informam nomes vazios, excessivamente longos e duplicados.
- [x] Listas e alterações são persistidas em um único arquivo JSON local.
- [x] Testes do módulo de regras cobrem criação, unicidade, normalização, renomeação e exclusão sem Flask ou HTTP.
- [x] A tela inicial vazia oferece uma ação clara para criar a primeira lista.
