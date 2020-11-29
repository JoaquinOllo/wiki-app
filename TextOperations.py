import re

class LinkedText:

    def __init__(self, text, links = []):
        self.text = text
        self.links = links

def extractLinks(text):
    formattedText = LinkedText("")
    contador = 1
    correccion = 0

    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    links = re.findall(regexPattern, text)
    formattedText.links = links

    matchIterator = re.finditer (regexPattern, text)

    for match in matchIterator:
        text = text[:match.start()-correccion] + str(contador) + text[match.end()-correccion:]
        contador = contador + 1
        correccion = correccion + match.end() - match.start() -1

    formattedText.text = text
    
    return formattedText

def hasEnoughSlots(operation, nOfSlotsNeeded):
    hasEnoughSlots = True

    for contador in range(nOfSlotsNeeded):
        if operation.find("<" + str(contador+1) + ">") == -1:
            hasEnoughSlots = False
            break

    return hasEnoughSlots

def generateOperation(operationBeginning, nOfSlots):
    operation = operationBeginning + " "

    for contador in range(nOfSlots):
        if contador != 0:
            operation = operation + ","
        operation = operation + " <" + str(contador+1) + ">"

    operation = operation + "."

    return operation


##print (hasEnoughSlots("mi casa queda en <1> y <2>" ,3))
##print (generateOperation("Combatieron en la guerra", 3))
