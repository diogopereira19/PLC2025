# TPC 6

from exp_analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

# P1: Expressao --> Conteudo Op Conteudo
# P2: Conteudo  --> '(' Expressao ')'
# P3:             | Num

def rec_Expressao():
    global prox_simb
    print("Derivando por P1: Expressao --> Conteudo Op Conteudo")
    rec_Conteudo()
    rec_term('OP')
    rec_Conteudo()
    print("Reconheci P1: Expressao --> Conteudo Op Conteudo")

def rec_Conteudo():
    global prox_simb
    if prox_simb.type == 'PA':
        print("Reconheci por P2: Conteudo --> '(' Expressao ')'")
        rec_term('PA')
        rec_Expressao()
        rec_term('PF')
        print("Reconheci P2: Conteudo --> '(' Expressao ')'")
    elif prox_simb.type == 'NUM':
        print("Derivando por P3: Conteudo --> Num")
        rec_term('NUM')
        print("Reconheci P3: Conteudo --> Num")
    else:
        parserError(prox_simb)

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Expressao()
    print("That's all folks!")