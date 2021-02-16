"""Text Operations

This script contains utility functions and classes to perform string operations related to the extension, alteration or generation of Links.
"""

import re


class LinkedText:
    """
    A class used to represent unformatted text and an accompanying list of slotted links.

    ...

    Attributes
    ----------
    text : str
        unformatted text containing markup for slots < >
    title : str
        an optional identifier for the object
    links : list
        A list of slotted link references

    Methods
    -------
    getReducedText(self)
        Returns unformatted text without the annotations for sublinks
    """
    def __init__(self, text: str, links:list=[], title:str=""):
        self.title = title
        self.text = text
        self.links = links

    def __str__(self):
        map = {"a": self.title, "b": self.text, "c": self.links}
        return "Texto linkeado, título: {a} texto: {b}, links: {c}".format(**map)  

class AnotatedText:
    """
    A class used to represent formatted text containing slots with their definitions in the same text.

    ...

    Attributes
    ----------
    text : str
        unformatted text containing markup for slots < > and slot annotations [<<slot>> (<slot annotation>)]
    sublinks : list
        A list of LinkedText items containing all slots, along with their annotations (definitions)

    Methods
    -------
    getReducedText(self)
        Returns unformatted text without the annotations for sublinks
    """
    def __init__(self, text: str):
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

    def __str__(self) -> str:
        sublinks = ""
        for i in self.sublinks:
            sublinks = sublinks + i.__str__() + ". "
        map = {"b": self.text, "c": sublinks}
        return "Texto formateado con links, texto: {b}, links: {c}".format(**map)        

    def getReducedText(self) -> str:
        """Returns a LinkedText object formatting the provided text. The object contains the existing links as an array.
        ----------
        name : self
            The AnotatedText object
        """ 
        
        newText = self.text
        fragmentRegex = r'\[.*?<<(.+?)>>.*?\]'
        regexFragmPattern = re.compile (fragmentRegex)

        replacementFunction = lambda match : "<" + match[1] + ">."

        newText = re.sub(regexFragmPattern, replacementFunction, self.text)

        return newText
            

def extractLinks(text: str) -> LinkedText:
    """Returns a LinkedText object formatting the provided text. The object contains the existing links as an array.
    ----------
    name : text
        An unformatted string containing slots
    """ 
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

def extendEnumerationByX(operation: str, ammountOfNewSlots: int) -> str:
    """Extends an enumeration, adding new slots to it, sepparated by commas.
    ----------
    name : operation
        The operation attribute of a Link object
    name : ammountOfNewSlots
        The amount of new slots to add to the operation
    """ 
    existingSlots = getNumberOfLinksByOperation(operation)

    indexOfOpBeginning = operation.find("<1>")

    operationBeginning = (
        operation if indexOfOpBeginning == -1 else operation[:indexOfOpBeginning]
    )

    newSlots = existingSlots + ammountOfNewSlots

    return generateOperation(operationBeginning, newSlots)


def hasEnoughSlots(operation: str, nOfSlotsNeeded: int) -> bool:
    """Returns a boolean value indicating whether an operation contains enough slots as needed, or not.
    ----------
    name : operation
        The operation attribute of a Link object
    name : nOfSlotsNeeded
        The amount of slots the operation must have
    """ 
    hasEnoughSlots = True

    for contador in range(nOfSlotsNeeded):
        if operation.find("<" + str(contador + 1) + ">") == -1:
            hasEnoughSlots = False
            break

    return hasEnoughSlots


def generateOperation(operationBeginning: str, nOfSlots: int) -> str:
    """Generates a simple enumerative operation, by using commas to list all slots after a provided operation beginning.
    ----------
    name : operationBeginning
        The beginning of an operation, after the first slot
    name : nOfSlots
        The amount of slots to be listed in the operation
    """ 
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


def getNumberOfLinksByOperation(operation: str) -> int:
    """Returns the number of links in a formatted operation passed as argument.
    ----------
    name : operation
        The operation attribute of a Link object
    """ 
    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    links = re.findall(regexPattern, operation)

    return int(links[-1]) if links else 0

def offsetSlots(operation: str, existingSlots: int) -> str:
    """Offsets numeric slots referencing links by the ammount indicated in the 2nd parameter.
    Parameters
    ----------
    name : operation
        The operation attribute of a Link object
    name : existingSlots
        An integer indicating the value of the offset operation for the operation
    """ 
    pattern = "(?<=<).+?(?=>)"
    regexPattern = re.compile(pattern)

    replacementFunction = lambda match: str(int(match[0])+existingSlots)

    newOperation = re.sub(regexPattern, replacementFunction, operation)


    return newOperation
        
def turnFragIntoSentence(text: str) -> str:
    """Returns the text capitalized and adds a period at its end, if it hasn't it already. Recognizes slotted text.
    Parameters
    ----------
    name : text
        Any kind of string, slotted or not.
    """ 
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

def capitalize(text: str) -> str:
    """Capitalizes the first character in a provided text, omitting slot markers like < and >
    Parameters
    ----------
    name : text
        Any kind of string, slotted or not.
    """ 
    firstLetterRegex = "(?i)[a-zñÑ]"
    firstLetterPattern = re.compile(firstLetterRegex)
    contador = 0
    newText = ""

    match = re.search(firstLetterPattern, text)

    if match:
        newText = text[:match.start(0)] + match[0].upper() + text[match.end(0):]

    return newText

def undoSlot(text: str, wordToUnslot: str) -> str:
    """Turns a slot from a text input into common text
    Parameters
    ----------
    name : text
        Unformatted text with links
    name : wordToUnslot
        A word already present in the text input as a slot, which will be unslotted
    """
    unslotRegex = "<%s>" % wordToUnslot
    unslotPattern = re.compile (unslotRegex)

    newText = re.sub(unslotPattern, wordToUnslot, text)
    return newText


def validateJSON(jsonInput: object) -> bool:
    """Validates whether a json passed as argument is valid as a possible link. The only required attribute is 'name', everything else is optional.
    Parameters
    ----------
    name : jsonInput
        A json provided as input
    """
    isValid = False
    if jsonInput != None:
        try:
            isValid = True if jsonInput["name"] else False
        except:
            pass
    return isValid


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
#print (undoSlot("<teniente general> del <quinto ejército>", "teniente general"))
#print (validateJSON({"name": "hola"}))
#print (validateJSON({"chateau": "hola"}))