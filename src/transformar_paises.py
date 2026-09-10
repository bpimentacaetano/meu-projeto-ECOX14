
import json
from datetime import datetime
from pathlib import Path

import pandas as pd

BRONZE = Path("dados/bronze/banco_mundial")
PRATA = Path("dados/prata")
PADRAO = "paises_*.csv"


def carregar():
    arquivos = sorted(BRONZE.glob(PADRAO))
    if not arquivos:
        raise FileNotFoundError(f"Nenhum arquivo {PADRAO} em {BRONZE}")
    caminho = arquivos[-1]
    df = pd.read_csv(caminho)
    print("lido:", caminho.name, df.shape)
    print()
    print("colunas:", df.columns.tolist())
    print()
    print("ausentes por coluna:")
    print(df.isna().sum())
    print()
    return df, caminho


def tirar_espacos(df):
    df.columns = df.columns.str.strip()
    for coluna in df.select_dtypes(include="object"):
        df[coluna] = df[coluna].str.strip()
    return df


def separar_agregados(df):
    e_pais = df["region.value"] != "Aggregates"
    print("paises   :", int(e_pais.sum()))
    print("agregados:", int((~e_pais).sum()))
    return df[e_pais].copy()


def conferir_chave(df, chave="id"):
    repetidas = int(df[chave].duplicated().sum())
    print("chaves repetidas:", repetidas)
    if repetidas:
        print(df[df[chave].duplicated(keep=False)].sort_values(chave))
    return df.drop_duplicates(subset=chave)


def converter_tipos(df):
    for coluna in ["longitude", "latitude"]:
        antes = int(df[coluna].isna().sum())
        df[coluna] = pd.to_numeric(df[coluna], errors="coerce")
        depois = int(df[coluna].isna().sum())
        print(f"{coluna}: ausentes {antes} -> {depois}")
    return df


def limites_iqr(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def marcar_extremos(df, coluna):
    baixo, alto = limites_iqr(df[coluna])
    df[coluna + "_extremo"] = (df[coluna] < baixo) | (df[coluna] > alto)
    print(coluna, "extremos por IQR:", int(df[coluna + "_extremo"].sum()))
    return df


def marcar_zscore(df, coluna, limite=3):
    z = (df[coluna] - df[coluna].mean()) / df[coluna].std()
    df[coluna + "_z"] = z.abs() > limite
    print(coluna, f"extremos por z acima de {limite}:",
          int(df[coluna + "_z"].sum()))
    return df


def remover_erros(df, coluna, minimo, maximo):
    valido = df[coluna].between(minimo, maximo)
    print(f"{coluna} fora de [{minimo}, {maximo}]:", int((~valido).sum()))
    return df[valido].copy()


def salvar(df):
    PRATA.mkdir(parents=True, exist_ok=True)
    destino = PRATA / "paises.parquet"
    df.to_parquet(destino, index=False)
    print("salvo em:", destino, df.shape)
    return destino


def registrar(origem, destino, antes, depois, decisoes):
    info = {
        "origem": origem.name,
        "arquivo_prata": destino.name,
        "linhas_antes": antes,
        "linhas_depois": depois,
        "decisoes": decisoes,
        "transformado_em": datetime.now().isoformat(timespec="seconds"),
    }
    caminho = PRATA / "proveniencia.jsonl"
    with caminho.open("a", encoding="utf-8") as f:
        f.write(json.dumps(info, ensure_ascii=False) + "\n")
    print("proveniencia:", caminho)
    return info


def main():
    df, origem = carregar()
    antes = len(df)

    df = tirar_espacos(df)
    print("espacos removidos de colunas e de texto")
    print(df.columns.tolist())
    df = separar_agregados(df)
    df = conferir_chave(df)
    df = converter_tipos(df)

   # exN, exP = limites_iqr()
    # Longitude fora de -180 a 180 e erro de geografia, nao valor
    # extremo. Por isso aqui a remocao se justifica.
    df = remover_erros(df, "longitude", -180, 180)
    df = remover_erros(df, "latitude", -90, 90)

    destino = salvar(df)

    registrar(origem, destino, antes, len(df), [
        "espacos removidos de colunas e de texto",
        "agregados regionais separados",
        "duplicidade conferida pela chave id",
        "longitude e latitude convertidas para numero",
        "coordenadas fora da faixa geografica removidas",
    ])


if __name__ == "__main__":
    main()