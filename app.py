from art import *
import os
from pynput import keyboard

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


#accept only numeric input
def getInput():
    global inp_value
    inp_value = input("Select Menu Item:")
    while not inp_value.isnumeric():
        print("Please enter a number.")
        inp_value = input("Select Menu Item:")
    return int(inp_value)

def getFieldType(field):
    _type = ""
    if field == "string" or field == "str":
        _type = "StringField"

    elif field == "int":
        _type = "IntegerField"

    elif field == "datetime":
        _type = "DateTimeField"

    else:
        _type="Field"
    return _type


getInput()

user_cmd=inp_value


#define menu options as functions
def option0():
    print('==== Generate Code Step By Step ====\n')

    class_name=input("Please enter class name: ")
    print("class name is:",class_name+"\n")

    print("Enter fields name and types separated by ',' and space")
    print("like => name,string age,int\n")
    
    input_list = input()
    #split fields
    class_fields_list = input_list.split()

    print(class_name,'fields are: ', class_fields_list)
    print("Creating class file ...")
    print("=========================")

    textfile = open(class_name+".py", "w")
    textfile.write(
    "from typing import ClassVar\nfrom .db import db\nimport datetime\nfrom flask_bcrypt import generate_password_hash, check_password_hash\n"+
    "\nclass "+class_name+"(db.Document):\n")


    for fields in class_fields_list:
        #split field and type
        field=fields.split(',')

        _fieldName=field[0]
        _fieldType=getFieldType(field[1])

        textfile.write("\t"+_fieldName+ " = db."+_fieldType+"(required=True)\n")

    textfile.close()

    print("Class file created with "+class_name+".py"+" name.")


def option1():
    print("this is option 1")

def option2():
    print("this is option 2")

def option3():
    print("this is option 3")

def option4():
    print("this is option 4")


def main(func_keys,user_cmd):
        count=len(func_keys.keys())
        if count > int(user_cmd):
            func_keys[user_cmd]()
        else:
            print("There is no options, please select other option.")

func_keys={
    '0':option0,
    '1':option1,
    '2':option2,
    '3':option3,
    '4':option4,
}
main(func_keys,user_cmd)