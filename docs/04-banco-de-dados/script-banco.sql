-- =============================================================
-- Cupcakes Gourmet – Projeto físico do banco de dados (SQLite)
-- Gerado a partir dos models do SQLAlchemy (backend/app/models)
-- Na aplicação, as tabelas são criadas automaticamente por db.create_all()
-- =============================================================

CREATE TABLE categoria (
    id      INTEGER      NOT NULL,
    nome    VARCHAR(50)  NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (nome)
);

CREATE TABLE usuario (
    id          INTEGER       NOT NULL,
    nome        VARCHAR(100)  NOT NULL,
    email       VARCHAR(120)  NOT NULL,
    senha_hash  VARCHAR(255)  NOT NULL,
    telefone    VARCHAR(20),
    endereco    VARCHAR(255),
    is_admin    BOOLEAN       NOT NULL,
    criado_em   DATETIME,
    PRIMARY KEY (id),
    UNIQUE (email)
);

CREATE TABLE produto (
    id            INTEGER        NOT NULL,
    nome          VARCHAR(100)   NOT NULL,
    descricao     TEXT,
    preco         NUMERIC(8, 2)  NOT NULL,
    estoque       INTEGER        NOT NULL,
    ativo         BOOLEAN        NOT NULL,
    imagem        VARCHAR(100),
    categoria_id  INTEGER        NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (categoria_id) REFERENCES categoria (id)
);

CREATE TABLE pedido (
    id                INTEGER         NOT NULL,
    usuario_id        INTEGER         NOT NULL,
    data_pedido       DATETIME,
    status            VARCHAR(30)     NOT NULL,
    endereco_entrega  VARCHAR(255)    NOT NULL,
    forma_pagamento   VARCHAR(20),
    valor_total       NUMERIC(10, 2)  NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (usuario_id) REFERENCES usuario (id)
);

CREATE TABLE item_pedido (
    id              INTEGER        NOT NULL,
    pedido_id       INTEGER        NOT NULL,
    produto_id      INTEGER        NOT NULL,
    quantidade      INTEGER        NOT NULL,
    preco_unitario  NUMERIC(8, 2)  NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (pedido_id)  REFERENCES pedido (id),
    FOREIGN KEY (produto_id) REFERENCES produto (id)
);

-- -------------------------------------------------------------
-- Carga inicial (backend/app/seed.py)
-- -------------------------------------------------------------
INSERT INTO categoria (id, nome) VALUES (1, 'Clássicos'), (2, 'Frutas'), (3, 'Especiais');

INSERT INTO produto (nome, descricao, preco, estoque, ativo, imagem, categoria_id) VALUES
('Baunilha',        'Massa de baunilha com cobertura de buttercream e chocolate branco.', 9.90,  50, 1, 'baunilha.jpg',        1),
('Chocolate Belga', 'Massa de cacau com ganache de chocolate belga.',                    11.90, 50, 1, 'chocolate-belga.jpg', 1),
('Red Velvet',      'Massa aveludada com cobertura de cream cheese.',                    12.90, 50, 1, 'red-velvet.jpg',      1),
('Morango',         'Massa e cobertura de morango com calda da fruta.',                  11.50, 50, 1, 'morango.jpg',         2),
('Limão Siciliano', 'Massa cítrica com creme e calda de limão siciliano.',               11.50, 50, 1, 'limao-siciliano.jpg', 2),
('Doce de Leite',   'Cobertura cremosa de doce de leite com castanhas.',                 13.90, 50, 1, 'doce-de-leite.jpg',   3),
('Pistache',        'Massa de pistache com cobertura de chocolate branco.',              15.90, 50, 1, 'pistache.jpg',        3),
('Avelã',           'Massa de chocolate com creme de avelã e avelãs picadas.',           14.90, 50, 1, 'avela.jpg',           3);

-- Usuário administrador (a senha é gravada como hash pela aplicação: admin123)

-- -------------------------------------------------------------
-- Consultas úteis
-- -------------------------------------------------------------
-- Pedidos com nome do cliente e quantidade de itens
-- SELECT p.id, u.nome, p.status, p.valor_total, SUM(i.quantidade) AS itens
--   FROM pedido p
--   JOIN usuario u      ON u.id = p.usuario_id
--   JOIN item_pedido i  ON i.pedido_id = p.id
--  GROUP BY p.id ORDER BY p.data_pedido DESC;

-- Produtos mais vendidos (exceto pedidos cancelados)
-- SELECT pr.nome, SUM(i.quantidade) AS vendidos
--   FROM item_pedido i
--   JOIN produto pr ON pr.id = i.produto_id
--   JOIN pedido  p  ON p.id  = i.pedido_id
--  WHERE p.status <> 'Cancelado'
--  GROUP BY pr.nome ORDER BY vendidos DESC;
