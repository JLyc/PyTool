import winreg

# from distutils.core import setup
# import py2exe

# type = "RegSetValue"
type = "WriteFile"
# inputString = "'property' : 'Key' ,'component' : 'RegistryItem' ,'value' : 'StubPath' ,'condition' : 'ends' | 'property' : 'Key' ,'component' : 'RegistryItem' ,'value' : 'SOFTWARE\\Microsoft\\Active Setup\\Installed Components' ,'condition' : 'contains' |"
# inputString = "'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':' ,'condition' : 'contains' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':Zone.Identifier' ,'condition' : 'notcontains' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':$ATTRIBUTE_LIST' ,'condition' : 'notcontains' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : ':favicon' ,'condition' : 'notcontains' |"
inputString = "'property' : 'Extension' ,'component' : 'FileItem' ,'value' : 'lnk' ,'condition' : 'is' | 'property' : 'Path' ,'component' : 'FileItem' ,'value' : '%DESKTOP%' ,'condition' : 'starts' |"
# inputString = "'property' : 'Path' ,'component' : 'FileItem' ,'value' : '%TMP%' ,'condition' : 'starts' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : 'vbs' ,'condition' : 'is' |"

# remove
executable_name = "test.py"
commandParts = inputString.split("|")

# registryItem
registryKey = []
writeFileKey = []
for command in commandParts:
    if "RegSetValue" == type and len(command) > 0:
        registryKey.append(eval('{' + command + '}'))
    elif "WriteFile" == type and len(command) > 0:
        writeFileKey.append(eval('{' + command + '}'))
    elif "RenameFile" == type and len(command) > 0:
        writeFileKey.append(eval('{' + command + '}'))
    elif "DeleteFile" == type and len(command) > 0:
        writeFileKey.append(eval('{' + command + '}'))
    else:
        print "found different item " + command




def reg_set_value(registryKey, type):
    path = []
    for property in registryKey:
        if property["condition"].lower() == 'ends':
            path.append(property["value"])
        elif property["condition"].lower() == 'contains':
            path.insert(len(path) - 1, property["value"])
        elif property["condition"].lower() == 'start':
            path.insert(0, property["value"])
        elif property["condition"].lower() == 'is':
            path = property["value"]
        else:
            print property["condition"].lower()

    key_path = "".join(path)
    reg_modification(key_path)



def write_file_key(writeFileKey, type):
    path = ["c:\\\\work"]
    file_name = ["test"]
    extension = ["txt"]

    for property in writeFileKey:
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

    file = open(executable_name, 'w')
    code = """
import os
os.rename("MyTest.py", os.path.join('{0}', '{1}'))
""".format(file_path, file_name)

    file.write(code)


def write_file(file_path, file_name):
    file = open(executable_name, 'w')

    code = """
import os
file = open(os.path.join('{0}', '{1}'), 'a')
file.write(\" \")
""".format(file_path, file_name)

    file.write(code)


def delete_file(file_path, file_name):
    file = open(executable_name, 'w')

    code = """
import shutil
shutil.rmtree(os.path.join('{0}', '{1}'), True)
""".format(file_path, file_name)

    file.write(code)


def reg_modification(key_path):
    file = open(executable_name, 'w')
    code = """
from winreg import *
Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
RawKey = CreateKey(Registry, "{0}")
""".format(key_path)
    file.write(code)

if registryKey:
    reg_set_value(registryKey, type)
elif writeFileKey:
    write_file_key(writeFileKey, type)

# setup(console=['executable_name'])


