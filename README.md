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
- Matplotlib
- SQLAlchemy
- nbclient
- nbformat
- PostgreSQL 16
- Docker Compose

## Pré-requisitos

- Docker e Docker Compose instalados

## Variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com:

```env
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

## Como rodar

### 1. Subir o banco e executar o pipeline completo

```bash
docker compose up --build
```

Esse comando:

- sobe o PostgreSQL
- cria a tabela `vendas` com o script em `sql/`
- executa o job `generate_raw`
- executa o job `etl`
- gera `data/raw/vendas_raw.csv` no host
- gera `data/processed/vendas_clean.csv` no host
- limpa a tabela e carrega os dados tratados

O pipeline agora é 100% executável via Docker. Não é mais necessário gerar o CSV bruto manualmente antes do Compose.

## Como executar o notebook

Depois de rodar o ETL e carregar os dados no PostgreSQL, voce pode abrir o notebook:

```bash
jupyter notebook notebook/01_exploratory_analysis.ipynb
```

O notebook:

- carrega as credenciais do arquivo `.env`
- consulta a tabela `vendas` no PostgreSQL
- gera tabelas-resumo e graficos de exploracao

Se quiser executar todas as celulas de forma automatica, use um ambiente com as dependencias de `requirements.txt` instaladas.

## Fluxo do ETL

### Geração do bruto

O job `generate_raw` cria o arquivo `data/raw/vendas_raw.csv`.

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

- `data/raw/vendas_raw.csv`: dados brutos gerados pelo job Docker `generate_raw`
- `data/processed/vendas_clean.csv`: dados limpos gerados pelo job Docker `etl`

Os arquivos são salvos dentro do container em `/app/data/...` e persistidos no host via bind mount em `data/...`.

## Banco de dados

A tabela criada no PostgreSQL é:

- `vendas`

Ela possui colunas para data da venda, categoria, produto, quantidade, preço unitário, canal, UF e receita.

## Próximos passos sugeridos

- adicionar consultas SQL de validação
- expandir o notebook com gráficos e insights
- incluir testes para o pipeline
- considerar um serviço de visualização ou BI para consumir a tabela `vendas`
