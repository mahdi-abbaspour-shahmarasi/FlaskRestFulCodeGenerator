from genericpath import isdir
from art import *
import os
from pynput import keyboard


def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')


clearScreen()
tprint('CodeGenerator')
print('====================================================================================')
print('1. Generate Code Step By Step')
print('2. Generate Code By Existing Class')
print('3. Help')
print('4. About')
print('0. Exit')
print('====================================================================================')

# accept only numeric input


def getInput():
    global inp_value
    inp_value = input("Select Menu Item:")
    while not inp_value.isnumeric():
        print("Please enter a number.")
        inp_value = input("Select Menu Item:")
    return int(inp_value)

# check and return field type


def getFieldType(field):
    _type = ""
    if field == "string" or field == "str":
        _type = "StringField"

    elif field == "int":
        _type = "IntegerField"

    elif field == "datetime":
        _type = "DateTimeField"

    else:
        _type = "Field"
    return _type

# define menu items as functions


def item1():
    print('==== Generate Code Step By Step ====\n')

    class_name = input("Please enter class name: ")
    print("class name is:", class_name+"\n")

    print("Please complete class details.")

    class_fields_name = []
    class_fields_type = []
    class_fields_req = []

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
        _isRequirement = _isRequirement.capitalize()
        if _isRequirement != "True" and _isRequirement != "False":
            _isRequirement = "True"
        class_fields_req.append(_isRequirement)

        print("\n"+class_name+" class info:")
        for _n, _t, _r in zip(class_fields_name, class_fields_type, class_fields_req):
            print("field name: "+_n+"\t field type: " +
                  _t+"\t field requirement: "+_r)

    print("Creating class file ...")
    print("=========================")

    #check to exist src directory
    if not isdir("src"):
        os.mkdir("src")
        os.mkdir("src/Api")
        os.mkdir("src/Models")
    class_text="""from typing import ClassVar
from .db import db
import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
"""

    #create class file        
    classFile = open("src/Models/"+class_name+".py", "w")
    classFile.write(class_text+
        "\nclass "+class_name+"(db.Document):\n")

    for _fieldName, _fieldType, _fieldRequirement in zip(class_fields_name, class_fields_type, class_fields_req):
        _fieldType = getFieldType(_fieldType)

        classFile.write("\t"+_fieldName + " = db."+_fieldType +
                       "(required="+_fieldRequirement+")\n")

    classFile.close()

    api_text = """from flask import jsonify, make_response, request
from src.Models import {ClassName}
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from flask_bcrypt import generate_password_hash
import re
from collections import deque

class GetApi(Resource):
    def get(slef):
        {listName}=[]
        for {class_var} in {ClassName}.objects:
            {listName}.append({class_var})  
        return make_response(jsonify({listName}), 200)

class PostApi(Resource):
    def post(self):
        body = request.get_json()
        id = body['id']
        {class_var} = {ClassName}.objects(id=id)
        if {class_var}.count() > 0:
            body=deque(body)
            # pop id field - we dont update id field
            body=body.pop()
            for {var} in body:
                var={var}
                val=body[{var}]
                {class_var}.update(var=val)
            return make_response(jsonify({class_var}), 200)
        else:
            return make_response(jsonify({{'Message': 'Not Found'}}), 200)  

class PutApi(Resource):
    def put(slef):
        body = request.get_json()
        {class_var} = {ClassName}(**body)
        {class_var}.save()
        return make_response(jsonify({{'Message': 'Successfully created with ID'+str({class_var}.id)}}), 200)

class DeleteApi(Resource):
    def delete(slef):
        body = request.get_json()
        id = body['id']
        {class_var} = {ClassName}.objects(id=id)
        if {class_var}.count() > 0:
            {class_var}.delete()
            return make_response(jsonify({{'Message':'Successfully deleted.'}}), 200)
        else:
            return make_response(jsonify({{'Message': 'Not Found'}}), 200)        

     """

    #create api file
    _class_var=class_name.lower()
    _listName=class_name.lower()+"List"
    _var="_"+class_name.lower()

    apiFile = open("src/Api/"+class_name+".py", "w")
    apiFile.write(api_text.format(ClassName=class_name,listName=_listName,class_var=_class_var,var=_var))
    apiFile.close()

    route_text="""# === {className} Api ===

from Api.{className} import GetApi, PostApi, PutApi, DeleteApi

def initialize_routes(api):
 api.add_resource(GetApi, '/{className}/get')
 api.add_resource(PostApi, '/{className}/post')
 api.add_resource(PutApi, '/{className}/put')
 api.add_resource(DeleteApi, '/{className}/delete')

"""
    
    #create route file
    routeFile=open("src/route.py","a")
    routeFile.write(route_text.format(className=class_name))
    routeFile.close()

    print("Class file successfully created -> path: src/Models/"+class_name+".py")
    print("Api file successfully created -> path: src/Api/api.py")
    print("Route file successfully Edited -> path: src/route.py")


def item2():
    print("this is item 2")


def item3():
    print("this is item 3")


def item4():
    print("this is item 4")


def item0():
    exit()


func_keys = {
    '0': item0,
    '1': item1,
    '2': item2,
    '3': item3,
    '4': item4,
}


def main(func_keys, user_cmd):
    count = len(func_keys.keys())
    if count > int(user_cmd):
        func_keys[user_cmd]()
    else:
        print("There is no items, please select other item.")


getInput()
user_cmd = inp_value

main(func_keys, user_cmd)
