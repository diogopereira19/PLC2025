# TPC 6

from exp_analex import lexer

prox_simb = ('Erro', '', 0, 0)

def parserError(simb):
    print("Erro sintático, token inesperado: ", simb)

def rec_term(simb):
    global prox_simb
    if prox_simb and prox_simb.type == simb:
        prox_simb = lexer.token()
    else:
        parserError(prox_simb)

# P1: Expressao  --> Termo RestoExpressao
# P2: Termo      --> Fator RestoTermo
# P3: Fator      --> NUM
# P4:              | '(' Expressao ')'

# P5: RestoTermo --> OP_MULT Fator RestoTermo
# P6:              | ε

# P7: RestoExpressao --> OP_SOMA Termo RestoExpressao
# P8:                  | ε

def rec_Expressao():
    global prox_simb
    print("Derivando por P1: Expressao --> Termo RestoExpressao")
    rec_Termo()
    rec_RestoExpressao()
    print("Reconheci P1: Expressao --> Termo RestoExpressao")

def rec_Termo():
    global prox_simb
    print("Derivando por P2: Termo --> Fator RestoTermo")
    rec_Fator()
    rec_RestoTermo()
    print("Reconheci P2: Termo --> Fator RestoTermo")

def rec_Fator():
    global prox_simb
    if prox_simb and prox_simb.type == "NUM":
        print("Derivando por P3: Fator --> Num")
        rec_term("NUM")
        print("Reconheci P3: Fator --> Num")
    elif prox_simb and prox_simb.type == "PA":
        print("Derivando P4: Fator --> '(' Expressao ')'")
        rec_term("PA")
        rec_Expressao()
        rec_term("PF")
        print("Reconheci P4: Fator --> '(' Expressao ')")
    else:
        parserError(prox_simb)

def rec_RestoTermo():
    global prox_simb
    if prox_simb and prox_simb.type == "OP_MULT":
        print("Reconheci por P5: RestoTermo --> OP_MULT Fator RestoTermo")
        rec_term("OP_MULT")
        rec_Fator()
        rec_RestoTermo()
        print("Reconheci P5: RestoTermo --> OP_MULT Fator RestoTermo")
    else:
        print("Derivando por P6: RestoTermo --> ε")
        print("Reconheci P6: RestoTermo --> ε")

def rec_RestoExpressao():
    global prox_simb
    if prox_simb and prox_simb.type == "OP_SOMA":
        print("Derivando P7: RestoExpressao --> OP_SOMA Termo RestoExpressao")
        rec_term("OP_SOMA")
        rec_Termo()
        rec_RestoExpressao()
        print("Reconheci P7: RestoExpressao --> OP_SOMA Termo RestoExpressao")
    else:
        print("Derivando por P7: RestoExpressao --> ε")
        print("Reconheci P7: RestoExpressao --> ε")

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Expressao()
    print("That's all folks!")
