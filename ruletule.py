import os
import re
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



def andRule(element, parent, _tmp_sentence):
    wasInEnd = True
    for item in childElements(element):
        if findEndElements(item):
            _tmp_sentence.append(saveData(item))
            element.removeChild(item)
            if not hasChildElements(parent):
                operation.append(_tmp_sentence)
        else:
            while hasChildElements(element):
                construcRule(item, element, _tmp_sentence)
                # if hasChildElements(item):
                #     break
            wasInEnd = False
    parent.removeChild(element)
    return wasInEnd

def orRule(element, parent, _tmp_sentence):
    wasInEnd = True
    if hasChildElements(element):
        for item in childElements(element):
            if findEndElements(item):
                _tmp_sentence.append(saveData(item))
                element.removeChild(item)
                break
            else:
                while hasChildElements(element):
                    construcRule(item, element, _tmp_sentence)
                    if not hasChildElements(item):
                        break
                wasInEnd = False
    else:
        parent.removeChild(element)
        return wasInEnd
    return wasInEnd

def construcRule(element, parent, sentence):
    _tmp_sentence = [sentence]
    attribute = str(element.getAttribute('type')).lower()
    wasInEnd = True

    if attribute == 'and':
        # wasInEnd = andRule(element, parent, _tmp_sentence)
        for item in childElements(element):
            if findEndElements(item):
                _tmp_sentence.append(saveData(item))
                element.removeChild(item)
                if not hasChildElements(parent):
                    operation.append(_tmp_sentence)
            else:
                while hasChildElements(element):
                    construcRule(item, element, _tmp_sentence)
                    # if hasChildElements(item):
                    #     break
                wasInEnd = False
        parent.removeChild(element)
    elif attribute == 'or':
        # wasInEnd = orRule(element, parent, _tmp_sentence)
        if hasChildElements(element):
            for item in childElements(element):
                if findEndElements(item):
                    _tmp_sentence.append(saveData(item))
                    element.removeChild(item)
                    break
                else:
                    while hasChildElements(element):
                        construcRule(item, element, _tmp_sentence)
                        if not hasChildElements(item):
                            break
                    wasInEnd = False
        else:
            parent.removeChild(element)
            return wasInEnd
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


foldr = 'test'
# foldr = 'rulezz'
for filename in os.listdir(foldr):
    print "\n******************************************************************"
    print filename

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
    processOperation = operation

    operation = []
    for element in process:  # Operations
        if element.hasChildNodes():
            for child1 in childElements(element):  # Operation
                sentence = []
                while hasChildElements(child1):
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

    print operationType
    print formateStringForDict(parentProcessOperation)
    print formateStringForDict(processOperation)

    for command in operation:
        print formateStringForDict(command)