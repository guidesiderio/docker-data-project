import os
import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text


# =========================
# Funções utilitárias
# =========================
def require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Variável de ambiente '{name}' não definida. "
            "Defina no seu .env (não versionado) e/ou exporte no terminal."
        )
    return value


# =========================
# Caminhos
# =========================
RAW_PATH = Path("./data/raw/vendas_raw.csv")
PROCESSED_DIR = Path("./data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = PROCESSED_DIR / "vendas_clean.csv"

# =========================
# Configuração do banco (SEM defaults sensíveis)
# =========================
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

DB_NAME = require_env("POSTGRES_DB")
DB_USER = require_env("POSTGRES_USER")
DB_PASS = require_env("POSTGRES_PASSWORD")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# =========================
# 1) EXTRACT
# =========================
df = pd.read_csv(RAW_PATH, parse_dates=["data_venda"])

# =========================
# 2) TRANSFORM
# =========================
df["categoria"] = df["categoria"].fillna("Desconhecida")

df["uf"] = df["uf"].astype(str).str.strip()
df.loc[df["uf"] == "", "uf"] = "NA"

df = df[(df["quantidade"] > 0) & (df["preco_unit"] > 0)].copy()

df["receita"] = (df["quantidade"] * df["preco_unit"]).round(2)
df = df.sort_values("data_venda")

# Exportar dataset limpo
df.to_csv(OUTPUT_PATH, index=False)

# =========================
# 3) LOAD
# =========================
# Pressupõe que a tabela 'vendas' já existe (DDL versionado em /sql)
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE vendas RESTART IDENTITY;"))

df.to_sql("vendas", engine, if_exists="append", index=False)

print("ETL concluído com sucesso (clean + load)")
print(f"Linhas carregadas: {len(df)}")
print(f"CSV limpo salvo em: {OUTPUT_PATH.resolve()}")
