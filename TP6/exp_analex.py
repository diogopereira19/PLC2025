# TPC 6

import ply.lex as lex

tokens = ('NUM', 'PA', 'PF', 'OP_SOMA', 'OP_MULT')

t_NUM = r'\d+'
t_PA = r'\('
t_PF = r'\)'
t_OP_SOMA = r'(\+|\-)'
t_OP_MULT = r'(\*|/)'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = '\t '

def t_error (t):
    print('Carácter desconhecido: ', t.value[0], 'Linha: ', t.lexer.lineno)
    t.lexer.skip(1)

lexer = lex.lex()
