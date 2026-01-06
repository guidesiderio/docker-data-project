import pandas as pd
import numpy as np
from pathlib import Path

# Reprodutibilidade
rng = np.random.default_rng(42)

# Parâmetros
n = 2000
datas = pd.date_range("2025-01-01", "2025-12-31", freq="D")
categorias = ["Eletrônicos", "Moda", "Casa", "Beleza"]
produtos = ["Produto A", "Produto B", "Produto C", "Produto D", "Produto E"]
canais = ["Site", "App", "Marketplace"]
ufs = ["PI", "CE", "MA", "BA", "PE", "SP", "RJ"]

# Dataset base
df = pd.DataFrame(
    {
        "data_venda": rng.choice(datas, size=n),
        "categoria": rng.choice(categorias, size=n),
        "produto": rng.choice(produtos, size=n),
        "quantidade": rng.integers(1, 6, size=n),
        "preco_unit": rng.choice([19.9, 29.9, 59.9, 99.9, 199.9, 399.9], size=n),
        "canal": rng.choice(canais, size=n),
        "uf": rng.choice(ufs, size=n),
    }
)

# Inserir sujeira proposital
idx = rng.choice(df.index, size=60, replace=False)
df.loc[idx[:20], "quantidade"] = 0  # inválido
df.loc[idx[20:40], "preco_unit"] = -29.9  # inválido
df.loc[idx[40:50], "categoria"] = None  # nulos
df.loc[idx[50:60], "uf"] = " "  # lixo

# Garantir pasta
output_dir = Path("./data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

# Exportar CSV bruto
output_path = output_dir / "vendas_raw.csv"
df.to_csv(output_path, index=False)

print(f"CSV bruto gerado em: {output_path.resolve()}")
print(f"Total de registros: {len(df)}")


df = pd.read_csv("./data/raw/vendas_raw.csv")

print(df.info())
print("\nQuantidade inválida:", (df["quantidade"] <= 0).sum())
print("Preço inválido:", (df["preco_unit"] <= 0).sum())
print("Categorias nulas:", df["categoria"].isna().sum())
print("UF em branco:", (df["uf"].str.strip() == "").sum())


# # Verificação dos dados brutos
# df = pd.read_csv("../data/raw/vendas_raw.csv")

# print(df.info())
# print("\nQuantidade inválida:", (df["quantidade"] <= 0).sum())
# print("Preço inválido:", (df["preco_unit"] <= 0).sum())
# print("Categorias nulas:", df["categoria"].isna().sum())
# print("UF em branco:", (df["uf"].str.strip() == "").sum())
