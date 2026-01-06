FROM python:3.12-slim

WORKDIR /app

# Copiar o requirements.txt da RAIZ do projeto
COPY requirements.txt /app/requirements.txt

# Instalar dependências
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar código do ETL
COPY etl /app/etl

# Copiar dados (CSV bruto e pasta processed)
COPY data /app/data

# Comando padrão
CMD ["python", "etl/01_etl_clean_and_load.py"]
