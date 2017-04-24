import os
import re

import win32file
import win32api

import errno
import win32com.client

executable_name = {'file_name': 'test.py'}
try:
    os.makedirs(os.path.dirname("c:/test/skipped.txt"))
except OSError as e:
    if e.errno != errno.EEXIST:
        pass

log_file = open("c:/test/skipped.txt", 'a')


def generate_executable(type, input_string, input_parent):
    global executable_name
    global log_file

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
            print("found different item " + command)

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
    parent = {'path': [], 'file_name': [], 'extension': [], 'command_line': []}

    for property in parentKey:
        if property["property"].lower() == 'path':
            parent['path'] = decode_property(property, parent['path'])
        elif property["property"].lower() == 'name':
            parent['file_name'] = decode_property(property, parent['file_name'])
        elif property["property"].lower() == 'extension':
            parent['extension'] = decode_property(property, parent['extension'])
        elif property["property"].lower() == 'commandline':
            parent['command_line'] = decode_property(property,
                                                     parent['command_line'])
        elif property["property"].lower() == 'signed':
            parent_signed = decode_property(property, parent_signed)
        elif property["property"].lower() == 'popularity':
            log_file.write("popularity " + property["condition"].lower() + "\n")
            if property["condition"].lower() == 'greater':
                print("ignor popularity\n\n\n\n\n\n\n")
                log_file.write("popularity: " + parent['file_name'] + "\n")
                # return
                # skipp
            else:
                log_file.write("ignored2: " + parent['file_name'] + "\n")

    for property in {'path', 'file_name', 'extension', 'command_line'}:
        executable_name[property] = ''.join(
            ["".join(item) for item in return_sentence(parent[property])])


def return_sentence(path):
    out = list()
    path_part = list()
    if not path:
        return []

    for contain in path["contains"]:
        path_part.append(contain)

    sub_path = list()
    for i in max([path["starts"], path["ends"]]):
        sub_path = [contain for contain in path_part]
        if i in path["starts"]:
            sub_path.insert(0, i)
        else:
            sub_path.append(i)
        for j in min([path["starts"], path["ends"]]):
            if j in path["starts"]:
                sub_path.insert(0, j)
            else:
                sub_path.append(j)
            out.append(sub_path)
        if len(min([path["starts"], path["ends"]])) == 0:
            out.append(sub_path)
        sub_path = list()
    return out if out else path_part


def sort_registry_path(path):
    paths = return_sentence(path)
    for path in paths:
        if isinstance(path, list):
            path = "\\".join(path)
        path = re.sub('\\\\$', '', path)
        # path = re.escape(path)

        if "HKLM" in path:
            path = path.replace("HKLM\\", "")
            location = "HKEY_LOCAL_MACHINE"
        elif "HKCU" in path:
            path = path.replace("HKCU\\", "")
            location = "HKEY_CURRENT_USER"
        else:
            location = "HKEY_CURRENT_USER"
            path = re.sub("^\\\\", '', path)
            # log_file.write("other: " + path + "\n")
        reg_modification(location, path)


def reg_set_value(registryKey, type):
    path = {"starts": [], "contains": [], "ends": []}
    for property in registryKey:
        if property:
            path = decode_property(property, path)
    sort_registry_path(path)


def write_file_key(writeFileKey, type):
    path = {"starts": [], "contains": [], "ends": []}
    file_name = {"starts": [], "contains": [], "ends": []}
    extension = {"starts": [], "contains": [], "ends": []}

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
            file_name = {"starts": [], "contains": [full_path[1]], "ends": []}
            path = {"starts": [], "contains": [full_path[0]], "ends": []}
        else:
            print(
                "****************************************** unknow ************ " +
                property["property"])

    path = return_sentence(path)
    if not path:
        path = ["c:\work"]
    file_name = return_sentence(file_name)
    if not file_name:
        file_name = ["test"]
    extension = return_sentence(extension)
    if not extension:
        extension = ["txt"]

    file_path = "".join(["".join(item) for item in path])
    file_path = file_path.replace("\\", "\\\\")
    file_path = fix_path(file_path)
    if not re.search(r'^[a-xA-X]:', file_path):
        if re.match(r'^\\', file_path):
            file_path = "c:" + file_path
        else:
            file_path = "c:\\" + file_path
    file_name = "".join(["".join(item) for item in file_name]) + "." + "".join(
        ["".join(item) for item in extension])
    print(file_path)

    if type == "WriteFile":
        write_file(file_path, file_name)
    elif type == "DeleteFile":
        delete_file(file_path, file_name)
    elif type == "RenameFile":
        rename_file(file_path, file_name)


def decode_property(property, out):
    if property["condition"].lower() == 'ends':
        out["ends"].append(property["value"])
    elif property["condition"].lower() == 'contains':
        out["contains"].append(property["value"])
    elif property["condition"].lower() == 'notcontains':
        # irelevant ignored
        pass
    elif property["condition"].lower() == 'isnot':
        # irelevant ignored
        pass
    elif property["condition"].lower() == 'starts':
        out["starts"].insert(0, property["value"])
    elif property["condition"].lower() == 'is':
        out = {"starts": [property["value"]], "contains": [], "ends": []}
    else:
        print(property["condition"].lower())
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
import errno
try:
    os.makedirs(os.path.dirname(os.path.join('{0}', '{1}')))
except OSError as e:
    if e.errno != errno.EEXIST:
        pass
file = open(os.path.join('{0}', '{1}'), 'a')
print(os.path.join('{0}', '{1}'))
file.write(\" \")
file.close()
""".format(file_path, file_name))


def delete_file(file_path, file_name):
    write_to_file("""
import shutil
import os
shutil.rmtree(os.path.join("{0}", "{1}"), True)
""".format(file_path, file_name))


def reg_modification(location, key_path):
    write_to_file("""
from _winreg import *
Registry = ConnectRegistry(None, {0})
RawKey = CreateKey(Registry, "{1}")
SetValueEx(RawKey, 'evalue', 0, REG_SZ, "Catch_me")
RawKey.Close()
""".format(location, key_path))


def write_to_file(code):
    print(
    ".".join([executable_name['file_name'], 'py']))
    file = open(".".join([executable_name['file_name'], 'py']), 'a')
    file.write(code)
    file.close()


def fix_path(path):
    oShell = win32com.client.Dispatch("Wscript.Shell")
    print oShell.SpecialFolders("AllUsersStartup")

    cheat_list = {"WINDIR": "WINDIR", "DESKTOP": "DESKTOP",
                  "PROGRAMFILES": "PROGRAMFILES",
                  "LOCALAPPDATA": "LOCALAPPDATA", "TMP": "TMP", "TEMP": "TEMP",
                  "APPDATA": "APPDATA", "STARTUP": "STARTUP",
                  "HOME": "HOMEPATH", "COMMONSTARTUP": "AllUsersStartup",
                  "RemovableDrive": "RemovableDrive", "SYSTEM": "SYSTEM"}

    pattern = re.compile(r'(%.*%)+')
    found = pattern.search(path)
    if found:
        clear_name = found.group(0)[1:len(found.group(0)) - 1]
        if clear_name in cheat_list:
            if clear_name in os.environ:
                path = path.replace(found.group(0),
                                    os.environ[cheat_list[clear_name]])
            elif clear_name == cheat_list["SYSTEM"]:
                path = path.replace(found.group(0),
                                    os.environ['WINDIR'] + '\\System32')
            elif clear_name == "RemovableDrive":
                drives = win32api.GetLogicalDriveStrings()
                drives = drives.split('\000')[:-1]
                for driver in drives:
                    if win32file.GetDriveType(
                            driver) == win32file.DRIVE_REMOVABLE:
                        path = path.replace(found.group(0), driver)
            else:
                path = path.replace(found.group(0), oShell.SpecialFolders(
                    cheat_list[clear_name]))

    return path
