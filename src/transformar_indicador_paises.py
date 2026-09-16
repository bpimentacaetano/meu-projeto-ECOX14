"""
Constroi a camada prata do indicador por pais e por ano.

O nome espelha o do script de ingestao. Toda fonte tem um par:
ingerir_X.py traz o dado bruto, transformar_X.py produz a prata.
Quando um dos dois e renomeado, o outro acompanha.

Tres decisoes desta aula aparecem aqui:

  1. O ano fica inteiro, nao vira data. O campo date da fonte
     vale "2023": e um ano, nao um instante. Converter para data
     criaria um primeiro de janeiro que ninguem mediu.

  2. As colunas sem informacao saem. unit, obs_status e decimal
     vem vazias ou constantes. Sao contadas e registradas antes
     de sumir.

  3. Os agregados regionais continuam na tabela. Aqui nao existe
     coluna de regiao para filtra-los, e essa falta e proposital:
     ela se resolve na aula de enriquecimento, quando esta tabela
     for juntada a de paises pelo codigo de tres letras.

Como executar, a partir da raiz do projeto:
    python src/transformar_indicador_paises.py
"""

import json
from datetime import datetime
from pathlib import Path

import pandas as pd

import limpeza

BRONZE = Path("dados/bronze/banco_mundial/indicador_paises")
PRATA = Path("dados/prata")
PADRAO = "*.csv"

CHAVE = "countryiso3code"
TEMPO = "date"
VALOR = "value"

ROTULOS_FAIXA = ["muito pequeno", "pequeno", "grande", "muito grande"]


def carregar():
    arquivos = sorted(
        p for p in BRONZE.glob(PADRAO) if p.name != "proveniencia.jsonl"
    )
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


def tipar_ano(df):
    """O ano fica inteiro.

    Int64 com I maiusculo e o inteiro do pandas que aceita
    ausente. O int comum nao aceita, e a conversao quebraria se
    algum registro viesse sem ano.
    """
    df[TEMPO] = pd.to_numeric(df[TEMPO], errors="coerce").astype("Int64")
    print("anos encontrados:", df[TEMPO].min(), "a", df[TEMPO].max())
    return df


def conferir_chave(df):
    """Aqui a chave e composta: entidade mais ano.

    Uma serie temporal repete a entidade de proposito. O que nao
    pode repetir e o par entidade-ano.
    """
    repetidas = int(df.duplicated(subset=[CHAVE, TEMPO]).sum())
    print("pares entidade-ano repetidos:", repetidas)
    if repetidas:
        print(df[df.duplicated(subset=[CHAVE, TEMPO], keep=False)]
              .sort_values([CHAVE, TEMPO]))
    return df.drop_duplicates(subset=[CHAVE, TEMPO])


def main():
    df, origem = carregar()
    antes = len(df)

    df = limpeza.tirar_espacos(df)
    df = limpeza.descartar_colunas_vazias(df)
    df = tipar_ano(df)
    df = conferir_chave(df)

    # Atributos derivados
    df = limpeza.variacao_no_tempo(df, CHAVE, TEMPO, VALOR)
    df = limpeza.faixa_por_quartil(df, VALOR, ROTULOS_FAIXA)

    PRATA.mkdir(parents=True, exist_ok=True)
    destino = PRATA / "indicador_paises.parquet"
    df.to_parquet(destino, index=False)
    print("salvo em:", destino, df.shape)

    info = {
        "origem": origem.name,
        "arquivo_prata": destino.name,
        "linhas_antes": antes,
        "linhas_depois": len(df),
        "decisoes": [
            "espacos removidos de colunas e de texto",
            "colunas sem informacao descartadas",
            "ano mantido como inteiro, nao convertido para data",
            "duplicidade conferida pelo par entidade-ano",
            "agregados regionais mantidos, a resolver no enriquecimento",
        ],
        "atributos_derivados": ["variacao_pct", VALOR + "_faixa"],
        "transformado_em": datetime.now().isoformat(timespec="seconds"),
    }
    caminho = PRATA / "proveniencia.jsonl"
    with caminho.open("a", encoding="utf-8") as f:
        f.write(json.dumps(info, ensure_ascii=False) + "\n")
    print("proveniencia:", caminho)


if __name__ == "__main__":
    main()