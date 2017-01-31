import winreg
# from distutils.core import setup
# import py2exe

inputString = "'property' : 'Key' ,'component' : 'RegistryItem' ,'value' : 'StubPath' ,'condition' : 'ends' | 'property' : 'Key' ,'component' : 'RegistryItem' ,'value' : 'SOFTWARE\\Microsoft\\Active Setup\\Installed Components' ,'condition' : 'contains' |"
# inputString = "'property' : 'Path' ,'component' : 'FileItem' ,'value' : '%TMP%' ,'condition' : 'starts' | 'property' : 'Extension' ,'component' : 'FileItem' ,'value' : 'vbs' ,'condition' : 'is' |"

#remove
commandParts = inputString.split("|")

#registryItem
registryKey = []
for command in commandParts:
    if "'property' : 'Key'" in command:
        registryKey.append(eval('{'+command+'}'))
    elif "'property' : 'Path'" in command:
        registryKey.append(eval('{'+command+'}'))
    else:
        print "found different item " + command

sentence = []
for property in registryKey:
    if property["condition"].lower() == 'ends':
        sentence.append(property["value"])
    elif property["condition"].lower() == 'contains':
        sentence.insert(len(sentence)-1, property["value"])
    elif property["condition"].lower() == 'start':
        sentence.insert(0, property["value"])
    else:
        print property["condition"].lower()

file = open("testName.py", 'w')
file.write("""from winreg import *\n
Registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
RawKey = CreateKey(Registry, "SOFTWARE\Microsoft\Active Setup\Installed Components\StubPath")
""")

# setup(console=['testName.py'])


