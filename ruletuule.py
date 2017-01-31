import os
from xml.dom import minidom, Node
from xml.dom.minicompat import NodeList


def childElements(node):
    nodeList = NodeList()
    for element in node.childNodes:
        if element.nodeType == Node.ELEMENT_NODE:
            nodeList.append(element)
    return nodeList


def notInSentence(list):
    for sentence1 in operation:
        for item in sentence1:
            if not item in list:
                return True

def construcRule(element, sentence):
    for child1 in childElements(element):  # operator A?
        if not child1.hasChildNodes():
            if child1.parentNode.getAttribute('type') == 'AND':
                sentence.append(child1)
                print sentence
                if notInSentence(sentence):
                    operation.append(sentence)
                    continue
            elif child1.parentNode.getAttribute('type') == 'OR':
                operation.append(sentence.append(child1))
            else:
                print "FATAL ERROR"
        else:
            construcRule(child1, sentence)


for filename in os.listdir('test'):
    print "\n******************************************************************"
    # doc = minidom.parse('a0100_active_setup_autostart_registry.xml')
    # doc = minidom.parse('a0101_appinit_registry_entry_create.xml')
    print filename
    # doc = minidom.parse("rulezz/"+filename)
    doc = minidom.parse("test/" + filename)

    root = doc.getElementsByTagName('rule')
    operations = doc.getElementsByTagName('Operations')
    operation = doc.getElementsByTagName('Operation')

    operation = []
    counter = 0;
    mapvalue = {}

    for element in operations:  # Operations
        if element.hasChildNodes():
            for child in childElements(element):  # Operation
                sentence = []
                construcRule(child, sentence)


    print len(operation)
    print operation



sentence find and find end-elem concat
         find list element
































