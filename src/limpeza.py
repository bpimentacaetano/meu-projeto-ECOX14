"""
Funcoes de limpeza que servem a qualquer fonte.

CRITERIO PARA UMA FUNCAO MORAR AQUI
===================================
Se a funcao menciona o nome de alguma fonte, ou alguma coluna
especifica dela, ela pertence ao script daquela fonte.
Se nao menciona, ela e generica e mora aqui.

Uma correcao feita neste arquivo conserta todas as fontes de uma
vez. Esse e o ganho, e e o motivo de o codigo sair dos scripts.

Coloque este arquivo em src, ao lado dos scripts de
transformacao, e importe com:
    import limpeza
"""

import pandas as pd


def tirar_espacos(df):
    """Remove espacos sobrando no nome das colunas e no texto.

    Espaco invisivel e a causa mais comum de juncao que nao
    encontra par. Rodar antes de qualquer comparacao de texto.
    """
    df.columns = df.columns.str.strip()
    for coluna in df.select_dtypes(include="object"):
        df[coluna] = df[coluna].str.strip()
    return df


def chave_texto(serie):
    """Versao comparavel de um texto.

    Devolve o texto sem acento, sem espaco sobrando e todo em
    minuscula. O resultado serve para COMPARAR e JUNTAR, nunca
    para exibir: o rotulo original continua na tabela.

    Exemplo:
        '  São Paulo ' -> 'sao paulo'
        'SAO PAULO'    -> 'sao paulo'
    """
    s = serie.str.strip().str.lower()
    s = s.str.normalize("NFKD")
    s = s.str.encode("ascii", errors="ignore")
    return s.str.decode("utf-8")


def aplicar_mapa(serie, mapa):
    """Troca variantes pelo valor canonico.

    O que nao estiver no mapa fica como esta. O dicionario e
    especifico de cada fonte, entao ele mora no script dela, e
    nao aqui.
    """
    return serie.replace(mapa)


def tipar_categoria(df, coluna, ordem=None):
    """Converte uma coluna para categoria, com ordem opcional.

    Quando ordem e informada, o que estiver fora da lista vira
    ausente. Isso e proposital: serve para separar o que nao
    pertence a escala. A funcao conta e imprime quantos foram,
    para que nada suma em silencio.
    """
    antes = int(df[coluna].isna().sum())
    if ordem:
        df[coluna] = pd.Categorical(df[coluna], categories=ordem, ordered=True)
    else:
        df[coluna] = df[coluna].astype("category")
    depois = int(df[coluna].isna().sum())
    print(f"{coluna}: fora da escala {depois - antes}")
    return df


def descartar_colunas_vazias(df):
    """Remove colunas sem informacao alguma.

    Entram nesse caso as colunas totalmente ausentes e as que tem
    um unico valor repetido em todas as linhas. Uma coluna
    constante nao distingue nada, entao nao ajuda a responder
    pergunta nenhuma.

    Imprime o que foi removido, porque remover coluna em silencio
    e a melhor forma de confundir quem ler o codigo depois.
    """
    remover = []
    for coluna in df.columns:
        sem_nulos = df[coluna].dropna()
        if len(sem_nulos) == 0 or sem_nulos.nunique() <= 1:
            remover.append(coluna)
    if remover:
        print("colunas sem informacao removidas:", remover)
    return df.drop(columns=remover)


def variacao_no_tempo(df, chave, tempo, valor, nome="variacao_pct"):
    """Variacao percentual em relacao ao periodo anterior.

    O sort_values nao e enfeite. Sem ordenar primeiro, a variacao
    seria calculada contra a linha anterior do arquivo, que pode
    ser outro ano ou ate outra entidade.

    O primeiro periodo de cada entidade fica ausente por
    definicao: nao existe anterior com que comparar.
    """
    df = df.sort_values([chave, tempo])
    df[nome] = df.groupby(chave)[valor].pct_change() * 100
    return df


def faixa_por_quartil(df, coluna, rotulos, sufixo="_faixa"):
    """Divide uma coluna continua em quatro faixas de igual tamanho.

    qcut corta por quantidade de registros: cada faixa fica com um
    quarto dos casos. Se voce quiser faixas de largura igual em
    valor, use pd.cut. Sao resultados diferentes, e a escolha
    depende da pergunta.
    """
    df[coluna + sufixo] = pd.qcut(df[coluna], q=4, labels=rotulos)
    return df