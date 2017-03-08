import os
import re
import win32file
import win32api
from string import ascii_uppercase

import win32com.client
from os import path

for drive in ascii_uppercase:
    if path.exists(path.join(drive, "File.ID")):
        print drive + ":\\"

# def fix_path(path):
#     oShell = win32com.client.Dispatch("Wscript.Shell")
#     print oShell.SpecialFolders("AllUsersStartup")
#
#     cheat_list = {"WINDIR": "WINDIR", "DESKTOP": "DESKTOP",
#                   "PROGRAMFILES": "PROGRAMFILES", "LOCALAPPDATA": "LOCALAPPDATA",
#                   "TMP": "TMP", "TEMP": "TEMP", "APPDATA": "APPDATA",
#                   "STARTUP": "STARTUP", "HOME": "HOMEPATH",
#                   "COMMONSTARTUP": "AllUsersStartup", "RemovableDrive": "RemovableDrive",
#                   "SYSTEM": "SYSTEM"
#                   }
#
#     pattern = re.compile(r'(%.*%)+')
#     finded = pattern.search(path)
#     if finded:
#         clear_name = finded.group(0)[1:len(finded.group(0))-1]
#         if clear_name in cheat_list:
#             if  clear_name in os.environ:
#                 path = path.replace(finded.group(0), os.environ[cheat_list[clear_name]])
#             elif clear_name == cheat_list["SYSTEM"]:
#                 path = path.replace(finded.group(0), os.environ['WINDIR']+'\\System32')
#             elif clear_name == "RemovableDrive":
#                 drives = win32api.GetLogicalDriveStrings()
#                 drives = drives.split('\000')[:-1]
#                 for driver in drives:
#                     if win32file.GetDriveType(driver) == win32file.DRIVE_REMOVABLE:
#                         path = path.replace(finded.group(0), driver)
#             else:
#                 path = path.replace(finded.group(0), oShell.SpecialFolders(cheat_list[clear_name]))
#
#     return path
#
# print fix_path("windows")