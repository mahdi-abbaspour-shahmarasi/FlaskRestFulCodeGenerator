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
print('3. Generate View Codes Step By Step')
print('4. Help')
print('5. About')
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
    def getType(field):
        _type = ""
        if field != "text" or field != "email" or field != "password":
            _type = "text"
        return _type

    print('==== Generate Code Step By Step ====\n')

    module_name = input("Please enter module name: ")

    module_name_fa = input("Please enter module name (Farsi): ")
    print("module name is:", module_name+"\t"+module_name_fa)

    print("Please complete module details.")

    module_var = module_name.lower()
    moduleVar = module_name.capitalize()


    module_fields_label = []
    module_fields_name = []
    module_fields_type = []
    module_fields_req = []

    while True:
        _label = input("Enter field label (Farsi): ")
        if not _label:
            print("done.")
            break

        _name = input("Enter field name: ")
        _type = input("Enter input type: (text, password, email,...)")
        _isRequired = input("The field is required? (True/False): ")

        module_fields_label.append(_label)
        module_fields_name.append(_name)
        module_fields_type.append(getType(_type))

        # default value is True
        _isRequired = _isRequired.capitalize()
        if _isRequired != "True" and _isRequired != "False":
            _isRequired = "True"
        module_fields_req.append(_isRequired)

        print("\n"+module_name+" module info:")
        for _l, _n, _t, _r in zip(module_fields_label, module_fields_name, module_fields_type, module_fields_req):
            print("field label: "+_l+"field name: "+_n+"\t field type: " +
                  _t+"\t field requirement: "+_r)

    print("Creating module file ...")
    print("=========================")

    # check to exist output directory
    if not isdir("output"):
        os.mkdir("output")
        os.mkdir("output/views")
        os.mkdir("output/views/"+module_var)

    if not isdir("output/views"):
        os.mkdir("output/views")
        
    if not isdir("output/views/"+module_var):
        os.mkdir("output/views/"+module_var)


    # View
    module_text_top = """<script src="/assets/js/tables.js"></script>

<div class="row">
    <div class="col-sm-12">
        <div class="panel">
            <div class="panel-body">
                <div class="row">
                    <div class="col-sm-6">
                        <div class="m-b-30">
                            <a href="#!/content/{module_var}/create" id="addToTable"
                                class="btn btn-primary waves-effect waves-light">افزودن <i class="fa fa-plus"></i></a>
                        </div>
                    </div>
                </div>

                <div class="editable-responsive" ng-controller="{module_var}Table">
                    <table class="table table-striped" id="datatable-editable-perms">
                        <div class="table-setting row">
                            <div class="search-box row col-md-3">
                                جستجو: <input type="text" class="form-control" placeholder="جستجو" ng-model="search" />
                                <div class="sorting-btn col-md-3">
                                    <a ng-click="sortBy('title')" class="btn waves-effect waves-light"><i
                                            class="fa fa-sort" aria-hidden="true"></i>
                                    </a>
                                </div>
                            </div>

                            <div class="pagination-per-page col-md-3">
                                نمایش
                                <select class="form-select" aria-label="Default select example" ng-model="rowPerPage">
                                    <option selected value="3">3</option>
                                    <option value="5">5</option>
                                    <option value="10">10</option>
                                    <option value="50">50</option>
                                </select>
                                سطر
                            </div>
                        </div>


                        <thead>
                            <tr>
"""
    module_text = """
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="gradeX"
                                dir-paginate="row in result | itemsPerPage: rowPerPage | filter: search | orderBy:propertyName:reverse">
    """

    module_text_end = """
                                        <td class="actions" id={{c=getID(row._id)}}>
                                    <a href="#!/content/{module_var}/update/{{c}}" class="on-default edit-row"
                                        style="color: #10c469; margin-left: 10px"><i class="fa fa-pencil"></i></a>
                                    <a href="" class="on-default remove-row" style="color: #ff5b5b"
                                        ng-click=deleteItem(c)><i class="fa fa-trash-o"></i></a>
                                </td>
                            </tr>
                        </tbody>
                    </table>

                    {{{{message}}}}
                    <dir-pagination-controls max-size=rowPerPage direction-links="true" boundary-links="true">
                    </dir-pagination-controls>
                </div>
            </div>
            <!-- end: panel body -->

        </div> <!-- end panel -->
    </div> <!-- end col-->
</div>
</div>
    """

    # create module file
    moduleFile = open("output/views/"+module_var+"/view.htm", "w")

    moduleFile.write(module_text_top.format(
        module_var=module_var))

    f_txt = """
    """
    t_txt = """
    """
    for _fieldLabel, _fieldName in zip(
            module_fields_label, module_fields_name):

        f_txt += "                               <th>"+_fieldLabel+"<th>\n"
        t_txt += "                               <td>{{row." + \
            _fieldName+"}}<td>\n"

    moduleFile.write(f_txt + module_text)
    moduleFile.write(t_txt)
    moduleFile.write(module_text_end.format(module_var=module_var))
    moduleFile.close()

    # Create
    module_text_top = """<div class="row" ng-controller="add{module_name}">
    <div class="col-md-12">
        <div class="card-box">
            <h4 class="header-title m-t-0 m-b-30">ثبت {module_name_fa} جدید</h4>
            <form action="#" data-parsley-validate novalidate>
"""
    module_text = """
                <div class="form-group">
                    <label for="{_fieldName}">{_fieldLabel}</label>
                    <input type="{_fieldType}" class="form-control" name="{_fieldName}" parsley-trigger="change" {_fieldRequirement} placeholder="{_fieldLabel}"
                        id="{_fieldName}" ng-model="{_fieldName}">
                </div>
    """

    module_text_end = """
               <div class="form-group text-right m-b-0">
                    <input class="btn btn-primary waves-effect waves-light" value="ثبت" ng-click="sendData()">

                    <a href="#!/content/{module_var}/list" class="btn btn-default waves-effect waves-light m-l-5">
                        لغو
                    </a>
                    <small class="col-lg-12 text-center" style="color: red; font-weight: bold">{{{{message}}}}</small>
                </div>

            </form>
        </div>
    </div><!-- end col -->
</div>
    """

    # create module file
    moduleFile = open("output/views/"+module_var+"/create.htm", "w")

    moduleFile.write(module_text_top.format(
        module_name=moduleVar, module_name_fa=module_name_fa))

    for _fieldLabel, _fieldName, _fieldType, _fieldRequirement in zip(
            module_fields_label, module_fields_name, module_fields_type, module_fields_req):

        if (_fieldRequirement):
            _fieldRequirement = "required"
        else:
            _fieldRequirement = ""

        moduleFile.write(module_text.format(
            _fieldType=_fieldType, _fieldName=_fieldName,
            _fieldLabel=_fieldLabel, _fieldRequirement=_fieldRequirement))

    moduleFile.write(module_text_end.format(module_var=module_var))
    moduleFile.close()

    # Update
    module_text_top = """<div class="row" ng-controller="update{module_name}">
    <div class="col-md-12">
        <div class="card-box">
            <h4 class="header-title m-t-0 m-b-30">ویرایش {module_name_fa}</h4>
            <form action="#" data-parsley-validate novalidate>
"""
    module_text = """
                <div class="form-group">
                    <label for="{_fieldName}">{_fieldLabel}</label>
                    <input type="{_fieldType}" class="form-control" name="{_fieldName}" {_fieldRequirement} placeholder="{_fieldLabel}"
                        id="{_fieldName}" ng-model="{_fieldName}">
                </div>
    """

    module_text_end = """
               <div class="form-group text-right m-b-0">
                    <input class="btn btn-primary waves-effect waves-light" value="ثبت" ng-click="sendData()">

                    <a href="#!/content/{module_var}/list" class="btn btn-default waves-effect waves-light m-l-5">
                        لغو
                    </a>
                    <small class="col-lg-12 text-center" style="color: red; font-weight: bold">{{{{message}}}}</small>
                </div>

            </form>
        </div>
    </div><!-- end col -->
</div>
    """

    # create module file
    moduleFile = open("output/views/"+module_var+"/update.htm", "w")

    moduleFile.write(module_text_top.format(
        module_name=moduleVar, module_name_fa=module_name_fa))

    for _fieldLabel, _fieldName, _fieldType, _fieldRequirement in zip(
            module_fields_label, module_fields_name, module_fields_type, module_fields_req):

        if (_fieldRequirement):
            _fieldRequirement = "required"
        else:
            _fieldRequirement = ""

        moduleFile.write(module_text.format(
            _fieldType=_fieldType, _fieldName=_fieldName,
            _fieldLabel=_fieldLabel, _fieldRequirement=_fieldRequirement))

    moduleFile.write(module_text_end.format(module_var=module_var))
    moduleFile.close()

    print("Module file successfully created -> path: output/views/"+module_var+"view.htm")
    print("Module file successfully created -> path: output/views/" +
          module_var+"create.htm")
    print("Module file successfully created -> path: output/views/" +
          module_var+"update.htm")


def item4():
    print("this is item 4")


def item5():
    print("this is item 5")


def item0():
    exit()


func_keys = {
    '0': item0,
    '1': item1,
    '2': item2,
    '3': item3,
    '4': item4,
    '5': item5,
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
