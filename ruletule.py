import os
from cx_Freeze import setup, Executable
from shutil import copy

import commandTranslator
from xml.dom import minidom, Node
from xml.dom.minicompat import NodeList


def childElements(node):
    nodeList = NodeList()
    for element in node.childNodes:
        if element.nodeType == Node.ELEMENT_NODE:
            if str(element.getAttribute('type')).lower() == 'and':
                nodeList.insert(0, element)
            else:
                nodeList.append(element)
    return nodeList


def hasChildElements(node):
    for element in node.childNodes:
        if element.nodeType == Node.ELEMENT_NODE:
            return True
    return False


def notInSentence(list):
    for sentence1 in operation:
        for item in sentence1:
            if not item in list:
                return True

def findEndElements(element):
    if str(element.localName).lower() == 'condition':
        return True
    else:
        return False

def saveData(element):
    outValue = ""
    for item in element.attributes.items():
        outValue += "\'" + item[0] + "\' : \'" + item[1] + "\' ,"
    return outValue


def construcRule(element, parent, sentence):
    _tmp_sentence = []
    _tmp_sentence.append(sentence)
    attribute = str(element.getAttribute('type')).lower()
    wasInEnd = True
    if attribute == 'and':
        for item in childElements(element):
            if findEndElements(item):
                # wasInEnd = True
                # _tmp_sentence.append(item)
                _tmp_sentence.append(saveData(item))
                element.removeChild(item)
        for item in childElements(element):
            if not findEndElements(item):
                while hasChildElements(element):
                    construcRule(item, element, _tmp_sentence)
                    # if not hasChildElements(item):
                    #     break
                wasInEnd = False
        parent.removeChild(element)
        # print "removed end way"
    elif attribute == 'or':#up
        if hasChildElements(element):
            for item in childElements(element):
                if findEndElements(item):
                    # _tmp_sentence.append(item)
                    _tmp_sentence.append(saveData(item))
                    element.removeChild(item)
                    break
                    # wasInEnd = False
                else:
                    while hasChildElements(element):
                        # print item.getAttribute('type')
                        construcRule(item, element, _tmp_sentence)
                        if not hasChildElements(item):
                            break
                    wasInEnd = False
                    break
        else:
            parent.removeChild(element)
            return
    else:
        if findEndElements(element):
            _tmp_sentence.append(saveData(element))
            parent.removeChild(element)
    if wasInEnd:
        operation.append(_tmp_sentence)

def formateStringForDict(command):
    temp = str(command).replace('[','')
    temp = temp.replace(']','')
    temp = temp.replace('u\"', '\"')
    temp = temp.replace(', \"', '')
    temp = temp.replace(',\"', '| ')
    temp = temp.replace('\"', '')
    return temp

count = 0
# foldr = 'test'
foldr = 'rulezz'
# print sys.argv
# foldr = 'compile'
# foldr = sys.argv[2]
for filename in os.listdir(foldr):
    print("\n*****************************************************************")
    print(filename)

    doc = minidom.parse(foldr + "/" + filename)

    operations = doc.getElementsByTagName('Operations')
    if len(operations) == 0:
        operations = doc.getElementsByTagName('operations')
    process = doc.getElementsByTagName('Process')
    if len(process) == 0:
        process = doc.getElementsByTagName('process')
    parentProcess = doc.getElementsByTagName('ParentProcess')
    if len(parentProcess) == 0:
        parentProcess = doc.getElementsByTagName('parentProcess')

    operation = []
    for element in parentProcess:  # OperationsParentProcess
        if element.hasChildNodes():
            for child1 in childElements(element):  # Operation
                sentence = []
                while hasChildElements(child1):
                    construcRule(child1, element, sentence)
            if findEndElements(child1):
                operation.append(saveData(child1))
    parentProcessOperation = operation

    operation = []
    for element in process:  # Process
        if element.hasChildNodes():
            for child1 in childElements(element):  # Operation
                sentence = []
                while hasChildElements(child1):
                    construcRule(child1, element, sentence)
            if findEndElements(child1):
                operation.append(saveData(child1))
    processOperation = operation

    operation = []
    operationType = ""
    for element in operations:  # Operations
        if element.hasChildNodes():
            for child in childElements(element):  # Operation
                operationType = saveData(child)
                for child1 in childElements(child):
                    sentence = []
                    while (hasChildElements(child)):
                        construcRule(child1, child, sentence)



    print(formateStringForDict(operationType))

    print("parent"+formateStringForDict(parentProcessOperation))

    parentCommand = formateStringForDict(parentProcessOperation)
    print("process"+formateStringForDict(processOperation))
    processCommand = formateStringForDict(processOperation)

    if not operation:
        log_file = open("c:/test/skipped.txt", 'a')
        log_file.write("skipped: " + filename + "\n")

    for command in operation:
        print(formateStringForDict(command))
        command = formateStringForDict(command)
        if not parentCommand:
            count += 1
            parent_name = "'property' : 'Name' ,'component' : 'FileItem' ,'value' : '{0}' ,'condition' : 'is'".format(filename[:-4])
        else:
            parent_name = parentCommand
        executable_name = commandTranslator.generate_executable(operationType, command, parent_name)

        if not executable_name:
            continue

        build_exe_options = {"packages": ["os"], "excludes": ["tkinter"],
                             "build_exe": "c:\\test\\" + executable_name['file_name']+ str(count), "silent": True}
        setup(name="ESET", version="0.1", description="ESET testing tool",
              options={"build_exe": build_exe_options},
              executables=[Executable(executable_name['file_name']+'.py')])


        file = open(".".join(["c:\\test\\" + executable_name['file_name'] + str(count)+ "\\help", 'txt']), 'w')
        file.write(str(executable_name))
        file.close()

        copy(foldr + "/" + filename,
                 "c:\\test\\" + executable_name['file_name'] + str(count))
        copy(executable_name['file_name']+'.py',
             "c:\\test\\" + executable_name['file_name'] + str(count))