# 01 – Planejamento (revisão do PIT I)

## Situação-problema
Uma loja de cupcakes gourmet precisa de uma aplicação para que os clientes **vejam os produtos, façam pedidos, realizem pagamentos e acompanhem a entrega**. No PIT I foram levantados os requisitos, escritas 15 histórias de usuário e montado o backlog priorizado, organizado nos temas: Cadastro e Acesso, Vitrine e Produtos, Carrinho e Pedido, Entrega e Pagamento, Acompanhamento e Administração.

## Ajustes de escopo feitos no PIT II (Kaizen)

| Planejado no PIT I | Decisão no PIT II | Motivo |
|---|---|---|
| Aplicativo mobile | **Aplicação web responsiva** (funciona no celular e no computador) | Uma única base de código, hospedagem gratuita e acesso por qualquer navegador, sem instalação |
| Pagamento integrado | **Pagamento simulado** (Pix e cartão) | O desafio pede apenas a simulação; nenhum dado de pagamento é gravado |
| Papel de entregador | **Status da entrega controlado pelo administrador** | Simplifica o MVP sem perder o acompanhamento da entrega pelo cliente |
| Cadastro de produtos pelo admin | **Carga inicial de produtos** no banco | Priorização do fluxo de compra dentro do prazo; CRUD de produtos fica para evolução |

## Requisitos funcionais implementados

| ID | Requisito | Tema | Situação |
|---|---|---|---|
| RF01 | Exibir a vitrine de cupcakes com foto, descrição e preço | Vitrine e Produtos | ✅ |
| RF02 | Filtrar produtos por categoria | Vitrine e Produtos | ✅ |
| RF03 | Exibir o detalhe do produto | Vitrine e Produtos | ✅ |
| RF04 | Cadastrar cliente com validação dos dados | Cadastro e Acesso | ✅ |
| RF05 | Login e logout | Cadastro e Acesso | ✅ |
| RF06 | Adicionar produtos ao carrinho (vitrine e detalhe), com quantidade | Carrinho e Pedido | ✅ |
| RF07 | Alterar quantidade e remover itens do carrinho, com total automático | Carrinho e Pedido | ✅ |
| RF08 | Finalizar pedido informando endereço e forma de pagamento | Carrinho e Pedido | ✅ |
| RF09 | Pagamento simulado por Pix ou cartão (aprovação e recusa) | Entrega e Pagamento | ✅ |
| RF10 | Baixar o estoque ao finalizar o pedido | Carrinho e Pedido | ✅ |
| RF11 | Listar os pedidos do cliente | Acompanhamento | ✅ |
| RF12 | Acompanhar o pedido por linha do tempo (Aguardando pagamento → Entregue) | Acompanhamento | ✅ |
| RF13 | Painel do administrador com todos os pedidos e filtro por status | Administração | ✅ |
| RF14 | Alterar o status do pedido (admin) | Administração | ✅ |
| RF15 | Cancelar pedido devolvendo os produtos ao estoque | Administração | ✅ |

## Requisitos não funcionais

| ID | Requisito | Como foi atendido |
|---|---|---|
| RNF01 | Interface responsiva | Bootstrap 5; testado em celular (Chrome e Safari) e computador |
| RNF02 | Segurança das senhas | Senhas gravadas apenas como *hash* (Werkzeug) |
| RNF03 | Controle de acesso | Login obrigatório no checkout e nos pedidos; painel restrito ao admin (erro 403) |
| RNF04 | Proteção contra ataques comuns | Token CSRF em todos os formulários; redirecionamentos só para páginas internas |
| RNF05 | Tratamento de erros | Páginas próprias para 403, 404 e 500; mensagens claras de validação |
| RNF06 | Qualidade | 58 testes automatizados (pytest) e testes com 6 usuários |

## Evoluções futuras (backlog)
Sugeridas nos testes com usuários e registradas no [laudo de qualidade](../06-laudo-qualidade/):
- Avaliação dos produtos pelos clientes.
- Painel de estoque para o administrador (consulta e reposição; a baixa automática já existe).
- Busca de endereço por CEP.
- Cadastro e edição de produtos pelo administrador.
