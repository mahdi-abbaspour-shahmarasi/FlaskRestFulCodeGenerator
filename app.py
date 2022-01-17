from art import *
import os
def clearScreen():
  os.system('cls' if os.name=='nt' else 'clear')
clearScreen()
tprint('CodeGenerator')
print('====================================================================================')
print('0. Generate Code Step By Step')
print('1. Generate Code By Existing Class')
print('2. Help')
print('3. About')
print('4. Exit')
print('====================================================================================')
input('Select Menu Item: ')
