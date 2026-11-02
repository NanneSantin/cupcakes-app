# Cupcakes Gourmet 🧁

Loja virtual de cupcakes desenvolvida no **Projeto Integrador Transdisciplinar em Engenharia de Software II**.

**Aluna:** Elaine Stefani Santini · **RGM:** 33146420

🔗 **Sistema publicado:** https://nannesantin.pythonanywhere.com

---

## Funcionalidades

**Cliente**
- Vitrine com fotos, filtro por categoria e página de detalhe
- Cadastro, login e logout, com validação dos dados
- Carrinho com botões − / +, total automático e adição sem recarregar a página
- Finalização do pedido com endereço e forma de pagamento
- **Pagamento simulado** por Pix ou cartão (aprovado e recusado)
- "Meus pedidos" com linha do tempo da entrega

**Administrador**
- Painel com todos os pedidos e filtro por status
- Alteração do status (Pago → Em preparo → Saiu para entrega → Entregue)
- Cancelamento com devolução dos produtos ao estoque

**Qualidade e segurança**
- Senhas gravadas como *hash*, proteção CSRF e controle de acesso por perfil
- Páginas de erro próprias (403, 404 e 500)
- 58 testes automatizados

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Back-end | Python 3 + Flask (padrão MVC) |
| Banco de dados | SQLite, via SQLAlchemy |
| Front-end | HTML, CSS e JavaScript + Bootstrap 5 |
| Autenticação e segurança | Flask-Login, Werkzeug (hash de senha), Flask-WTF (CSRF) |
| Testes | pytest |
| Hospedagem | PythonAnywhere (plano gratuito) |

## Estrutura do projeto

```
cupcakes-app/
├── backend/
│   ├── app/
│   │   ├── models/        → Model: entidades do banco
│   │   ├── controllers/   → Controller: rotas e regras de negócio
│   │   ├── validacoes.py  → regras de validação
│   │   └── seed.py        → carga inicial (produtos e admin)
│   ├── tests/             → testes automatizados (pytest)
│   ├── config.py
│   ├── requirements.txt
│   └── run.py             → inicia o servidor
├── frontend/
│   ├── templates/         → View: telas HTML (layouts, pages, components, errors, admin)
│   └── static/            → CSS, JavaScript e imagens
└── docs/                  → documentação do projeto
```

---

## Como testar o sistema publicado

Acesse **https://nannesantin.pythonanywhere.com** e use os dados abaixo.

| Para | Dados |
|---|---|
| Cliente | Crie uma conta em **Entrar → Cadastre-se** (endereço no formato *Rua das Flores, 100 - Centro, Curitiba*) |
| Administrador | E-mail `admin@cupcakes.com` · senha `admin123` → menu **Administrador → Painel de pedidos** |
| Pagamento aprovado (cartão) | `4111 1111 1111 1111` · validade `12/30` · CVV `123` |
| Pagamento recusado (cartão) | Qualquer número terminado em `0000` |
| Pix | Clique em "Já fiz o Pix (simular pagamento)" |

> ⚠️ **Os pagamentos são apenas simulados.** Nenhum valor é cobrado e os dados de cartão não são gravados. Não use dados reais.

Roteiro sugerido: vitrine e filtros → detalhe → cadastro → carrinho (− / +) → pedido com Pix → pedido com cartão → Meus pedidos → painel do admin (mudar status) → conferir o status como cliente → abrir um endereço inexistente (ex.: `/produto/999`).

**Sobre a hospedagem:** o site está no plano gratuito do PythonAnywhere, que precisa ser renovado mensalmente pelo painel. Se o endereço estiver fora do ar, o sistema pode ser executado localmente, como descrito abaixo.

---

## Como executar localmente

**Pré-requisitos:** [Python 3.12+](https://www.python.org/downloads/) e [Git](https://git-scm.com/).

```bash
# 1. Baixar o projeto
git clone https://github.com/NanneSantin/cupcakes-app.git
cd cupcakes-app

# 2. Criar e ativar o ambiente virtual
python -m venv venv
venv\Scripts\activate          # Windows (PowerShell)
# source venv/bin/activate     # Linux / macOS

# 3. Instalar as dependências
pip install -r backend/requirements.txt

# 4. Iniciar o servidor
python backend/run.py
```

Acesse **http://127.0.0.1:5000**.

- O banco `backend/cupcakes.db` é criado automaticamente na primeira execução, já com os 8 cupcakes e o usuário administrador.
- Para começar com o banco zerado, pare o servidor, apague `backend/cupcakes.db` e inicie de novo.
- No Windows, se a ativação do ambiente for bloqueada, rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Como rodar os testes automatizados

Com o ambiente virtual ativo, na raiz do projeto:

```bash
python -m pytest backend -v
```

Resultado esperado: **58 passed**. Os testes usam um banco em memória e não alteram o `cupcakes.db`.

| Arquivo | O que testa |
|---|---|
| `test_vitrine.py` | Vitrine, filtro, detalhe e páginas 404 |
| `test_auth.py` | Cadastro (com validações), login e logout |
| `test_carrinho.py` | Adicionar, atualizar, remover, estoque e quantidade inválida |
| `test_pedidos.py` | Checkout, pagamento Pix/cartão e acompanhamento |
| `test_admin.py` | Painel do admin, status e cancelamento |
| `test_seguranca.py` | Proteção CSRF |

---

## Documentação

| | |
|---|---|
| [Planejamento e requisitos](docs/01-planejamento/) | Revisão do PIT I, requisitos e backlog |
| [Modelagem UML](docs/02-modelagem-uml/) | Casos de uso, classes, sequência e atividades |
| [IHC](docs/03-ihc/) | Mapa de navegação, telas e mensagens |
| [Banco de dados](docs/04-banco-de-dados/) | DER, normalização, script SQL e dicionário de dados |
| [Testes](docs/05-testes/) | Testes automatizados e testes com usuários |
| [Laudo de qualidade](docs/06-laudo-qualidade/) | Erros encontrados, correções e evidências |

## Evoluções futuras
- Avaliação dos produtos pelos clientes
- Painel de estoque para o administrador
- Busca de endereço por CEP
- Cadastro de produtos pelo administrador
