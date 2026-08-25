import pandas as pd

CAMINHO = "./dados/bronze/Spotify.csv"

df = pd.read_csv(CAMINHO)

print(df.shape)
print(df.head())

for coluna in df.columns:
    print(f"{coluna}: {df[coluna].dtype}")



