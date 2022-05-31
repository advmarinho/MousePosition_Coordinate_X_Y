import pyautogui
from random import *

cont = 0
while cont <= 20:
    img = pyautogui.screenshot(region=(0,0, 300, 400))
    img.save('C:\\_RPA\\img\\my_screenshot' + str(cont) +'.png')
    cont += int(input('Digite [1] e [enter] para fazer screenshot: '))
    print('\n\33[1;32m[my_screenshot - ',cont,']', '\033[m')
else:
    print('\n\33[1;31m[Fim]', '\033[m')



