FROM python:3.12-slim AS runtime

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt

COPY etl /app/etl

CMD ["python", "etl/01_etl_clean_and_load.py"]
