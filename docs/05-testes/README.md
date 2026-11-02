# 05 – Testes

A qualidade foi verificada em dois níveis, seguindo o Modelo V:

| Nível | Como | Resultado |
|---|---|---|
| **Testes unitários e de integração** (verificação) | 58 testes automatizados com **pytest**, usando um banco em memória | 58 aprovados |
| **Testes de aceitação** (validação) | 6 pessoas testaram o sistema publicado seguindo um roteiro e responderam um formulário | 72 de 72 verificações "Funcionou"; nota de facilidade de uso 5/5 |

## 1. Testes automatizados (pytest)

Como executar (na raiz do projeto, com o ambiente virtual ativo):
```bash
python -m pytest backend -v
```
Resultado completo: [`resultado-pytest.txt`](resultado-pytest.txt).

| Arquivo | Qtd. | O que verifica |
|---|---|---|
| `test_vitrine.py` | 5 | Listagem, filtro por categoria, detalhe do produto e erros 404 |
| `test_auth.py` | 12 | Cadastro válido e inválido (senha, e-mail repetido, campos vazios, endereço, nome), login, logout e admin |
| `test_carrinho.py` | 17 | Adicionar, somar, limite de estoque, atualizar, remover, total, respostas JSON, quantidade inválida e redirecionamento seguro |
| `test_pedidos.py` | 12 | Checkout com login, validações, baixa de estoque, Pix, cartão válido/inválido/recusado, meus pedidos e isolamento entre clientes |
| `test_admin.py` | 9 | Acesso restrito, alteração de status visível ao cliente, status inválido, cancelamento com devolução ao estoque e retorno ao painel |
| `test_seguranca.py` | 3 | Bloqueio de formulários sem token CSRF, presença do token nas páginas e funcionamento em HTTPS sem cabeçalho Referer |
| **Total** | **58** | |

## 2. Testes com usuários

- **Formulário:** Google Forms com roteiro de 12 passos, grade "Funcionou / Não funcionou / Não testei", campos para bugs, sugestões, nota de 1 a 5 e prints.
- **Ambiente:** sistema publicado em https://nannesantin.pythonanywhere.com
- **Participantes:** 6 pessoas, em celular (Chrome e Safari) e computador (Chrome e Edge).

| Testador | Data | Aparelho / navegador | Resultado da grade | Problemas e sugestões |
|---|---|---|---|---|
| Suellen Priscilla de Camargo | 29/10/2026 | Celular / Chrome | 12 de 12 funcionaram | Página voltava ao topo ao adicionar; sugeriu botões +1/−1 |
| Luiz Felipe Bini | 29/10/2026 | Computador / Chrome | 12 de 12 funcionaram | 4 bugs (quantidade, endereço, confirmação, CSRF) e 6 sugestões, com relatório em PDF |
| Janaina Ferreira | 29/10/2026 | Celular / Safari | 12 de 12 funcionaram | Painel do admin voltava para a vitrine ao mudar status |
| Matheus Nunes | 29/10/2026 | Computador / Edge | 12 de 12 funcionaram | Nenhum bug |
| Thais Prado | 30/10/2026 | Computador / Chrome | 12 de 12 funcionaram | Nenhum bug |
| Alyssa Mey Tsutsumi | 30/10/2026 | Celular / Safari | 12 de 12 funcionaram | Sugeriu avaliação de produtos e controle de estoque (evolução futura) |

Os problemas encontrados, as correções e as evidências estão no [laudo de qualidade](../06-laudo-qualidade/).
