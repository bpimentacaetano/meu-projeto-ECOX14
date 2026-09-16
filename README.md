# meu-projeto-ECOX14

Troque **N** pelo número que você viu na saída do seu script. Número sem
origem não vale: se você não conseguiu medir, escreva o que impediu.

## Tema e pergunta norteadora

**Tema:** _uma frase._

**Pergunta norteadora:** _o que o pipeline deve ajudar a responder._

Toda decisão registrada abaixo se justifica em relação a essa pergunta.

## Como executar

```
python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux e macOS
pip install -r requirements.txt
```

Depois, a partir da raiz do projeto, na ordem:

```
python src/ingerir.py
python src/ingerir_paises.py
python src/ingerir_indicador_paises.py
python src/explorar.py
python src/transformar_paises.py
python src/transformar_artistas.py
python src/transformar_indicador_paises.py
```

A fonte do Spotify exige o arquivo `kaggle.json` em `~/.kaggle/`. As duas
do Banco Mundial são abertas e não pedem cadastro.

## Estrutura do projeto

```
src/                                  codigo
dados/
    bronze/                           dado bruto, imutavel
        spotify/
            artistas/
        banco_mundial/
            paises/
            indicador_paises/
    prata/                            dado tratado, reconstruivel
    ouro/
relatorios/                           perfilamento, nao versionado
```

A bronze tem dois níveis. O primeiro é a **origem**: um sistema, uma forma de
acesso, um termo de uso. O segundo é o **conjunto de dados**: uma tabela, um
esquema, uma granularidade, uma proveniência própria.

Países e indicador vêm do mesmo sistema e não são a mesma tabela, por isso
compartilham a pasta de origem e têm subpastas separadas.

## Fontes de dados

| Fonte | Conjunto | Uma linha é | Formato | Acesso | Extraído | Link |
|---|---|---|---|---|---|---|
| Spotify | artistas | um artista | CSV | token | 20/08/2026 | kaggle.com/... |
| Banco Mundial | paises | um país | JSON | aberto | 20/08/2026 | api.worldbank.org/v2/country |
| Banco Mundial | indicador_paises | um país em um ano | JSON | aberto | 17/09/2026 | api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL |

A coluna "uma linha é" declara a granularidade de cada conjunto. Ela é o que
define a chave, e é o que impede somar coisas que não se somam.

A data de extração aqui é um resumo. O registro que vale é o
`proveniencia.jsonl` de cada pasta da bronze.

## Defeitos conhecidos das fontes

### Spotify, conjunto artistas

- `Artist Type` tem espaço no início do nome da coluna.
- `Total`, `Lead` e `Feature` são redundantes: Total = Lead + Feature.
- `Debut Year` tem N valores ausentes.

### Banco Mundial, conjunto paises

- Devolve agregados regionais junto com os países, marcados com
  `region.value` igual a `Aggregates`.
- Nomes de região têm espaço no fim, como em `Latin America & Caribbean `.
- `capitalCity`, `longitude` e `latitude` vêm vazias nos agregados. Não é dado
  faltando: um agrupamento de países não tem capital.
- `adminregion.value` vem vazia nos países de renda alta, porque a
  classificação não se aplica a eles.
- `longitude` e `latitude` chegam como texto.
- `incomeLevel.value` mistura níveis de renda com `Aggregates` e
  `Not classified`, que não são níveis de renda.

### Banco Mundial, conjunto indicador_paises

- A resposta vem paginada. Na consulta de teste foram N páginas para N
  registros. Quem lê só a primeira página leva uma fração da série sem receber
  nenhum aviso.
- `unit`, `obs_status` e `decimal` vêm vazias ou com valor constante em todos
  os registros, então não carregam informação.
- O campo `date` é um ano, não uma data. Não tem mês, dia, hora nem fuso.
- Devolve agregados regionais junto com os países, e aqui **não existe** coluna
  de região para identificá-los. Só dá para separar cruzando com o conjunto
  `paises`.
- `value` é ausente em N pares país-ano, porque nem toda série cobre todo país
  em todo ano.

## Decisões de tratamento

### Banco Mundial, conjunto paises

- Espaços removidos de nomes de coluna e de texto.
- Agregados regionais separados: N linhas retiradas.
  Motivo: granularidade diferente da dos países.
- `longitude` e `latitude` convertidas para número.
  Vazios viraram ausentes: N ocorrências.
- `capitalCity` vazia mantida. Não se aplica a agregados, então preencher
  seria inventar dado.
- `incomeLevel.value` convertido para categoria com ordem declarada:
  Low income < Lower middle income < Upper middle income < High income.
  `Aggregates` e `Not classified` ficaram fora da escala e viraram ausentes:
  N ocorrências. Foi de propósito: não são níveis de renda.

### Spotify, conjunto artistas

- Espaços removidos de nomes de coluna e de texto, o que corrige
  `Artist Type`.
- Valores extremos de `Total` marcados, não removidos, em coluna própria.
  IQR marcou N registros e o escore padronizado marcou N.
  Os dois métodos discordam em N casos, listados abaixo:
  _descreva o que você encontrou ao olhar essas linhas._

### Banco Mundial, conjunto indicador_paises

- Todas as páginas da resposta foram percorridas. Registros recebidos: N,
  contra N informados pela API.
- Espaços removidos de nomes de coluna e de texto.
- Colunas sem informação descartadas: `unit`, `obs_status`, `decimal`.
- `date` mantido como inteiro, **não** convertido para data.
  Motivo: converter um ano para data cria um primeiro de janeiro que ninguém
  mediu, ou seja, precisão falsa.
- Duplicidade conferida pelo par `countryiso3code` + `date`, não por país
  sozinho. Numa série temporal, a entidade repete de propósito.
- Agregados regionais mantidos, a resolver no enriquecimento.

### Funções compartilhadas

As funções que não mencionam nenhuma fonte foram para `src/limpeza.py` e são
importadas pelos scripts de transformação. Uma correção nesse arquivo conserta
todas as fontes de uma vez.

## Atributos derivados

### variacao_pct

Variação percentual do indicador em relação ao ano anterior, por país.

Existe porque a coluna original esconde o que interessa: a população sobe em
todos os anos, e só a variação mostra se o ritmo está acelerando ou caindo.

Ausente no primeiro ano de cada país, por definição: não existe ano anterior
com que comparar.

### value_faixa

Quartil do valor do indicador, com quatro rótulos.

Existe para agrupar países comparáveis sem escolher um corte arbitrário. Usa
`qcut`, que corta por quantidade de registros, e não `cut`, que corta por
largura de valor.

Ausente quando `value` é ausente.

### _o seu terceiro atributo_

_O que é._

_Por que existe, em uma frase, ligada à pergunta norteadora._

_O que acontece quando o dado não permite calcular._

## Atualidade dos dados

A API do Banco Mundial informa, no metadado, a data em que a série foi
atualizada pela última vez. Esse valor está guardado no
`proveniencia.jsonl` do conjunto, no campo `fonte_atualizada_em`.

Última atualização informada pela fonte na extração deste projeto: N.

## Dificuldades e dúvidas

_O que não funcionou, o que ficou por resolver, e o que você não conseguiu
decidir sozinho. Um pipeline que falha por um motivo identificado e descrito
vale mais do que um pipeline silencioso que ninguém sabe se funcionou._