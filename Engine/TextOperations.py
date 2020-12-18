import re


class LinkedText:
    def __init__(self, text, links=[]):
        self.text = text
        self.links = links


def extractLinks(text):
    formattedText = LinkedText("")
    contador = 1
    correccion = 0

    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    links = re.findall(regexPattern, text)
    links = list(dict.fromkeys(links))
    formattedText.links = links

    matchIterator = re.finditer(regexPattern, text)

    linksDictionary = {}

    for match in matchIterator:
        contadorAux = contador
        try:
            matchCode = linksDictionary[match[0]]
            contadorAux = matchCode
        except:
            linksDictionary[match[0]] = contadorAux

        text = (
            text[: match.start() - correccion]
            + str(contadorAux)
            + text[match.end() - correccion :]
        )
        contador = contador + 1
        correccion = correccion + match.end() - match.start() - 1

    formattedText.text = text

    return formattedText


def extendEnumerationByX(operation, ammountOfNewSlots):
    existingSlots = getNumberOfLinksByOperation(operation)

    indexOfOpBeginning = operation.find("<1>")

    operationBeginning = (
        operation if indexOfOpBeginning == -1 else operation[:indexOfOpBeginning]
    )

    newSlots = existingSlots + ammountOfNewSlots

    return generateOperation(operationBeginning, newSlots)


def hasEnoughSlots(operation, nOfSlotsNeeded):
    hasEnoughSlots = True

    for contador in range(nOfSlotsNeeded):
        if operation.find("<" + str(contador + 1) + ">") == -1:
            hasEnoughSlots = False
            break

    return hasEnoughSlots


def generateOperation(operationBeginning, nOfSlots):
    operation = (
        operationBeginning
        if operationBeginning[-1] != " "
        else operationBeginning[:-1]
    )

    for contador in range(nOfSlots):
        if contador != 0:
            operation = operation + ","
        operation = operation + " <" + str(contador + 1) + ">"

    operation = operation + "."

    return operation


def getNumberOfLinksByOperation(operation):
    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    links = re.findall(regexPattern, operation)

    return int(links[-1])

def offsetSlots(operation, existingSlots):
    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    replacementFunction = lambda match: str(int(match[0])+existingSlots)

    newOperation = re.sub(regexPattern, replacementFunction, operation)

    return newOperation
        



##print (hasEnoughSlots("mi casa queda en <1> y <2>" ,3))
##print (generateOperation("Combatieron en la guerra", 3))
##print (getNumberOfLinksByOperation("<1> y <2> lucharon con <3>"))
##print (extendEnumerationByX("Combatieron en la guerra: <1>, <2>", 2))
##print(extendEnumerationByX("Aquí murió <1>.", 2))
##casa = extractLinks("<Amanda> vivió en el <Lago Brevis>, pero <Amanda> se sentía mal.")
##print (casa.text)
##print (casa.links)
##print(offsetSlots("<1> fue el <2> de mi <3>", 3))