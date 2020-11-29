import TextOperations
import re

class Link:
    def __init__(self, alias = [], operation = "", links = [], decoratedName = ""):
        self.alias = alias
        self.operation = operation
        self.links = links
        self.name = decoratedName

        if decoratedName:
            self.alias.append(decoratedName)

    def getFullText (self):
        text = self.operation

        for contador in range(len(self.links)+1) :
            text = text.replace ("<" + str(contador) + ">", self.links[contador])
            contador += 1

        return text

    def getName(self):
        return self.name if self.name else alias[0]

    def toJSON(self):
        json = {"alias": self.alias, "operation": self.operation, "links": self.links}
        if self.name:
            json["name"] = self.name
        return json

    def fromJSON(self, json):
        self.alias = json["alias"]
        self.operation = json["operation"]
        self.links = json["links"]

        try:
            self.name = json["name"]
            self.alias.append(json["name"])
        except:
            pass

    def fromUnformattedText(self, text):
        linkedText = TextOperations.extractLinks(text)
        self. operation = linkedText.text
        self.links = linkedText.links

    def addLinkToOperation(self, wordToMakeLink):
        posOfWord = self.operation.find(wordToMakeLink)
        print(posOfWord)
        contador = 0

        if posOfWord != -1:
            slotsBeforeMatch = re.findall(r'(<[1-9]+>)', self.operation[:posOfWord-1])
            print(slotsBeforeMatch)
            lastSlotPos = len(slotsBeforeMatch)
            print(lastSlotPos)
            wordReplacement = "<" + str(lastSlotPos+1) + ">"
            print(wordReplacement)
            newText = self.operation.replace(wordToMakeLink, wordReplacement)

            slotsAfterMatch = re.findall(r'(<[1-9]+>)', self.operation[posOfWord+len(wordToMakeLink)+1:])
            print (slotsAfterMatch)
            if (len(slotsAfterMatch)) > 0:
                
                wordsArray = re.split(r'(<[1-9]+>|\w+|[^a-zA-Z0-9_<>])', self.operation[posOfWord+len(wordToMakeLink):])
                print (wordsArray)

                slotCounter = lastSlotPos +1
                for word in wordsArray:
                    print(str(slotCounter) + " " + word)
                    if word != '':
                        if word == ("<" + str(slotCounter) + ">"):
                            slotCounter = slotCounter + 1
                            print ("encontré coincidencia " + str(contador) )
                            wordsArray[contador] = "<" + str(slotCounter) + ">"
                    contador = contador +1

                print(wordsArray)
                finalFormattedText = newText[:posOfWord+3]
                print (finalFormattedText)
                formattedTextAfterLink = "".join(wordsArray)
                print (formattedTextAfterLink)
                finalFormattedText = finalFormattedText + formattedTextAfterLink

            else:
                finalFormattedText = newText
                
            self.operation = finalFormattedText
            print(lastSlotPos)
            self.links.insert(lastSlotPos, wordToMakeLink)
                

        
##        wordsArray = re.split(r'(<[1-9]+>|\w+|[^a-zA-Z0-9_<>])', self.operation)
##        contador = 0
##        slotCounter = 1
##        wasWordTurnedIntoLink = False
##        positionForReplacement = 0
##
##        for word in wordsArray:
##            if word != '':
##                if word == ("<" + str(slotCounter) + ">") and not wasWordTurnedIntoLink:
##                    slotCounter = slotCounter + 1
##                elif word == ("<" + str(slotCounter) + ">") and wasWordTurnedIntoLink:
##                    wordsArray[contador] = "<" + str(slotCounter+1) + ">"
##                    slotCounter = slotCounter + 1
##                elif word == wordToMakeLink and not wasWordTurnedIntoLink:
##                    wasWordTurnedIntoLink = True
##                    positionForReplacement = slotCounter
##                    wordsArray[contador] = "<" + str(slotCounter) + ">"
##                elif word == wordToMakeLink and wasWordTurnedIntoLink:
##                    wordsArray[contador] = "<" + str(positionForReplacement) + ">"
##            contador += 1
##
##        if wasWordTurnedIntoLink:
##            self.links.insert(positionForReplacement-1, wordToMakeLink)
##            self.operation = "".join(wordsArray)
        

