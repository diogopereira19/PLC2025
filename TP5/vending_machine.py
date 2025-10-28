import vending_lexer as vlex
import sys

programa_a_terminar = False # Flag de controlo

vlex.carregar_stock()
print("maq: Bom dia. Estou disponível para atender o seu pedido.")

for linha in sys.stdin:
    vlex.lexer.input(linha)
    
    for tok in vlex.lexer:
        if tok.value == 'SAIR':
            programa_a_terminar = True
            break  # Quebra o loop do lexer para esta linha
    
    if programa_a_terminar:
        break