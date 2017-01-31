import os
from xml.dom import minidom, Node


def saveCondition(element):
    global list
    list = []
    # something = " ".join(allParents(element,list))
    element.parentNode.getAttribute('type')
    allParents(element)
    operation.append([list, element])

def allParents(node):
    global list
    parent = node.parentNode
    if parent.hasAttributes():
        attr = parent.getAttribute('type')
        list.append(attr)
        allParents(parent)
    else:
        return

list = []

def traverseTree(element):
    global counter
    counter += len(operation) + 1
    for child in element.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if not child.hasChildNodes():
                operand = child.parentNode.getAttribute('type')
                saveCondition(child)
            else:
                traverseTree(child)


def addToAll(part):
    global sentences
    for i in xrange(len(sentences)):
        sentences[i] += part.getAttribute(
            'component') + '-' + part.getAttribute(
            'property') + ' ' + part.getAttribute(
            'condition') + '=' + part.getAttribute('value') + " & "


def callme(lsitPart):
    global sentences
    for part in lsitPart:
        if isinstance(part, list):
            sentences *= len(part)
            callme(part)
        else:
            addToAll(part)


# for filename in os.listdir('rulezz'):
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
            elementChilds = element.childNodes

            for child in elementChilds:  # Operation
                if child.nodeType == Node.ELEMENT_NODE:

                    for child2 in child.childNodes:
                                if child2.nodeType == Node.ELEMENT_NODE:
                                    if not child2.hasChildNodes():
                                        saveCondition(child2)
                                    else:
                                        traverseTree(child2)

    print len(operation)
    # print operation

    for item in operation:
        print item

    # pseudocode
    # sentences = [""]
    # callme(operation)
    #
    # for sentence in sentences:
    #     print sentence
