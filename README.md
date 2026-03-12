# Docker Data Project

Projeto de ETL com `Python`, `Pandas`, `PostgreSQL` e `Docker` para simular um fluxo de dados de vendas do início ao fim: geração de dados brutos, limpeza, enriquecimento e carga em banco relacional.

## O que o projeto faz

- Gera um CSV sintético de vendas com inconsistências propositalmente inseridas
- Limpa e padroniza os dados
- Calcula a coluna `receita`
- Carrega o resultado na tabela `vendas` do PostgreSQL
- Reserva um notebook para análise exploratória dos dados

## Estrutura

```text
.
|-- docker-compose.yml
|-- etl/
|   |-- 00_generate_csv.py
|   |-- 01_etl_clean_and_load.py
|   `-- Dockerfile
|-- sql/
|   `-- 01_create_tables.sql
|-- notebook/
|   `-- 01_exploratory_analysis.ipynb
`-- requirements.txt
```

## Stack

- Python 3.12
- Pandas
- SQLAlchemy
- PostgreSQL 16
- Docker Compose

## Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.12+ instalado localmente caso você queira gerar o CSV fora do container

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com:

```env
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Como rodar

### 1. Criar as pastas de dados

O projeto grava arquivos em `data/raw` e `data/processed`. Crie essas pastas antes de executar:

```bash
mkdir -p data/raw data/processed
```

### 2. Gerar o CSV bruto

O ETL principal espera encontrar o arquivo `data/raw/vendas_raw.csv`. Gere esse arquivo com:

```bash
python3 etl/00_generate_csv.py
```

### 3. Subir o banco e executar o ETL

```bash
docker compose up --build
```

Esse comando:

- sobe o PostgreSQL
- cria a tabela `vendas` com o script em `sql/`
- executa o container `etl`
- limpa a tabela e carrega os dados tratados

## Fluxo do ETL

### Extração

Lê o arquivo `data/raw/vendas_raw.csv`.

### Transformação

- substitui `categoria` nula por `Desconhecida`
- remove espaços em branco da coluna `uf`
- substitui `uf` vazia por `NA`
- remove linhas com `quantidade <= 0`
- remove linhas com `preco_unit <= 0`
- calcula a coluna `receita`

### Carga

Insere os dados limpos na tabela `vendas` do PostgreSQL.

## Arquivos gerados

- `data/raw/vendas_raw.csv`: dados brutos gerados
- `data/processed/vendas_clean.csv`: dados limpos após o ETL

## Banco de dados

A tabela criada no PostgreSQL é:

- `vendas`

Ela possui colunas para data da venda, categoria, produto, quantidade, preço unitário, canal, UF e receita.

## Próximos passos sugeridos

- automatizar a geração do CSV dentro do fluxo Docker
- adicionar consultas SQL de validação
- expandir o notebook com gráficos e insights
- incluir testes para o pipeline
