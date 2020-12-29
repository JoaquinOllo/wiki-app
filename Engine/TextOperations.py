import re


class LinkedText:
    def __init__(self, text, links=[], title=""):
        self.title = title
        self.text = text
        self.links = links

    def __str__(self):
        map = {"a": self.title, "b": self.text, "c": self.links}
        return "Texto linkeado, título: {a} texto: {b}, links: {c}".format(**map)  

class AnotatedText:
    def __init__(self, text):
        self.text = text
        self.sublinks = []
        
        mainLinkRegex = "(?<=<<).+?(?=>>)"
        regexMainLinkPattern = re.compile (mainLinkRegex)
        secondaryLinkRegex = "(?<=<).+?(?=>)"
        regexSecLinkPattern = re.compile (secondaryLinkRegex)
        fragmentRegex = r'(?<=\[).*?<<.+?>>.*?(?=\])'
        regexFragmPattern = re.compile (fragmentRegex)

        fragmentMatchesIter = re.finditer(regexFragmPattern, text)
        
        for match in fragmentMatchesIter:
            titleMatch = re.findall(regexMainLinkPattern, match[0])
            title = titleMatch[0]

            matchSentence = turnFragIntoSentence(match[0])

            linkedText = extractLinks(matchSentence)

            linkedText.title = title

            self.sublinks.append(linkedText)

    def __str__(self):
        sublinks = ""
        for i in self.sublinks:
            sublinks = sublinks + i.__str__() + ". "
        map = {"b": self.text, "c": sublinks}
        return "Texto formateado con links, texto: {b}, links: {c}".format(**map)        

    def getReducedText(self):
        
        newText = self.text
        fragmentRegex = r'\[.*?<<(.+?)>>.*?\]'
        regexFragmPattern = re.compile (fragmentRegex)

        replacementFunction = lambda match : "<" + match[1] + ">."

        newText = re.sub(regexFragmPattern, replacementFunction, self.text)

        return newText
            

def extractLinks(text):
    formattedText = LinkedText(text)
    contador = 1

    pattern = "(?<=<)(.+?)(?=>)"
    regexPattern = re.compile(pattern)

    links = re.findall(regexPattern, text)
    links = list(dict.fromkeys(links))
    formattedText.links = links

    for match in links:
        matchPattern = "(?<=<)("+ match +")(?=>)"
        matchRegex = re.compile(matchPattern)
        formattedText.text = re.sub(matchRegex, str(contador), formattedText.text)
        contador += 1
        
    return formattedText

    # formattedText = LinkedText("")
    # contador = 1
    # correccion = 0

    # pattern = "(?<=<).+?(?=>)"
    # regexPattern = re.compile(pattern)

    # links = re.findall(regexPattern, text)
    # links = list(dict.fromkeys(links))
    # formattedText.links = links

    # matchIterator = re.finditer(regexPattern, text)

    # linksDictionary = {}

    # for match in matchIterator:
    #     contadorAux = contador
    #     try:
    #         matchCode = linksDictionary[match[0]]
    #         contadorAux = matchCode
    #     except:
    #         linksDictionary[match[0]] = contadorAux

    #     text = (
    #         text[: match.start() - correccion]
    #         + str(contadorAux)
    #         + text[match.end() - correccion :]
    #     )
    #     contador = contador + 1
    #     caracteresCorreccion = len(str(contadorAux))
    #     correccion = correccion + match.end() - match.start() - caracteresCorreccion

    # formattedText.text = text

    # return formattedText


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
    if operationBeginning:
        operation = (
            operationBeginning
            if operationBeginning[-1] != " "
            else operationBeginning[:-1]
        )
    else:
        operation = ""

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

    return int(links[-1]) if links else 0

def offsetSlots(operation, existingSlots):
    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    replacementFunction = lambda match: str(int(match[0])+existingSlots)

    newOperation = re.sub(regexPattern, replacementFunction, operation)


    return newOperation
        
def turnFragIntoSentence(text):
    mainLinkRegex = "<<.+?>>"
    mainLinkPattern = re.compile(mainLinkRegex)

    textWOMainLink = re.sub(mainLinkPattern, "", text)

    punctuationMarksRegex = "^[ ,.:;\-!?]*"
    punctuationMarksPattern = re.compile(punctuationMarksRegex)

    textStartNormalized = re.sub(punctuationMarksPattern, "", textWOMainLink)

    punctuationMarksEndRegex = "[ ,.:;\-!?]$"
    punctuationMarksEndPattern = re.compile(punctuationMarksEndRegex)

    textEndNormalized = re.sub(punctuationMarksEndPattern, ".", textStartNormalized)

    textCapitalized = capitalize(textEndNormalized)

    return textCapitalized

def capitalize(text):
    firstLetterRegex = "(?i)[a-zñÑ]"
    firstLetterPattern = re.compile(firstLetterRegex)
    contador = 0
    newText = ""

    match = re.search(firstLetterPattern, text)

    if match:
        newText = text[:match.start(0)] + match[0].upper() + text[match.end(0):]

    return newText



##print (hasEnoughSlots("mi casa queda en <1> y <2>" ,3))
##print (generateOperation("Combatieron en la guerra", 3))
##print (getNumberOfLinksByOperation("<1> y <2> lucharon con <3>"))
##print (extendEnumerationByX("Combatieron en la guerra: <1>, <2>", 2))
##print(extendEnumerationByX("Aquí murió <1>.", 2))
#casa = extractLinks("<Amanda> vivió en el <Lago Brevis>, pero <Amanda> se sentía mal. Esto fue hasta que conoció a <Brevis>, <a> <b> <c> <b> <a> <d>")
#print (casa.text)
#print (casa.links)
##print(offsetSlots("<1> fue el <2> de mi <3>", 3))
#casa = AnotatedText("Se encontró con [<<Aurigas>> (<teniente general> del <quinto ejército>)] Cenaron juntos en [el arcón gris].")
#print (casa.getReducedText())
#print (turnFragIntoSentence(", <teniente general> del <quinto ejército>"))