import requests
from pathlib import Path
import pandas as pd
from datetime import date, datetime
import json

from requests.help import info

URL = "https://api.worldbank.org/v2/country"

BRONZE = Path("dados/bronze/banco_mundial")

def buscar():
    r = requests.get(URL, params={
        "format": "json", "per_page": 300}, timeout=30)
    r.raise_for_status()
    return r.json()

def conferir(dados):
    meta = dados[0]
    print("registros:", meta["total"])
    print("paginas :", meta["pages"])
    if meta["pages"] > 1:
        print("ATENCAO: falta paginar")
    return meta

def salvar(dados):
    BRONZE.mkdir(parents=True, exist_ok=True)
    paises = pd.json_normalize(dados[1])
    hoje = date.today().strftime("%Y%m%d")
    destino = BRONZE / f"paises_{hoje}.csv"
    paises.to_csv(destino, index=False)
    print(paises["region.value"].unique())
    return destino


def registrar(destino, meta):
    info = {
        "fonte": URL,
        "arquivo_bronze": destino.name,
        "registros": meta["total"],
        "extraido_em": datetime.now().isoformat(),
    }
    caminho = BRONZE / "proveniencia.jsonl"
    with caminho.open("a", encoding="utf-8") as f:
        f.write(json.dumps(info, ensure_ascii=False) + "\n")

    

def main():
    dados = buscar()
    print(type(dados), len(dados))
    print(dados[0])
    conferir(dados)
    salvar(dados)
    registrar(salvar(dados), conferir(dados))

if __name__ == "__main__":
    main()
