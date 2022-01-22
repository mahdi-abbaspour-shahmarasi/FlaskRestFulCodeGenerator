from art import *
import os
from pynput import keyboard

def clearScreen():
  os.system('cls' if os.name=='nt' else 'clear')
clearScreen()
tprint('CodeGenerator')
print('====================================================================================')
print('1. Generate Code Step By Step')
print('2. Generate Code By Existing Class')
print('3. Help')
print('4. About')
print('0. Exit')
print('====================================================================================')

#accept only numeric input
def getInput():
    global inp_value
    inp_value = input("Select Menu Item:")
    while not inp_value.isnumeric():
        print("Please enter a number.")
        inp_value = input("Select Menu Item:")
    return int(inp_value)

#check and return field type
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

#define menu items as functions
def item1():
    print('==== Generate Code Step By Step ====\n')

    class_name=input("Please enter class name: ")
    print("class name is:",class_name+"\n")

    print("Please complete class details.")
 
    class_fields_name=[]
    class_fields_type=[]
    class_fields_req=[]

    while True:   
        _name = input("Enter field name: ")
        if not _name:
            print("done.")
            break

        _type = input("Enter field type: ")
        _isRequirement = input("The field is requirement? (True/Flase): ")
        
        class_fields_name.append(_name)
        class_fields_type.append(_type)

        # default value is True
        _isRequirement=_isRequirement.capitalize()
        if _isRequirement!="True" and _isRequirement!="False":
            _isRequirement="True"
        class_fields_req.append(_isRequirement)
        
        print("\n"+class_name+" class info:")
        for _n,_t,_r in zip(class_fields_name,class_fields_type,class_fields_req):
            print("field name: "+_n+"\t field type: "+_t+"\t field requirement: "+_r)
        
    

    print("Creating class file ...")
    print("=========================")

    textfile = open(class_name+".py", "w")
    textfile.write(
    "from typing import ClassVar\nfrom .db import db\nimport datetime\nfrom flask_bcrypt import generate_password_hash, check_password_hash\n"+
    "\nclass "+class_name+"(db.Document):\n")


    for _fieldName,_fieldType,_fieldRequirement in zip(class_fields_name,class_fields_type,class_fields_req):
        _fieldType=getFieldType(_fieldType)

        textfile.write("\t"+_fieldName+ " = db."+_fieldType+"(required="+_fieldRequirement+")\n")

    textfile.close()

    print("Class file successfully created -> name: "+class_name+".py")

def item2():
    print("this is item 2")

def item3():
    print("this is item 3")

def item4():
    print("this is item 4")

def item0():    
    exit()

func_keys={
    '0':item0,
    '1':item1,
    '2':item2,
    '3':item3,
    '4':item4,
}

def main(func_keys,user_cmd):
        count=len(func_keys.keys())
        if count > int(user_cmd):
            func_keys[user_cmd]()
        else:
            print("There is no items, please select other item.")

getInput()
user_cmd=inp_value

main(func_keys,user_cmd)