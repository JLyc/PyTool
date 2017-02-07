import os
import re
from xml.dom import minidom, Node
from xml.dom.minicompat import NodeList


def childElements(node):
    nodeList = NodeList()
    for element in node.childNodes:
        if element.nodeType == Node.ELEMENT_NODE:
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
                else:
                    while hasChildElements(element):
                        # print item.getAttribute('type')
                        construcRule(item, element, _tmp_sentence)
                        if not hasChildElements(item):
                            break
                    wasInEnd = False
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


# foldr = 'test'
foldr = 'rulezz'
for filename in os.listdir(foldr):
    print "\n******************************************************************"
    # doc = minidom.parse('a0100_active_setup_autostart_registry.xml')
    # doc = minidom.parse('a0101_appinit_registry_entry_create.xml')
    print filename
    doc = minidom.parse(foldr + "/" + filename)

    root = doc.getElementsByTagName('rule')
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
    counter = 0;
    mapvalue = {}

    for element in parentProcess:  # OperationsParentProcess
        if element.hasChildNodes():
            for child1 in childElements(element):  # Operation
                sentence = []
                while (hasChildElements(child1)):
                    construcRule(child1, element, sentence)
            if findEndElements(child1):
                operation.append(saveData(child1))
    processOperation = operation

    operation = []
    for element in process:  # Operations
        if element.hasChildNodes():
            for child1 in childElements(element):  # Operation
                sentence = []
                while (hasChildElements(child1)):
                    construcRule(child1, element, sentence)
            if findEndElements(child1):
                operation.append(saveData(child1))
    parentProcessOperation = operation

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



    # print operationType
    try:
        oType = eval('{'+operationType+'}')
        if oType['type'] in ['WriteFile', 'DeleteFile', 'RegSetValue', 'TcpIpConnect']:
            print '###### SUCCESS ######'
            continue
    except:
        pass
    print formateStringForDict(parentProcessOperation)
    print formateStringForDict(processOperation)

    for command in operation:
        print formateStringForDict(command)