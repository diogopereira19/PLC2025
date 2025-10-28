import ply.lex as lex
import json

STOCK_FILE = 'stock.json'
STOCK = []
SALDO = 0

valores = {
    "2e": 200, "1e": 100, "50c": 50, "20c": 20,
    "10c": 10, "5c": 5, "2c": 2, "1c": 1
}

tokens = (
    'COM_LISTAR',
    'COM_SAIR',
    'COM_MOEDA',
    'COM_SELECIONAR',

    'ARTIGO',
    'VALOR',
    'VIRGULA'
)

def carregar_stock():
    global STOCK
    
    with open(STOCK_FILE, 'r', encoding='utf-8') as f:
        STOCK = json.load(f)

    print("maq: STOCK carregado. Estado atualizado")

def guardar_stock():
    with open(STOCK_FILE, 'w', encoding='utf-8') as f:
        json.dump(STOCK, f, indent=4)

def formatar_saldo(SALDO_cent):

    euros = SALDO_cent // 100
    centos = SALDO_cent % 100
    
    if euros > 0 and centos > 0:
        return f"{euros}e{centos}c" # Ex: 1e30c 
    elif euros > 0: # e centos == 0
        return f"{euros}e" # Ex: 2e
    else: # euros == 0
        return f"{centos}c"

def encontra_STOCK(codigo):
    global STOCK
    for item in STOCK:
        if codigo == item['cod']:
            return item
    return None

def calcular_troco(saldo_a_devolver):
    if saldo_a_devolver <= 0:
        return "Sem troco."

    # Moedas disponíveis para troco, em cêntimos (por ordem decrescente)
    moedas = [
        (200, "2e"), (100, "1e"), (50, "50c"), (20, "20c"), 
        (10, "10c"), (5, "5c"), (2, "2c"), (1, "1c")
    ]
    
    troco_str_list = []
    
    # Algoritmo "guloso" para calcular o troco
    for valor_cent, nome in moedas:
        if saldo_a_devolver >= valor_cent:
            # Quantas moedas deste valor cabem no saldo
            quantidade = saldo_a_devolver // valor_cent
            # O que sobra do saldo
            saldo_a_devolver %= valor_cent
            # Adiciona à lista de strings (ex: "1x 50c")
            troco_str_list.append(f"{quantidade}x {nome}")
            
    # Junta as strings com vírgulas e adiciona o ponto final (conforme o exemplo)
    return ", ".join(troco_str_list) + "."

def t_COM_LISTAR(t):
    r'LISTAR'

    print("maq:")
    """if STOCK:
        max_len_nome = max(len(item['nome']) for item in STOCK)"""
    
    #print(f" {'cod':<3} | {'nome':<{max_len_nome}} | {'quantidade':>10} | {'preço':>5}")
    print(f" {'cod'} | {'nome'} | {'quantidade'} | {'preço'}")
    print("---------------------------------------")

    for item in STOCK:
        print(f" {item['cod']} | {item['nome']} | {item['quant']} | {item['preco']}")
    print()
    return t

def t_COM_SAIR(t):
    r'SAIR'
    global SALDO

    troco_formatado = calcular_troco(SALDO)
    print(f"maq: Pode retirar o troco: {troco_formatado}.")
    
    SALDO = 0

    print("maq: Até à próxima")
    guardar_stock()

    return t

def t_COM_SELECIONAR(t):
    r'SELECIONAR'
    global SALDO
    global STOCK

    tok = t.lexer.token()
    if tok is None or tok.type != 'ARTIGO':
        print("maq: ERRO: Deve indicar um código de artigo (ex: SELECIONAR A23).")
        return t

    cod_artigo = tok.value
    produto = encontra_STOCK(cod_artigo)

    if produto is None:
        print(f"maq: ERRO: Produto com código '{cod_artigo}' não existe.")
        return t
    
    nome = produto["nome"]
    preco = produto["preco"]
    preco_cent = int(round(preco * 100))
    quantidade = produto["quant"]

    if quantidade <= 0:
        print(f"maq: Produto '{nome}' esgotado.")
        return t
    
    if SALDO >= preco_cent:
        SALDO -= preco_cent
        produto["quant"] -= 1

        print(f"maq: Pode retirar o produto dispensado {nome}.")
        print(f"Saldo = {formatar_saldo(SALDO)}")

    else:
        print(f"Saldo insuficiente para satisfazer o seu pedido.")
        print(f"Saldo = {formatar_saldo(SALDO)}; Pedido = {formatar_saldo(preco_cent)}")
    return t

def t_COM_MOEDA(t):
    r'MOEDA'
    global SALDO
    total_adicionado = 0

    while True:
        tok = t.lexer.token()

        if tok is None:
            break
        if tok.type == 'VALOR':
            valor = valores.get(tok.value,0)
            total_adicionado += valor
        elif tok.type == 'VIRGULA':
            continue
        else:
            print(f"maq:AVISO: Input inesperado '{tok.value}' após MOEDA.")
            break

    SALDO += total_adicionado
    
    # Imprime a mensagem de SALDO conforme o enunciado 
    print(f"maq: Saldo = {formatar_saldo(SALDO)}")
    
    return t

t_VIRGULA = r','
t_VALOR = r'(2e|1e|50c|20c|10c|5c|2c|1c)'
t_ARTIGO = r'[A-Z]\d+'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'

def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()