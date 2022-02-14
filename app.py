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
        _type = "IntField"

    elif field == "float":
        _type = "FloatField"

    elif field == "bool" or field == "boolean":
        _type = "BooleanField"

    elif field == "datetime":
        _type = "DateTimeField"

    else:
        # defualt type is string
        _type = "StringField"
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
        class_fields_type.append(getFieldType(_type))

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

    #check to exist output directory
    if not isdir("output"):
        os.mkdir("output")
        os.mkdir("output/database")
        os.mkdir("output/resources")
        os.mkdir("output/routes")
        
    class_text="""from typing import ClassVar
from database.db import db
import datetime
"""

    #create class file        
    classFile = open("output/database/"+class_name+".py", "w")
    classFile.write(class_text+
        "\nclass "+class_name+"(db.Document):\n")

    for _fieldName, _fieldType, _fieldRequirement in zip(class_fields_name, class_fields_type, class_fields_req):
        _fieldType = _fieldType
        if _fieldType=="DateTimeField":
            classFile.write("\t"+_fieldName + " = db."+_fieldType +
                       "(default=datetime.datetime.utcnow)\n")           
        else:    
            classFile.write("\t"+_fieldName + " = db."+_fieldType +
                       "(required="+_fieldRequirement+")\n")

    classFile.close()
    # perm_var=class_name[:-1]

    perm_var= class_name[:-1] if class_name[-1]=='s' else class_name

    api_text = """from flask import jsonify, make_response, request
from database.{ClassName} import {ClassName}
from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity,get_jwt

class {ClassName}Api(Resource):
    # get all {class_var}
    @jwt_required()
    def get(slef):
        claims = get_jwt()['perms']
        if not(("get{ClassName}List" in claims) or "administrator" in claims):
            return make_response(jsonify({{"Message":"Not Allowed"}}), 406)         
        {class_var} = {ClassName}.objects.all()
        return make_response(jsonify({class_var}), 200)

    # update {class_var}
    @jwt_required()
    def post(self):
        claims = get_jwt()['perms']
        if not(("update{perm_var}" in claims) or "administrator" in claims):
            return make_response(jsonify({{"Message":"Not Allowed"}}), 406)         
        body = request.get_json()
        id = body["id"]
        {class_var} = {ClassName}.objects(id=id)
        if {class_var}.count() > 0:
            
            # delete id field
            del body['id']
            
            # update everything in body
            {class_var}.update(**body)
            return make_response(jsonify({{"Message":"Sussefully updated","Result":{class_var}}}), 200)
        else:
            return make_response(jsonify({{'Message': 'Not Found'}}), 200)
    
    # create new {class_var}
    @jwt_required()
    def put(slef):
        claims = get_jwt()['perms']
        if not(("create{perm_var}" in claims) or "administrator" in claims):
            return make_response(jsonify({{"Message":"Not Allowed"}}), 406)                 
        body = request.get_json()
        {class_var} = {ClassName}(**body)
        {class_var}.save()
        return make_response(jsonify({{'Created{ClassName}ID':str({class_var}.id)}}), 200)

    # delete {class_var} by id
    @jwt_required()
    def delete(slef):
        claims = get_jwt()['perms']
        if not(("delete{perm_var}" in claims) or "administrator" in claims):
            return make_response(jsonify({{"Message":"Not Allowed"}}), 406)         
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

    apiFile = open("output/resources/"+_class_var+".py", "w")
    apiFile.write(api_text.format(ClassName=class_name,class_var=_class_var,perm_var=perm_var))
    apiFile.close()

    route_text="""#{className}
from .{class_var} import {className}Api

def initialize_routes(api):
 api.add_resource({className}Api, '/{class_var}')
"""
    
    #create route file
    routeFile=open("output/routes/"+_class_var+".py","w")
    routeFile.write(route_text.format(className=class_name,class_var=_class_var))
    routeFile.close()

    print("Class file successfully created -> path: output/database/"+class_name+".py")
    print("Api file successfully created -> path: output/resources/"+_class_var+".py")
    print("Route file successfully Edited -> path: output/routes/"+_class_var+".py")


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
