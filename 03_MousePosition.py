import pyautogui as abrirsite
import os


print("\t |#############################################################| \t")
print("\t |#############################################################| \t")
print("\t |**Robô encontra-se atuando na tarefa de abrir Site Pontotel**| \t")
print("\t |ABRIR O SITE, COLETAR ARQUIVO R09 E TRATAR EXCEL INICIALMENTE| \t")
print("\t |                         \      /                            | \t")
print("\t |                         (\____/)                            | \t")
print("\t |                          (_oo_)                             | \t")
print("\t |                           ([])                              | \t")
print("\t |                          __||__    \)  Oi, sou seu RPA      | \t")
print("\t |                       []/______\[] /                        | \t")
print("\t |                       / \______/ \/                         | \t")
print("\t |                      /    /__\                              | \t")
print("\t |                     (\   /____\      by Ads Anderson        | \t")
print("\t |#############################################################| \n\n\t")

#  C:\Users\marin\Documents\_class\_GitHub\_Aulas   pyinstaller --onefile --noconsole .\rpacalc.py
#  Código para capturar a posição do mouse e melhorar a construção de RPA com a função Pyautogui
#  Foi criado a função e a entrada e saída para o sistema se mante funcionando com o enter e nº 2    

def posicaoMouse(): 
    var = input("\n Buscar posicao do mouse na tela, Enter=(x,y) e 2=(sair):  ").lower()
    if var == input(' Pressione enter novamente \n'):        
        print(abrirsite.position(), '<-------Copiar posicao\n')
        
    if var == '2':
        exit()

while True:
    posicaoMouse()
#  Final do código fechando ação.