"""
Constroi a camada prata a partir da bronze da fonte de artistas.

Este arquivo e o par do transformar_paises.py. Ele existe para
mostrar que as mesmas funcoes servem para fontes diferentes, e
para exercitar o tratamento de valores extremos, que na fonte do
Banco Mundial nao tinha coluna adequada.

IMPORTANTE: os nomes de coluna aqui vieram do arquivo baixado em
aula. Se a fonte mudar, o script avisa em vez de quebrar em
silencio. Confira sempre a saida do primeiro print.

Como executar, a partir da raiz do projeto:
    python src/transformar_artistas.py
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

BRONZE = Path("dados/bronze/spotify")
PRATA = Path("dados/prata")
PADRAO = "artists_*.csv"

# Coluna numerica usada na analise de valores extremos.
COLUNA_EXTREMOS = "Lead Streams (in millions)"


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
    """Aqui a primeira linha e a que resolve o defeito conhecido.

    A coluna 'Artist Type' vem com espaco no inicio do nome. Sem
    o strip nas colunas, qualquer df['Artist Type'] daria erro de
    chave inexistente.
    """
    df.columns = df.columns.str.strip()
    for coluna in df.select_dtypes(include="object"):
        df[coluna] = df[coluna].str.strip()
    return df


def descobrir_chave(df):
    """Usa a primeira coluna como chave e mostra qual foi.

    Preferimos descobrir a chave a assumir o nome dela. Se a
    fonte renomear a coluna, o script continua funcionando e voce
    ve na saida qual chave foi usada.
    """
    chave = df.columns[0]
    print("chave usada:", repr(chave))
    return chave


def conferir_chave(df, chave):
    repetidas = int(df[chave].duplicated().sum())
    print("chaves repetidas:", repetidas)
    if repetidas:
        print(df[df[chave].duplicated(keep=False)].sort_values(chave))
    return df.drop_duplicates(subset=chave)


def limites_iqr(serie):
    q1 = serie.quantile(0.25)
    q3 = serie.quantile(0.75)
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def marcar_extremos(df, coluna):
    baixo, alto = limites_iqr(df[coluna])
    df[coluna + "_extremo"] = (df[coluna] < baixo) | (df[coluna] > alto)
    print(f"{coluna}: limites IQR [{baixo:.1f}, {alto:.1f}]")
    print(coluna, "extremos por IQR:", int(df[coluna + "_extremo"].sum()))
    return df


def marcar_zscore(df, coluna, limite=3):
    z = (df[coluna] - df[coluna].mean()) / df[coluna].std()
    df[coluna + "_z"] = z.abs() > limite
    print(coluna, f"extremos por z acima de {limite}:",
          int(df[coluna + "_z"].sum()))
    return df


def comparar_metodos(df, coluna):
    """Mostra onde os dois metodos discordam.

    A concordancia nao ensina nada. A divergencia e o material da
    discussao: um artista que o IQR marca e o z-score nao e um
    artista muito ouvido, ou um erro de coleta?
    """
    so_iqr = df[df[coluna + "_extremo"] & ~df[coluna + "_z"]]
    so_z = df[df[coluna + "_z"] & ~df[coluna + "_extremo"]]
    print("marcados so pelo IQR    :", len(so_iqr))
    print("marcados so pelo z-score:", len(so_z))
    return so_iqr, so_z


def salvar(df):
    PRATA.mkdir(parents=True, exist_ok=True)
    destino = PRATA / "artistas.parquet"
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
    chave = descobrir_chave(df)
    df = conferir_chave(df, chave)

    if COLUNA_EXTREMOS in df.columns:
        df = marcar_extremos(df, COLUNA_EXTREMOS)
        df = marcar_zscore(df, COLUNA_EXTREMOS)
        comparar_metodos(df, COLUNA_EXTREMOS)
    else:
        print(f"AVISO: coluna {COLUNA_EXTREMOS} nao existe mais.")
        print("Escolha outra coluna numerica e ajuste o topo do arquivo.")

    destino = salvar(df)
    registrar(origem, destino, antes, len(df), [
        "espacos removidos de colunas e de texto",
        f"duplicidade conferida pela chave {chave}",
        f"valores extremos de {COLUNA_EXTREMOS} marcados, nao removidos",
    ])


if __name__ == "__main__":
    main()