from pathlib import Path
import pandas as pd
from data_profiling import ProfileReport


BRONZE = Path("dados/bronze/spotify")
PADRAO = "artists_*.csv"
RELATORIOS = Path("relatorios")

def mais_recente():
    arquivos = sorted(BRONZE.glob(PADRAO))
    if not arquivos:
        raise FileNotFoundError("bronze vazia")
    return arquivos[-1]

def gerar(caminho):
    df = pd.read_csv(caminho)
    perfil = ProfileReport(df, title=caminho.name)
    RELATORIOS.mkdir(exist_ok=True)
    saida = RELATORIOS / f"{caminho.stem}.html"
    perfil.to_file(saida)
    return saida


if __name__ == "__main__":
    caminho = mais_recente()
    print("perfilando:", caminho.name)
    print(gerar(caminho))

