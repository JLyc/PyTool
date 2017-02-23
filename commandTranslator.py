import winreg

from distutils.core import setup
# import py2exe

# type = "RegSetValue"
# type = "WriteFile"
# inputString = "'property' : 'Key' ,'component' : 'RegistryItem' ,'value' : 'StubPath' ,'condition' : 'ends' | 'property' : 'Key' ,'component' : 'RegistryItem' ,'value' : 'SOFTWARE\\Microsoft\\Active Setup\\Installed Components' ,'condition' : 'contains' |"
# inputString = "'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':' ,'condition' : 'contains' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':Zone.Identifier' ,'condition' : 'notcontains' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':$ATTRIBUTE_LIST' ,'condition' : 'notcontains' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':favicon' ,'condition' : 'notcontains' |"
# inputString = "'property' : 'Extension' ,'component' : 'FileItem' ,'value' : 'lnk' ,'condition' : 'is' | 'property' : 'Path' ,'component' : 'FileItem' ,'value' : '%DESKTOP%' ,'condition' : 'starts' |"
# inputString = "'property' : 'Path' ,'component' : 'FileItem' ,'value' : '%TMP%' ,'condition' : 'starts' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : 'vbs' ,'condition' : 'is' |"

# inputParent = "'property' : 'Popularity' ,'component' : 'LiveGrid' ,'value' : '10000' ,'condition' : 'less' | 'property' : 'Name' ,'component' : 'FileItem' ,'value' : 'cscript' ,'condition' : 'is' | 'property' : 'Path' ,'component' : 'FileItem' ,'value' : '%WINDIR%' ,'condition' : 'isnot'"

# remove
executable_name = "test.py"

def generate_executable(type, input_string, input_parent):
    global executable_name
    commandParts = input_string.split("|")
    parentParts = input_parent.split("|")
    type_dic = eval('{' + type + '}')


    parentKey = []
    for command in parentParts:
        if command:
            parentKey.append(eval('{' + command + '}'))

    # registryItem
    registryKey = []
    writeFileKey = []
    for command in commandParts:
        if "RegSetValue" == type_dic['type'] and len(command) > 0:
            registryKey.append(eval('{' + command + '}'))
        elif "WriteFile" == type_dic['type'] and len(command) > 0:
            writeFileKey.append(eval('{' + command + '}'))
        elif "RenameFile" == type_dic['type'] and len(command) > 0:
            writeFileKey.append(eval('{' + command + '}'))
        elif "DeleteFile" == type_dic['type'] and len(command) > 0:
            writeFileKey.append(eval('{' + command + '}'))
        else:
            print "found different item " + command

    if parentKey:
        parent(parentKey)
    if registryKey:
        reg_set_value(registryKey, type_dic['type'])
    if writeFileKey:
        write_file_key(writeFileKey, type_dic['type'])


def parent(parentKey):
    global executable_name
    parent_path = []
    parent_file_name = []
    parent_extension = []
    parent_command_line = []

    for property in parentKey:
        if property["property"].lower() == 'path':
            parent_path = decode_property(property, parent_path)
        elif property["property"].lower() == 'name':
            parent_file_name = decode_property(property, parent_file_name)
        elif property["property"].lower() == 'extension':
            parent_extension = decode_property(property, parent_extension)
        elif property["property"].lower() == 'commandline':
            parent_command_line = decode_property(property, parent_command_line)
        elif property["property"].lower() == 'signed':
            parent_signed = decode_property(property, parent_signed)
        elif property["property"].lower() == 'popularity':
            if property["condition"].lower() == 'greater':
                print "ignor popularity"
                #skipp
    executable_name = "".join(parent_file_name) + '.py'


def reg_set_value(registryKey, type):
    path = []
    for property in registryKey:
        if property:
            decode_property(property, path)
    key_path = "\\".join(path)
    reg_modification(key_path)


def write_file_key(writeFileKey, type):
    path = ["c:\\\\work"]
    file_name = ["test"]
    extension = ["txt"]

    for property in writeFileKey:
        if not property:
            continue
        if property["property"].lower() == 'path':
            path = decode_property(property, path)
        elif property["property"].lower() == 'name':
            file_name = decode_property(property, file_name)
        elif property["property"].lower() == 'extension':
            extension = decode_property(property, extension)

    file_path = "".join(path)
    file_name = "".join(file_name) + "." + "".join(extension)
    print file_path

    if type == "WriteFile":
        write_file(file_path, file_name)
    elif type == "DeleteFile":
        delete_file(file_path, file_name)
    elif type == "RenameFile":
        rename_file(file_path, file_name)


def decode_property(property, out):
    if property["condition"].lower() == 'ends':
        out.append(property["value"])
    elif property["condition"].lower() == 'contains':
        out.insert(len(out) - 1, property["value"])
    elif property["condition"].lower() == 'notcontains':
        # irelevant ignored
        pass
    elif property["condition"].lower() == 'isnot':
        # irelevant ignored
        pass
    elif property["condition"].lower() == 'start':
        out.insert(0, property["value"])
    elif property["condition"].lower() == 'is':
        out = property["value"]
    else:
        print property["condition"].lower()
    return out


def rename_file(file_path, file_name):
    target = open("MyTest.py", 'w')
    target.write("Test")
    write_to_file("""
import os
os.rename("MyTest.py", os.path.join('{0}', '{1}'))
""".format(file_path, file_name))


def write_file(file_path, file_name):
    write_to_file("""
import os
file = open(os.path.join('{0}', '{1}'), 'a')
file.write(\" \")
""".format(file_path, file_name))


def delete_file(file_path, file_name):
    write_to_file("""
import shutil
import os
shutil.rmtree(os.path.join('{0}', '{1}'), True)
""".format(file_path, file_name))


def reg_modification(key_path):
    global executable_name
    print executable_name
    write_to_file("""
from winreg import *
Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
RawKey = CreateKey(Registry, "{0}")
""".format(key_path))


def write_to_file(code):
    file = open(executable_name, 'w')
    file.write(code)

# setup(console=[executable_name])


