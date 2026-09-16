"""
Gera os slides da Aula 6 de ECOX14 em PowerPoint.

COMO USAR
=========
    pip install python-pptx
    python gerar_aula06_pptx.py

O arquivo ECOX14_Aula06_Limpeza_e_Atributos.pptx e criado na mesma
pasta de onde o comando for executado.
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

NAVY = "1B3A5F"
NAVY_D = "14304F"
CODE_BG = "10283F"
ORANGE = "D96F2C"
ORANGE_T = "B4571C"
BLUE_M = "3E6E9E"
BLUE_L = "8FB0CE"
TINT = "EDF1F6"
PAPER = "F7F8FA"
INK = "1F2D3A"
MUTED = "5C6E7C"
RULE = "D6DDE4"
WHITE = "FFFFFF"
GREEN = "5A9E4B"
GREEN_T = "3F7833"
DIM = "6E8AA8"
PEACH = "FBEDE2"

F = "Calibri"
MONO = "Courier New"

W = 13.333
M = 0.85
CW = W - 2 * M

prs = Presentation()
prs.slide_width = Inches(W)
prs.slide_height = Inches(7.5)
BRANCO = prs.slide_layouts[6]

ALIGN = {"left": PP_ALIGN.LEFT, "center": PP_ALIGN.CENTER, "right": PP_ALIGN.RIGHT}
ANCHOR = {"top": MSO_ANCHOR.TOP, "middle": MSO_ANCHOR.MIDDLE, "bottom": MSO_ANCHOR.BOTTOM}


def shape(s, x, y, w, h, cor, forma=MSO_SHAPE.RECTANGLE, linha=None, linha_pt=1.25):
    sh = s.shapes.add_shape(forma, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid()
    sh.fill.fore_color.rgb = RGBColor.from_string(cor)
    if linha:
        sh.line.color.rgb = RGBColor.from_string(linha)
        sh.line.width = Pt(linha_pt)
    else:
        sh.line.fill.background()
    try:
        sh.shadow.inherit = False
    except Exception:
        pass
    return sh


def txt(s, t, x, y, w, h, size, cor=INK, bold=False, fonte=F,
        align="left", valign="top", italic=False, espaco=None, letra=None):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = ANCHOR[valign]
    p = tf.paragraphs[0]
    p.alignment = ALIGN[align]
    if espaco:
        p.line_spacing = espaco
    r = p.add_run()
    r.text = t
    r.font.name = fonte
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = RGBColor.from_string(cor)
    if letra:
        try:
            r.font._rPr.set("spc", str(int(letra * 100)))
        except Exception:
            pass
    return tb


def slide(fundo=PAPER):
    s = prs.slides.add_slide(BRANCO)
    shape(s, 0, 0, W, 7.5, fundo)
    return s


def notas(s, t):
    s.notes_slide.notes_text_frame.text = t


def head(s, t):
    txt(s, t, M, 0.55, CW, 0.85, 38, INK, bold=True)


def head_dark(s, t):
    txt(s, t, M, 0.55, CW, 0.85, 38, WHITE, bold=True)


def hrule(s, x, y, w, c=RULE):
    shape(s, x, y, w, 0.015, c)


def panel(s, x, y, w, h, c=TINT):
    shape(s, x, y, w, h, c)


def marker(s, n, x, y, c=ORANGE, d=0.52):
    shape(s, x, y, d, d, c, MSO_SHAPE.OVAL)
    txt(s, str(n), x, y, d, d, 20, WHITE, bold=True, align="center", valign="middle")


def step_badge(s, t):
    panel(s, M, 0.55, 2.6, 0.62, ORANGE)
    txt(s, t, M, 0.55, 2.6, 0.62, 24, WHITE, bold=True, align="center", valign="middle")


def step_title(s, t):
    txt(s, t, M, 1.35, CW, 0.75, 34, INK, bold=True)


def code(s, linhas, x, y, w, h, size=20, lh=0.42):
    panel(s, x, y, w, h, CODE_BG)
    for i, (linha, estilo) in enumerate(linhas):
        cor = ORANGE if estilo == "novo" else (DIM if estilo == "dim" else WHITE)
        txt(s, linha, x + 0.35, y + 0.2 + i * lh, w - 0.7, lh, size, cor,
            bold=(estilo == "novo"), fonte=MONO, valign="middle")


def fonte_txt(s, t, escuro=False):
    txt(s, t, M, 6.85, CW, 0.34, 16, "7E9AB8" if escuro else MUTED, italic=True)


def nota(s, t, y=6.7):
    txt(s, t, M, y, CW, 0.7, 21, MUTED, espaco=1.1)


# ==================================================================== capa
s = slide(NAVY)
txt(s, "UNIVERSIDADE FEDERAL DE ITAJUBÁ", M, 2.05, CW, 0.4, 24, BLUE_L,
    bold=True, letra=1.6)
txt(s, "Engenharia de Dados na Prática", M, 2.7, 11.2, 0.95, 52, WHITE, bold=True)
shape(s, M, 3.85, 1.5, 0.05, ORANGE)
txt(s, "Limpeza avançada e engenharia de atributos", M, 4.2, 11.2, 0.6, 30, WHITE)
txt(s, "Profa. Bárbara Pimenta Caetano", M, 5.5, 8, 0.45, 24, BLUE_L)
notas(s, "Conferir quem conseguiu gravar o parquet da prata. Quem nao gravou "
         "resolve nos primeiros minutos, porque a aula de hoje escreve em cima "
         "dela.")

# ================================================================== agenda
s = slide()
head(s, "O que veremos hoje")
for i, t in enumerate([
        "Uma terceira fonte, para termos tempo no projeto",
        "Tipos: quando a coluna passa a se comportar",
        "Texto: o mesmo valor escrito de várias formas",
        "Datas: o que o computador entende por tempo",
        "Atributos derivados e o critério para criá-los"]):
    y = 2.0 + i * 0.95
    marker(s, i + 1, M, y, ORANGE if i >= 1 else BLUE_M)
    txt(s, t, M + 0.9, y - 0.02, CW - 0.9, 0.55, 27, INK, valign="middle")
    if i < 4:
        hrule(s, M, y + 0.68, CW)
notas(s, "Aula longa em topicos e curta em conceito novo. O fio e sempre o "
         "mesmo: deixar a prata utilizavel.")

# =========================================================== onde estamos
s = slide(NAVY)
head_dark(s, "Onde estamos")
for i, (cor, nome, desc, destaque) in enumerate([
        (BLUE_L, "Bronze", "Três fontes ao fim de hoje", False),
        (ORANGE, "Prata", "Correta na aula passada, utilizável hoje", True),
        ("2E4A66", "Ouro", "Modelagem e entrega", False)]):
    y = 2.1 + i * 1.3
    panel(s, M, y, CW, 1.1, ORANGE if destaque else NAVY_D)
    shape(s, M + 0.45, y + 0.3, 0.5, 0.5, WHITE if destaque else cor)
    txt(s, nome, M + 1.25, y, 3.0, 1.1, 30, WHITE, bold=True, valign="middle")
    txt(s, desc, M + 4.4, y, CW - 4.8, 1.1, 25,
        WHITE if destaque else BLUE_L, valign="middle")
txt(s, "Correto e utilizável não são a mesma coisa.",
    M, 6.15, CW, 0.6, 26, WHITE, bold=True)
notas(s, "A prata da aula passada esta certa: sem duplicata, sem agregado, sem "
         "espaco sobrando. Mas ainda nao responde nenhuma pergunta.")

# ================================================== correto x utilizavel
s = slide()
head(s, "O que a sua Prata ainda não é")
for i, (prob, desc) in enumerate([
        ("Os tipos estão frouxos",
         "Categoria guardada como texto livre, número guardado como texto, "
         "nada impede um valor impossível de entrar."),
        ("O mesmo valor aparece escrito de formas diferentes",
         "E o computador trata cada forma como uma coisa distinta na hora de "
         "agrupar ou de juntar com outra fonte."),
        ("Não existe nenhuma coluna que responda à sua pergunta",
         "Só existem as colunas que a fonte resolveu publicar. Ninguém lá "
         "sabia o que você queria perguntar.")]):
    y = 1.8 + i * 1.6
    shape(s, M, y, 0.09, 1.4, ORANGE)
    txt(s, prob, M + 0.35, y, CW - 0.35, 0.55, 26, INK, bold=True, espaco=1.05)
    txt(s, desc, M + 0.35, y + 0.62, CW - 0.7, 0.8, 22, MUTED, espaco=1.1)
nota(s, "As três coisas se resolvem hoje, nessa ordem.", 6.7)
notas(s, "Cada item vira um bloco da aula. Vale voltar a esse slide entre os "
         "blocos para mostrar onde estamos.")

# ============================================== falta tempo nos dados
s = slide()
head(s, "Falta tempo nos nossos dados")
panel(s, M, 1.8, CW, 1.9, TINT)
txt(s, "Nenhuma das duas fontes tem coluna temporal", M + 0.45, 1.95, CW - 0.9,
    0.5, 26, INK, bold=True)
txt(s, "A tabela de países descreve um retrato, não uma história. A de artistas "
       "traz um ano de estreia, que é um atributo, não uma linha do tempo.",
    M + 0.45, 2.55, CW - 0.9, 1.05, 23, MUTED, espaco=1.15)
txt(s, "Sem tempo, você não pergunta:", M, 4.0, CW, 0.5, 24, BLUE_M, bold=True)
for i, t in enumerate([
        "cresceu ou caiu?",
        "quando mudou de patamar?",
        "o que aconteceu antes e o que veio depois?"]):
    txt(s, "• " + t, M + 0.4, 4.55 + i * 0.52, CW - 0.8, 0.5, 23, INK,
        valign="middle")
panel(s, M, 6.25, CW, 0.85, PEACH)
txt(s, "Boa parte das perguntas interessantes é sobre variação. Vamos buscar "
       "uma fonte que tenha tempo.", M + 0.45, 6.25, CW - 0.9, 0.85, 22,
    ORANGE_T, bold=True, valign="middle")
notas(s, "Perguntar quem escolheu uma fonte com tempo. Quem nao escolheu "
         "precisa pensar em uma segunda fonte temporal ate a aula de "
         "enriquecimento.")

# ============================================= a mesma api, outro recurso
s = slide()
head(s, "A mesma API, outro recurso")
txt(s, "Indicador por país e por ano. Aqui, população total:",
    M, 1.5, CW, 0.45, 24, INK)
code(s, [
    ("https://api.worldbank.org/v2/country/all", "novo"),
    ("    /indicator/SP.POP.TOTL", "novo"),
    ('    ?format=json&date=2000:2023', "novo"),
], M, 2.05, CW, 1.8, 20, 0.45)
txt(s, "Um registro da resposta:", M, 4.05, CW, 0.45, 24, BLUE_M, bold=True)
code(s, [
    ('{"indicator": {"id": "SP.POP.TOTL", ...},', ""),
    ('  "country": {"id": "ZH", "value": "Africa Eastern..."},', ""),
    ('  "countryiso3code": "AFE",', "novo"),
    ('  "date": "2023",', "novo"),
    ('  "value": 750491370,', ""),
    ('  "unit": "", "obs_status": "", "decimal": 0}', "dim"),
], M, 4.6, CW, 2.25, 17, 0.36)
fonte_txt(s, "Resposta real da API, consultada durante o preparo desta aula.")
notas(s, "Destacar o countryiso3code: e a mesma chave da tabela de paises. "
         "Isso monta o join da proxima aula com dado que eles ja conhecem.")

# ================================================== o guarda que dispara
s = slide()
head(s, "O alerta que vocês escreveram finalmente disparou")
txt(s, "Na aula de ingestão, a função conferir() terminava assim:",
    M, 1.5, CW, 0.45, 23, INK)
code(s, [
    ('if meta["pages"] > 1:', "dim"),
    ('    print("ATENCAO: a resposta veio paginada.")', "dim"),
], M, 2.0, CW, 1.3, 20, 0.45)
txt(s, "Até hoje ele nunca havia disparado. Agora o metadado vem assim:",
    M, 3.45, CW, 0.5, 23, INK)
code(s, [
    ('{"page": 1, "pages": 133, "total": 530,', "novo"),
    ('  "sourceid": "2", "lastupdated": "2026-07-13"}', "novo"),
], M, 4.0, CW, 1.35, 19, 0.45)
panel(s, M, 5.55, CW, 1.2, PEACH)
txt(s, "Se você ignorar a paginação, leva para casa a primeira página e acha "
       "que tem a série inteira. É o tipo de erro que não avisa: o script roda, "
       "o arquivo salva, e o número está errado.",
    M + 0.45, 5.55, CW - 0.9, 1.2, 21, ORANGE_T, bold=True, valign="middle",
    espaco=1.15)
fonte_txt(s, "Metadado real de uma consulta de duas décadas. Com a sua "
             "consulta os números mudam, a estrutura não.")
notas(s, "Esse e o momento de pagamento de uma decisao antiga. Vale dizer isso "
         "em voz alta: a guarda foi escrita quando nao servia para nada.")

# ============================================================ tipos: por que
s = slide()
head(s, "Tipo não é formalidade")
for i, (ganho, desc) in enumerate([
        ("A operação certa fica disponível",
         "Em texto, 10 é menor que 9. Em número, não. Ordenar, somar e comparar "
         "só funcionam depois da conversão."),
        ("O erro aparece cedo",
         "Uma coluna tipada recusa o valor impossível na hora da carga, em vez "
         "de entregar um resultado estranho três etapas adiante."),
        ("O arquivo encolhe",
         "Categoria guardada como categoria ocupa uma fração do que ocupa como "
         "texto repetido milhares de vezes.")]):
    y = 1.85 + i * 1.55
    panel(s, M, y, CW, 1.35, TINT if i % 2 == 0 else PAPER)
    shape(s, M, y, 0.09, 1.35, ORANGE)
    txt(s, ganho, M + 0.35, y + 0.12, CW - 0.7, 0.5, 26, INK, bold=True)
    txt(s, desc, M + 0.35, y + 0.68, CW - 0.7, 0.6, 22, MUTED, espaco=1.1)
notas(s, "O primeiro item e o mais facil de demonstrar ao vivo: ordenar uma "
         "coluna de numeros guardada como texto.")

# =========================================================== categorico
s = slide()
head(s, "Categoria com ordem é diferente de categoria sem ordem")
txt(s, "A tabela de países traz o nível de renda, que tem ordem natural:",
    M, 1.5, CW, 0.45, 23, INK)
code(s, [
    ('ordem = ["Low income", "Lower middle income",', "novo"),
    ('         "Upper middle income", "High income"]', "novo"),
    ("", ""),
    ('df["incomeLevel.value"] = pd.Categorical(', "novo"),
    ('    df["incomeLevel.value"], categories=ordem, ordered=True)', "novo"),
], M, 2.05, CW, 2.5, 18, 0.42)
panel(s, M, 4.75, CW, 1.35, PEACH)
txt(s, "Os valores que não estão na lista viram ausentes. E é isso que você "
       "quer: 'Aggregates' e 'Not classified' não são níveis de renda, e o "
       "código passa a dizer isso em voz alta.",
    M + 0.45, 4.75, CW - 0.9, 1.35, 21, ORANGE_T, bold=True, valign="middle",
    espaco=1.15)
nota(s, "Com ordem declarada, comparar e ordenar passam a funcionar. Sem ela, "
        "o pandas ordena em ordem alfabética, e 'High income' vem primeiro.", 6.3)
notas(s, "Cuidado que vale avisar: a conversao transforma em ausente o que "
         "estiver fora da lista. Contar antes e depois.")

# ================================================== texto: mesmo valor
s = slide()
head(s, "O mesmo valor, escrito de seis formas")
code(s, [
    ("São Paulo", ""),
    ("SAO PAULO", ""),
    ("sao paulo", ""),
    ("  São Paulo ", ""),
    ("S. Paulo", ""),
    ("SP", ""),
], M, 1.75, 5.4, 3.0, 21, 0.44)
panel(s, 6.85, 1.75, 5.65, 3.0, NAVY)
txt(s, "Para você", 7.25, 1.95, 4.9, 0.45, 24, BLUE_L, bold=True)
txt(s, "É a mesma cidade.", 7.25, 2.45, 4.9, 0.45, 23, WHITE)
txt(s, "Para o computador", 7.25, 3.1, 4.9, 0.45, 24, ORANGE, bold=True)
txt(s, "São seis cidades diferentes. Agrupar dá seis linhas, e juntar com "
       "outra fonte encontra no máximo uma.",
    7.25, 3.6, 4.9, 1.0, 23, WHITE, espaco=1.1)
txt(s, "Exemplo ilustrativo, montado para a aula. As nossas fontes vêm em "
       "inglês e razoavelmente padronizadas, mas a sua pode não vir.",
    M, 5.0, CW, 0.75, 20, MUTED, italic=True, espaco=1.1)
panel(s, M, 5.9, CW, 1.05, TINT)
txt(s, "Esse é o defeito que mais estraga junção de fontes, e é invisível em "
       "qualquer inspeção rápida, porque os valores parecem certos um a um.",
    M + 0.45, 5.9, CW - 0.9, 1.05, 22, INK, valign="middle", espaco=1.15)
notas(s, "Deixar claro que o exemplo e inventado. Perguntar quem tem coluna de "
         "municipio, estado ou nome de empresa na propria fonte: sao os casos "
         "classicos.")

# ================================================= texto: quatro operacoes
s = slide()
head(s, "Quatro operações, nessa ordem")
for i, (op, desc) in enumerate([
        ("Tirar espaços", "Nas pontas e os repetidos no meio."),
        ("Unificar a caixa", "Tudo em minúscula para comparar. O rótulo bonito "
                            "se recupera depois."),
        ("Tratar acentos", "Só quando a fonte é inconsistente. Se ela acentua "
                           "sempre, remover acento é perder informação."),
        ("Mapear sinônimos", "Um dicionário explícito, escrito por você, "
                             "ligando cada variante ao valor canônico.")]):
    y = 1.8 + i * 1.2
    marker(s, i + 1, M, y + 0.1, ORANGE)
    txt(s, op, M + 0.9, y, 3.6, 0.55, 25, INK, bold=True)
    txt(s, desc, M + 4.6, y, CW - 4.8, 0.95, 22, MUTED, espaco=1.1)
panel(s, M, 6.3, CW, 0.9, PEACH)
txt(s, "As três primeiras são automáticas. A quarta exige que você conheça o "
       "assunto, e por isso precisa ficar escrita no código, não na sua cabeça.",
    M + 0.45, 6.3, CW - 0.9, 0.9, 21, ORANGE_T, bold=True, valign="middle",
    espaco=1.1)
notas(s, "A ordem importa: mapear sinonimo antes de unificar caixa obriga a "
         "escrever cada variante duas vezes.")

# ================================================== datas: ano nao e data
s = slide()
head(s, "Nem todo dado temporal é uma data")
panel(s, M, 1.8, CW, 1.5, TINT)
txt(s, 'O campo date da nossa fonte nova vale "2023"',
    M + 0.45, 1.95, CW - 0.9, 0.5, 26, INK, bold=True)
txt(s, "Isso é um ano, não um instante. Não tem mês, não tem dia, não tem hora "
       "e não tem fuso.", M + 0.45, 2.5, CW - 0.9, 0.7, 23, MUTED, espaco=1.1)
txt(s, "Converter para data cria precisão que o dado não tem:",
    M, 3.5, CW, 0.5, 24, BLUE_M, bold=True)
code(s, [
    ('pd.to_datetime("2023")   # vira 2023-01-01 00:00:00', "novo"),
    ("# e o primeiro de janeiro nunca foi medido", "dim"),
], M, 4.05, CW, 1.3, 19, 0.45)
panel(s, M, 5.6, CW, 1.2, PEACH)
txt(s, "Para uma série anual, inteiro é o tipo honesto. Ele ordena, subtrai e "
       "compara, sem inventar um dia que ninguém observou.",
    M + 0.45, 5.6, CW - 0.9, 1.2, 22, ORANGE_T, bold=True, valign="middle",
    espaco=1.15)
notas(s, "Ponto contraintuitivo: converter para data parece mais sofisticado e "
         "e pior. A pergunta certa e sempre qual a granularidade real da "
         "medicao.")

# ===================================================== datas: parsing
s = slide()
head(s, "Quando é data mesmo, o risco é o formato")
code(s, [
    ('pd.to_datetime("03/04/2026")', "novo"),
    ("# 3 de abril ou 4 de março?", "dim"),
    ("", ""),
    ('pd.to_datetime(coluna, format="%d/%m/%Y")', "novo"),
    ("# agora não há dúvida", "dim"),
], M, 1.7, CW, 2.5, 19, 0.44)
for i, (risco, desc) in enumerate([
        ("Ambiguidade de ordem",
         "Sem format declarado, a biblioteca adivinha, e pode adivinhar "
         "diferente em arquivos diferentes da mesma fonte."),
        ("Fuso horário",
         "Só importa quando o dado tem hora e vem de sistemas em lugares "
         "diferentes. Registro de evento e log quase sempre têm.")]):
    y = 4.45 + i * 1.25
    panel(s, M, y, CW, 1.1, TINT if i % 2 == 0 else PAPER)
    shape(s, M, y, 0.09, 1.1, ORANGE)
    txt(s, risco, M + 0.35, y, 3.7, 1.1, 23, INK, bold=True, valign="middle")
    txt(s, desc, M + 4.2, y, CW - 4.4, 1.1, 21, MUTED, valign="middle", espaco=1.1)
notas(s, "Declarar format sempre. O modo adivinhacao e a fonte silenciosa de "
         "erro em pipeline que roda todo mes.")

# ============================================= datas: lastupdated
s = slide()
head(s, "A data que estava escondida no metadado")
txt(s, "A resposta da API traz, junto da paginação:", M, 1.5, CW, 0.45, 24, INK)
code(s, [('"lastupdated": "2026-07-13"', "novo")], M, 2.05, CW, 0.9, 23)
txt(s, "Não é uma coluna do dado. É a data em que a fonte atualizou a série "
       "pela última vez.", M, 3.15, CW, 0.7, 23, INK, espaco=1.1)
for i, (uso, desc) in enumerate([
        ("Responde à pergunta de atualidade",
         "Aquela quarta dimensão da aula passada deixa de ser abstrata: agora "
         "você tem o número para dizer se o dado ainda vale."),
        ("Vai para a proveniência, não para a tabela",
         "É informação sobre o conjunto inteiro, não sobre cada linha. "
         "Repetir em todas as linhas seria desperdício e confusão.")]):
    y = 4.05 + i * 1.35
    panel(s, M, y, CW, 1.2, TINT if i % 2 == 0 else PAPER)
    shape(s, M, y, 0.09, 1.2, BLUE_M)
    txt(s, uso, M + 0.35, y + 0.1, CW - 0.7, 0.45, 23, INK, bold=True)
    txt(s, desc, M + 0.35, y + 0.58, CW - 0.7, 0.55, 21, MUTED, espaco=1.05)
fonte_txt(s, "Valor real devolvido pela API no preparo desta aula.")
notas(s, "Boa oportunidade de mostrar que metadado costuma valer tanto quanto "
         "dado, e que quase todo mundo joga fora.")

# ========================================== atributo derivado: o que e
s = slide()
head(s, "Atributo derivado")
panel(s, M, 1.75, CW, 1.35, TINT)
txt(s, "Uma coluna nova, calculada a partir das que já existem, que responde "
       "melhor à sua pergunta do que qualquer uma delas sozinha.",
    M + 0.45, 1.75, CW - 0.9, 1.35, 25, INK, valign="middle", espaco=1.15)
txt(s, "A fonte publicou o que ela achou útil. Ninguém lá sabia o que você "
       "queria perguntar.", M, 3.35, CW, 0.6, 24, BLUE_M, bold=True, espaco=1.1)
for i, (antes, depois) in enumerate([
        ("população em 2000 e população em 2023", "crescimento percentual no período"),
        ("data de nascimento", "faixa etária"),
        ("valor total e quantidade", "valor médio por unidade")]):
    y = 4.2 + i * 0.95
    txt(s, antes, M, y, 5.4, 0.8, 21, MUTED, valign="middle", espaco=1.05)
    txt(s, "→", 6.4, y, 0.6, 0.8, 26, ORANGE, bold=True, align="center",
        valign="middle")
    txt(s, depois, 7.15, y, CW - 6.3, 0.8, 22, INK, bold=True, valign="middle",
        espaco=1.05)
notas(s, "Comecar pedindo que releiam a propria pergunta norteadora, escrita na "
         "primeira entrega. O atributo tem que servir a ela.")

# ========================================== atributo derivado: criterio
s = slide()
head(s, "O critério, e a armadilha");
panel(s, M, 1.75, CW, 1.15, NAVY)
txt(s, "Se você não consegue dizer em uma frase por que a coluna nova ajuda a "
       "responder a sua pergunta, ela não deveria existir.",
    M + 0.45, 1.75, CW - 0.9, 1.15, 24, WHITE, bold=True, valign="middle",
    espaco=1.15)
txt(s, "A armadilha: derivar de colunas que já dizem a mesma coisa",
    M, 3.15, CW, 0.5, 25, INK, bold=True)
code(s, [
    ("Total = Lead + Feature", "dim"),
    ("", ""),
    ("proporcao = Lead / Total", "novo"),
], M, 3.75, CW, 1.75, 20, 0.45)
panel(s, M, 5.75, CW, 1.15, PEACH)
txt(s, "Essa proporção é informação de verdade, porque compara. Já uma coluna "
       "'soma = Lead + Feature' seria só o Total com outro nome, ocupando "
       "espaço e abrindo espaço para discordarem entre si.",
    M + 0.45, 5.75, CW - 0.9, 1.15, 21, ORANGE_T, bold=True, valign="middle",
    espaco=1.15)
notas(s, "Retomar a redundancia que eles descobriram no perfilamento. Derivar "
         "de coluna redundante e o erro mais comum de quem esta comecando.")

# ============================================ atributo derivado: familias
s = slide()
head(s, "Quatro famílias para começar")
for i, (fam, desc, ex) in enumerate([
        ("Razão ou taxa", "Divide para tirar o efeito do tamanho",
         "densidade, valor por habitante, percentual do total"),
        ("Variação no tempo", "Compara o registro com ele mesmo no passado",
         "crescimento anual, diferença em relação ao primeiro ano"),
        ("Faixa a partir de contínuo", "Agrupa para comparar em blocos",
         "porte, faixa etária, quartil de população"),
        ("Combinação de fontes", "Só existe depois da junção",
         "indicador por país cruzado com o nível de renda")]):
    y = 1.8 + i * 1.3
    panel(s, M, y, CW, 1.15, TINT if i % 2 == 0 else PAPER)
    shape(s, M, y, 0.09, 1.15, ORANGE if i < 3 else BLUE_M)
    txt(s, fam, M + 0.35, y, 3.3, 1.15, 23, INK, bold=True, valign="middle")
    txt(s, desc, M + 3.7, y, 4.2, 1.15, 20, BLUE_M, valign="middle", espaco=1.05)
    txt(s, ex, M + 8.0, y, CW - 8.2, 1.15, 19, MUTED, valign="middle", espaco=1.05)
nota(s, "A quarta família é a da próxima aula. As três primeiras você consegue "
        "hoje, com o que já tem em mãos.", 6.95)
notas(s, "Pedir que cada aluno escolha uma familia diferente para os tres "
         "atributos, em vez de tres razoes parecidas.")

# ================================================= por que um modulo
s = slide()
head(s, "Por que src/limpeza.py")
txt(s, "As funções de hoje servem para qualquer fonte. Tirar espaço, unificar "
       "caixa e mapear sinônimo não têm nada de Banco Mundial nem de Spotify.",
    M, 1.5, CW, 0.9, 24, INK, espaco=1.15)
panel(s, M, 2.6, 5.55, 2.6, TINT)
txt(s, "Copiadas em cada script", M + 0.4, 2.8, 4.9, 0.5, 24, INK, bold=True)
txt(s, "Um defeito descoberto obriga a corrigir em três arquivos. Alguém "
       "esquece um, e as fontes passam a discordar.",
    M + 0.4, 3.4, 4.9, 1.5, 21, MUTED, espaco=1.1)
panel(s, 6.95, 2.6, 5.55, 2.6, NAVY)
txt(s, "Num módulo importado", 7.35, 2.8, 4.9, 0.5, 24, WHITE, bold=True)
txt(s, "Uma correção conserta as três de uma vez, e fica registrada em um "
       "commit só.", 7.35, 3.4, 4.9, 1.5, 21, BLUE_L, espaco=1.1)
panel(s, M, 5.5, CW, 1.25, PEACH)
txt(s, "O teste para saber se algo vira módulo: a função menciona o nome de "
       "alguma fonte? Se menciona, fica no script daquela fonte. Se não "
       "menciona, é do módulo.", M + 0.45, 5.5, CW - 0.9, 1.25, 22, ORANGE_T,
    bold=True, valign="middle", espaco=1.15)
notas(s, "Esse criterio e simples e eles conseguem aplicar sozinhos. Vai ser "
         "reaproveitado na aula de modularizacao.")

# ================================================================ passo 1
s = slide()
step_badge(s, "PASSO 1")
step_title(s, "Ingerir a terceira fonte")
txt(s, "O script está pronto no material de apoio. Coloque em src e rode:",
    M, 2.15, CW, 0.5, 24, INK)
code(s, [("python src/ingerir_indicador.py", "")], M, 2.75, CW, 0.85, 23)
txt(s, "Ele faz três coisas novas:", M, 3.85, CW, 0.45, 24, BLUE_M, bold=True)
for i, t in enumerate([
        "Percorre todas as páginas, em vez de parar na primeira",
        "Guarda o lastupdated da fonte na proveniência",
        "Salva em dados/bronze/indicador, com a data no nome"]):
    txt(s, "• " + t, M + 0.4, 4.4 + i * 0.6, CW - 0.8, 0.55, 22, INK,
        valign="middle")
panel(s, M, 6.25, CW, 0.85, TINT)
txt(s, "Leia o laço de paginação antes de rodar. Ele é curto e você vai "
       "precisar dele de novo.", M + 0.45, 6.25, CW - 0.9, 0.85, 21, INK,
    valign="middle")
notas(s, "Rodar junto e cronometrar: sao varias paginas, entao demora alguns "
         "segundos. Bom momento para falar de gentileza com API publica.")

# ================================================================ passo 2
s = slide()
step_badge(s, "PASSO 2")
step_title(s, "Criar src/limpeza.py")
code(s, [
    ('"""Funcoes de limpeza que servem a qualquer fonte."""', "novo"),
    ("", ""),
    ("import unicodedata", "novo"),
    ("", ""),
    ("import pandas as pd", "novo"),
    ("", ""),
    ("", ""),
    ("def tirar_espacos(df):", "novo"),
    ("    df.columns = df.columns.str.strip()", "novo"),
    ('    for c in df.select_dtypes(include="object"):', "novo"),
    ("        df[c] = df[c].str.strip()", "novo"),
    ("    return df", "novo"),
], M, 2.2, CW, 4.95, 18, 0.39)
nota(s, "A função é a mesma da aula passada. Ela só mudou de casa.", 7.25)
notas(s, "Recortar e colar do transformar_paises.py. Depois apagar de la e "
         "importar. E o primeiro movimento de modularizacao da disciplina.")

# ================================================================ passo 3
s = slide()
step_badge(s, "PASSO 3")
step_title(s, "Padronizar texto para comparação")
code(s, [
    ("def chave_texto(serie):", "novo"),
    ('    """Versao comparavel de um texto: sem acento,', "novo"),
    ('    sem espaco sobrando e tudo em minuscula."""', "novo"),
    ("    s = serie.str.strip().str.lower()", "novo"),
    ('    s = s.str.normalize("NFKD")', "novo"),
    ('    s = s.str.encode("ascii", errors="ignore")', "novo"),
    ('    return s.str.decode("utf-8")', "novo"),
], M, 2.2, CW, 3.4, 18, 0.42)
panel(s, M, 5.75, CW, 1.3, PEACH)
txt(s, "Repare no nome: chave_texto, não limpar_texto. O resultado serve para "
       "comparar e juntar, não para exibir. O rótulo original continua na "
       "tabela.", M + 0.45, 5.75, CW - 0.9, 1.3, 22, ORANGE_T, bold=True,
    valign="middle", espaco=1.15)
notas(s, "A cadeia normalize, encode, decode e o jeito padrao de tirar acento "
         "em pandas. Vale explicar que o NFKD separa a letra do acento e o "
         "encode descarta o que nao for ascii.")

# ================================================================ passo 4
s = slide()
step_badge(s, "PASSO 4")
step_title(s, "Mapear sinônimos explicitamente")
code(s, [
    ("def aplicar_mapa(serie, mapa):", "novo"),
    ('    """Troca variantes pelo valor canonico.', "novo"),
    ('    O que nao estiver no mapa fica como esta."""', "novo"),
    ("    return serie.replace(mapa)", "novo"),
    ("", ""),
    ("# no script da sua fonte, nao no modulo:", "dim"),
    ("MAPA_UF = {", "novo"),
    ('    "sao paulo": "SP",', "novo"),
    ('    "s. paulo": "SP",', "novo"),
    ("}", "novo"),
], M, 2.2, CW, 4.5, 18, 0.4)
nota(s, "A função é genérica e mora no módulo. O dicionário é específico da sua "
        "fonte e mora no script dela.", 6.85)
notas(s, "Aqui o criterio do slide do modulo se aplica na pratica e eles veem a "
         "divisao acontecer.")

# ================================================================ passo 5
s = slide()
step_badge(s, "PASSO 5")
step_title(s, "Importar o módulo no script da fonte")
code(s, [
    ("# no topo de transformar_paises.py", "dim"),
    ("import limpeza", "novo"),
    ("", ""),
    ("# e dentro da main, no lugar da funcao antiga:", "dim"),
    ("df = limpeza.tirar_espacos(df)", "novo"),
], M, 2.2, CW, 2.5, 20, 0.45)
panel(s, M, 5.0, CW, 1.7, TINT)
txt(s, "Para o import funcionar, rode a partir da raiz do projeto e mantenha "
       "os dois arquivos em src. Se der ModuleNotFoundError, quase sempre é "
       "porque o comando foi executado de dentro da pasta errada.",
    M + 0.45, 5.0, CW - 0.9, 1.7, 22, INK, valign="middle", espaco=1.15)
notas(s, "Erro garantido em pelo menos um aluno. Antecipar economiza dez "
         "minutos.")

# ================================================================ passo 6
s = slide()
step_badge(s, "PASSO 6")
step_title(s, "Tipar a coluna de nível de renda")
code(s, [
    ("# em transformar_paises.py", "dim"),
    ("ORDEM_RENDA = [", "novo"),
    ('    "Low income", "Lower middle income",', "novo"),
    ('    "Upper middle income", "High income",', "novo"),
    ("]", "novo"),
    ("", ""),
    ("def tipar_renda(df):", "novo"),
    ('    coluna = "incomeLevel.value"', "novo"),
    ("    antes = df[coluna].isna().sum()", "novo"),
    ("    df[coluna] = pd.Categorical(", "novo"),
    ("        df[coluna], categories=ORDEM_RENDA, ordered=True)", "novo"),
    ('    print("renda fora da escala:",', "novo"),
    ("          df[coluna].isna().sum() - antes)", "novo"),
    ("    return df", "novo"),
], M, 2.2, CW, 5.05, 17, 0.37)
notas(s, "O print e o que impede a conversao de apagar dado em silencio. "
         "Repetir o padrao: toda transformacao conta o que mudou.")

# ================================================================ passo 7
s = slide()
step_badge(s, "PASSO 7")
step_title(s, "Transformar a fonte nova")
txt(s, "Crie src/transformar_indicador.py e resolva três coisas:",
    M, 2.15, CW, 0.5, 24, INK)
for i, (item, desc) in enumerate([
        ("O ano fica inteiro",
         "pd.to_numeric na coluna date, e nada de converter para data."),
        ("As colunas vazias saem",
         "unit, obs_status e decimal não carregam informação nenhuma. "
         "Conte antes de apagar e registre."),
        ("Os agregados continuam lá",
         "E desta vez não há coluna de região para filtrá-los. Guarde a "
         "pergunta: ela se resolve na próxima aula.")]):
    y = 2.8 + i * 1.35
    panel(s, M, y, CW, 1.2, TINT if i % 2 == 0 else PAPER)
    shape(s, M, y, 0.09, 1.2, ORANGE if i < 2 else BLUE_M)
    txt(s, item, M + 0.35, y + 0.1, CW - 0.7, 0.45, 23, INK, bold=True)
    txt(s, desc, M + 0.35, y + 0.58, CW - 0.7, 0.55, 21, MUTED, espaco=1.05)
notas(s, "O terceiro item e proposital e importante: eles precisam sentir falta "
         "do join antes de aprender o join.")

# ================================================================ passo 8
s = slide()
step_badge(s, "PASSO 8")
step_title(s, "Primeiro atributo derivado: variação no tempo")
code(s, [
    ("def variacao_anual(df, chave, tempo, valor):", "novo"),
    ("    df = df.sort_values([chave, tempo])", "novo"),
    ('    df["variacao_pct"] = (', "novo"),
    ("        df.groupby(chave)[valor].pct_change() * 100)", "novo"),
    ("    return df", "novo"),
    ("", ""),
    ("df = variacao_anual(", "novo"),
    ('    df, "countryiso3code", "date", "value")', "novo"),
], M, 2.2, CW, 3.8, 18, 0.42)
panel(s, M, 6.15, CW, 1.0, PEACH)
txt(s, "O sort_values não é enfeite. Sem ordenar primeiro, a variação é "
       "calculada contra a linha anterior do arquivo, que pode ser outro ano "
       "ou outro país.", M + 0.45, 6.15, CW - 0.9, 1.0, 21, ORANGE_T, bold=True,
    valign="middle", espaco=1.1)
notas(s, "Erro classico e silencioso: pct_change sem ordenar. O resultado sai, "
         "parece plausivel e esta errado.")

# ================================================================ passo 9
s = slide()
step_badge(s, "PASSO 9")
step_title(s, "Segundo atributo: faixa a partir de contínuo")
code(s, [
    ("def faixa_por_quartil(df, coluna, rotulos):", "novo"),
    ('    df[coluna + "_faixa"] = pd.qcut(', "novo"),
    ("        df[coluna], q=4, labels=rotulos)", "novo"),
    ("    return df", "novo"),
    ("", ""),
    ("df = faixa_por_quartil(df, \"value\",", "novo"),
    ('    ["muito pequeno", "pequeno", "grande", "muito grande"])', "novo"),
], M, 2.2, CW, 3.4, 18, 0.42)
panel(s, M, 5.75, CW, 1.35, TINT)
txt(s, "qcut corta por quantidade de registros, então cada faixa fica com um "
       "quarto dos casos. cut corta por valor, em faixas de largura igual. São "
       "resultados diferentes, e a escolha depende da pergunta.",
    M + 0.45, 5.75, CW - 0.9, 1.35, 21, INK, valign="middle", espaco=1.15)
notas(s, "Vale rodar os dois e comparar a contagem por faixa. A diferenca "
         "costuma ser gritante em dado com cauda longa.")

# =============================================================== passo 10
s = slide()
step_badge(s, "PASSO 10")
step_title(s, "Terceiro atributo: escolha sua")
panel(s, M, 2.25, CW, 1.3, NAVY)
txt(s, "Crie um atributo que sirva à pergunta norteadora que você escreveu na "
       "primeira entrega. Volte nela antes de decidir.",
    M + 0.45, 2.25, CW - 0.9, 1.3, 25, WHITE, bold=True, valign="middle",
    espaco=1.15)
txt(s, "Ele precisa passar no critério:", M, 3.8, CW, 0.5, 24, BLUE_M, bold=True)
for i, t in enumerate([
        "Uma frase explica por que essa coluna ajuda a responder a pergunta",
        "Ela não repete informação que já existe em outra coluna",
        "O cálculo está em uma função, com nome que diz o que ela faz"]):
    y = 4.4 + i * 0.7
    marker(s, i + 1, M, y, ORANGE, 0.42)
    txt(s, t, M + 0.75, y - 0.05, CW - 0.75, 0.5, 22, INK, valign="middle")
nota(s, "Se nenhum atributo ocorrer, o problema pode ser a pergunta. Fale "
        "comigo antes do fim da aula.", 6.6)
notas(s, "Circular pela sala nessa hora. E o momento em que da para perceber "
         "quem escolheu uma pergunta fraca la atras.")

# =============================================================== passo 11
s = slide()
step_badge(s, "PASSO 11")
step_title(s, "Registrar no README")
code(s, [
    ("## Atributos derivados", "dim"), ("", ""),
    ("### variacao_pct", "novo"),
    ("Variacao percentual do indicador em relacao ao ano", "novo"),
    ("anterior, por pais. Serve para comparar ritmo de", "novo"),
    ("crescimento entre paises de tamanhos diferentes.", "novo"),
    ("Ausente no primeiro ano de cada pais, por definicao.", "novo"),
    ("", ""),
    ("### value_faixa", "novo"),
    ("Quartil de populacao. Serve para agrupar paises", "novo"),
    ("comparaveis sem escolher corte arbitrario.", "novo"),
], M, 2.2, CW, 4.55, 17, 0.38)
nota(s, "Para cada atributo: o que é, por que existe, e o que ele faz quando o "
        "dado não permite calcular.", 6.9)
notas(s, "A terceira frase e a que mais falta nos trabalhos: dizer o que "
         "acontece no caso limite.")

# =============================================================== passo 12
s = slide()
step_badge(s, "PASSO 12")
step_title(s, "Rodar tudo e conferir")
code(s, [
    ("python src/transformar_paises.py", ""),
    ("python src/transformar_indicador.py", ""),
], M, 2.2, CW, 1.35, 22, 0.45)
txt(s, "Três conferências antes de commitar:", M, 3.8, CW, 0.5, 24, BLUE_M,
    bold=True)
for i, (item, desc) in enumerate([
        ("Nenhuma conversão comeu dado sem avisar",
         "Os prints de antes e depois batem com o esperado."),
        ("Os atributos novos têm valores plausíveis",
         "Uma variação de 4000% costuma ser divisão por um valor quase zero."),
        ("A proveniência ganhou a linha de hoje",
         "Com as decisões novas listadas, não só as da aula passada.")]):
    y = 4.35 + i * 0.95
    panel(s, M, y, CW, 0.85, TINT if i % 2 == 0 else PAPER)
    txt(s, item, M + 0.35, y, 5.6, 0.85, 21, INK, bold=True, valign="middle")
    txt(s, desc, M + 6.1, y, CW - 6.3, 0.85, 20, MUTED, valign="middle",
        espaco=1.05)
notas(s, "O exemplo dos 4000% e real e comum em variacao percentual. Vale "
         "mostrar como se investiga: olhar a linha, nao so o numero.")

# ============================================================= fechamento
s = slide(NAVY)
head_dark(s, "Antes de fechar o computador")
for i, t in enumerate([
        "As três fontes estão na Bronze, com proveniência",
        "src/limpeza.py existe e é importado pelos scripts",
        "Os tipos estão declarados, não adivinhados",
        "Três atributos derivados, cada um com uma frase de justificativa",
        "Commit e push feitos"]):
    y = 1.9 + i * 0.92
    shape(s, M, y + 0.08, 0.34, 0.34, NAVY_D, linha=BLUE_L)
    txt(s, t, M + 0.65, y, CW - 0.65, 0.5, 25, WHITE, valign="middle")
txt(s, "Na próxima aula: juntar as fontes, e descobrir o que não casa.",
    M, 6.5, CW, 0.6, 23, BLUE_L)
notas(s, "Fechar confirmando com cada aluno qual e a fonte secundaria que sera "
         "integrada. Sem isso a proxima aula trava.")

# ============================================================ aprofundar
s = slide()
head(s, "Para aprofundar")
for i, (tipo, ref) in enumerate([
        ("Leitura principal",
         "MCKINNEY, W. Python para análise de dados. 3. ed. Novatec, 2023. "
         "Capítulos de manipulação de texto e de séries temporais."),
        ("Documentação",
         "Guia de dados categóricos e guia de séries temporais do pandas. "
         "São as duas páginas que respondem quase tudo de hoje."),
        ("Para quem quiser mais",
         "Documentação da API de indicadores do Banco Mundial, para descobrir "
         "outras séries úteis ao seu tema.")]):
    y = 1.95 + i * 1.5
    panel(s, M, y, CW, 1.3, TINT)
    shape(s, M, y, 0.09, 1.3, BLUE_M)
    txt(s, tipo, M + 0.35, y, 3.4, 1.3, 23, INK, bold=True, valign="middle")
    txt(s, ref, M + 3.85, y, CW - 4.05, 1.3, 21, MUTED, valign="middle", espaco=1.1)
notas(s, "O catalogo de indicadores do Banco Mundial e enorme. Quem tem tema de "
         "economia, saude ou educacao provavelmente acha serie pronta la.")


SAIDA = "ECOX14_Aula06_Limpeza_e_Atributos.pptx"
prs.save(SAIDA)
print("pronto:", SAIDA, "-", len(prs.slides), "slides")