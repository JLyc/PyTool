import os
from xml.dom import minidom, Node
from xml.dom.minicompat import NodeList


def saveCondition(operand, element, counter):
    if operand.upper() == 'AND':
        operation.append(element)
    else:
        try:
            operation[mapvalue[str(counter)]].append(element)
        except KeyError:
            operation.append([element])
            mapvalue[str(counter)] = len(operation) - 1


def traverseTree(element):
    global counter
    counter += len(operation) + 1
    for child in element.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            if not child.hasChildNodes():
                operand = child.parentNode.getAttribute('type')
                saveCondition(operand, child, counter)
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
    for idx, part in enumerate(lsitPart):
        if isinstance(part, list):
            callme(part)
        else:
            lsitPart[idx] = part.getAttribute('value')
    return lsitPart


def childElements(node):
    nodeList = NodeList()
    for element in node.childNodes:
        if element.nodeType == Node.ELEMENT_NODE:
            nodeList.append(element)
    return nodeList


# for filename in os.listdir('rulezz'):
def pickFrom(child1):
    element = []
    if child1.getAttribute('type') == 'OR':
        elements = childElements(child1)
        element.append(elements)
        return element
    elif child1.getAttribute('type') == 'AND':
        elements = childElements(child1)
        for e in elements:
            element.append(e)
        return element
    else:
        return element


def levelTraversing(operation):
    noEmpty = 0
    for idx, item in enumerate(operation):
        if isinstance(item, Node) and item.nodeType == Node.ELEMENT_NODE:
            if item.hasChildNodes():
                operation[idx] = pickFrom(item)
                noEmpty += 1
            else:
                continue
        elif isinstance(item, list):
            levelTraversing(item)
            noEmpty += 1
    return noEmpty


def levelSerach(operation):
    noEmpty = 1
    while noEmpty > 0:
        noEmpty = levelTraversing(operation)
    print 'one while'


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
                for child1 in childElements(child):  # operator
                    if child1.getAttribute('type') == 'OR':
                        elements = childElements(child1)
                        count = len(elements)
                        operation.append(elements)
                        levelSerach(operation)

                    elif child1.getAttribute('type') == 'AND':
                        elements = childElements(child1)
                        count = len(elements)
                        for e in elements:
                            operation.append(e)
                        levelSerach(operation)

                    else:
                        continue

                        # for child2 in child.childNodes:
                        #     if child2.nodeType == Node.ELEMENT_NODE:
                        #         if not child2.hasChildNodes():
                        #             operand = child2.parentNode.getAttribute('type')
                        #             saveCondition(operand, child2, counter)
                        #         else:
                        #             traverseTree(child2)

    print len(operation)
    print operation

    # pseudocode
    sentences = [""]
    print callme(operation)

    # for sentence in sentences:
    #     print sentence
