CREATE TABLE IF NOT EXISTS vendas (
  id SERIAL PRIMARY KEY,
  data_venda DATE NOT NULL,
  categoria TEXT NOT NULL,
  produto TEXT NOT NULL,
  quantidade INT NOT NULL CHECK (quantidade > 0),
  preco_unit NUMERIC(10,2) NOT NULL CHECK (preco_unit > 0),
  canal TEXT NOT NULL,
  uf TEXT NOT NULL,
  receita NUMERIC(12,2) NOT NULL
);
