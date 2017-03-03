import os
import re
import sys
from cx_Freeze import setup, Executable


executable_name = {'file_name': 'test.py'}
log_file = open("c:\\\\test\\skipped.txt", 'a')

def generate_executable(type, input_string, input_parent):
    global executable_name
    global log_file
    # log_file = open("c:\\test", 'w')
    # log_file.write("skipped: ")

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
    elif writeFileKey:
        write_file_key(writeFileKey, type_dic['type'])
    else:
        return
    return executable_name


def parent(parentKey):
    global executable_name
    global log_file
    log_file.write("skipped: ")
    parent = {'path': [], 'file_name': [], 'extension': [], 'command_line': []}
    # parent_path = []
    # parent_file_name = []
    # parent_extension = []
    # parent_command_line = []

    for property in parentKey:
        if property["property"].lower() == 'path':
            parent['path'] = decode_property(property, parent['path'])
        elif property["property"].lower() == 'name':
            parent['file_name'] = decode_property(property, parent['file_name'])
        elif property["property"].lower() == 'extension':
            parent['extension'] = decode_property(property, parent['extension'])
        elif property["property"].lower() == 'commandline':
            parent['command_line'] = decode_property(property, parent['command_line'])
        elif property["property"].lower() == 'signed':
            parent_signed = decode_property(property, parent_signed)
        elif property["property"].lower() == 'popularity':
            log_file.write("popularity " + property["condition"].lower() + "\n")
            if property["condition"].lower() == 'greater':
                print "ignor popularity\n\n\n\n\n\n\n"
                log_file.write("popularity: "+parent['file_name']+"\n")
                # return
                #skipp
            else:
                log_file.write("ignored2: " + parent['file_name'] + "\n")

    executable_name = {'path': "".join(parent['path']),
                       'file_name': "".join(parent['file_name']),
                       'extension': "".join(parent['extension']),
                       'command_line': "".join(parent['command_line'])}


def reg_set_value(registryKey, type):
    path = []
    for property in registryKey:
        if property:
            path = decode_property(property, path)
    if isinstance(path, list):
        path = "\\".join(path)
    count = path.count('\\')-1
    path = re.sub('\\\\$', '', path)
    reg_modification(path)


def write_file_key(writeFileKey, type):
    path = []
    file_name = []
    extension = []

    for property in writeFileKey:
        if not property:
            continue
        if property["property"].lower() == 'path':
            path = decode_property(property, path)
        elif property["property"].lower() == 'name':
            file_name = decode_property(property, file_name)
        elif property["property"].lower() == 'extension':
            extension = decode_property(property, extension)
        elif property["property"].lower() == 'fullpath':
            full_path = property["value"].rsplit('\\', 1)
            file_name = full_path[1]
            path = full_path[0]
        else:
            print "****************************************** unknow ************ " + property["property"]

    if not path:
        path = ["c:\\\\work"]
    if not file_name:
        file_name = ["test"]
    if not extension:
        extension = ["txt"]


    file_path = "".join(path)
    file_path = file_path.replace("\\","\\\\")
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
    elif property["condition"].lower() == 'notcontains':
        # irelevant ignored
        pass
    elif property["condition"].lower() == 'isnot':
        # irelevant ignored
        pass
    elif property["condition"].lower() == 'starts':
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
print os.path.join('{0}', '{1}')
file.write(\" \")
file.close()
""".format(file_path, file_name))


def delete_file(file_path, file_name):
    write_to_file("""
import shutil
import os
shutil.rmtree(os.path.join("{0}", "{1}"), True)
""".format(file_path, file_name))


def reg_modification(key_path):
    write_to_file("""
from winreg import *
Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
RawKey = CreateKey(Registry, "{0}")
""".format(key_path))


def write_to_file(code):
    print ".".join([executable_name['file_name'], 'py'])
    file = open(".".join([executable_name['file_name'], 'py']), 'w')
    file.write(code)
    file.close()

