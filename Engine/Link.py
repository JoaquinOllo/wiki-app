from Engine import TextOperations
from bson.objectid import ObjectId
import re
from flask import Flask
from flask import current_app

class Link:
    def __init__(self, alias="", operation="", links=[], decoratedName=""):
        self.alias = []
        try:
            self.alias = self.alias + alias
        except TypeError as error:
            self.alias = [alias]
        self.operation = operation
        self.links = links
        self.name = decoratedName

        if decoratedName:
            self.alias.append(decoratedName)

    def getFullText(self):
        text = self.operation
        regex = "<[0-9]+>"
        replacementFunction = lambda match: self.links[int(match[0][1:-1])-1]
        
        if len(self.links) > 0:
            text = re.sub(regex, replacementFunction, text)

        
        return text

    def getFormattedText(self):
        text = self.operation
        regex = "<[0-9]+>"
        replacementFunction = lambda match: "<" + self.links[int(match[0][1:-1])-1] + ">"
        
        if len(self.links) > 0:
            formattedText = re.sub(regex, replacementFunction, text)
            return formattedText
        else:
            return text 

    def getName(self):
        return self.name if self.name else self.alias[0]

    def toJSON(self):
        json = {"alias": self.alias, "operation": self.operation, "links": self.links}
        try:
            if self.name:
                json["name"] = self.name
        except:
            pass

        try:
            if self.id:
                json["_id"] = str(self.id)
        except:
            pass
        return json

    def fromJSON(self, json):
        current_app.logger.info("calling fromJSON method")

        if json != None:
            self.alias = json["alias"]
            self.operation = json["operation"]
            self.links = json["links"]
            
            try:
                self.id = json["_id"]
            except:
                pass

            try:
                self.name = json["name"]
                self.alias.append(json["name"])
            except:
                pass

    def normalize (self):
        contador = 1
        newLinks = []
        slotsToNormalize = []
        repeatedCounter = 0

        for link in self.links:
            
            if link not in newLinks:
                newLinks.append(link)
            else:
                repeatedCounter = self.links.index(link) + 1
                slotsToNormalize.append((contador, repeatedCounter))
            contador += 1

        newOperation = self.operation

        for slot in slotsToNormalize:
            pattern = "(?<=<)" + str(slot[0]) + "(?=>)"
            regexPattern = re.compile(pattern)
            replacementFunction = lambda match: str(slot[1])
            newOperation = re.sub(regexPattern, replacementFunction, newOperation)

        self.operation = newOperation
        self.links = newLinks

    def fromUnformattedText(self, text):
        linkedText = TextOperations.extractLinks(text)
        self.operation = linkedText.text
        self.links = linkedText.links

    def addLinkToOperation(self, wordToMakeLink):

        formattedText = self.getFormattedText()

        wordSoughtPattern = "(?i)" + wordToMakeLink
        wordSoughtRegex = re.compile(wordSoughtPattern)

        replFunction = lambda match : "<" + match[0] + ">"

        newFormattedText = re.sub(wordSoughtRegex, replFunction, formattedText)

        self.fromUnformattedText(newFormattedText)

    def removeLink (self, wordToRemove):
        unformattedText = self.getFormattedText()
        newUnformattedText = TextOperations.undoSlot(unformattedText, wordToRemove)
        
        self.fromUnformattedText(newUnformattedText)

    def __str__(self):
        map = {"a": self.alias, "b": self.operation, "c": self.links}
        return "Link, alias: {a}, operation: {b}, links: {c}".format(**map)

    def __add__(self, secondLink):
        matchingTitles = [x for x in self.alias if x in secondLink.alias]

        if len(matchingTitles) == 0:
            raise ArithmeticError("The links share no title and can't be added")
        
        title = list(dict.fromkeys(self.alias + secondLink.alias))

        name = self.name

        self.operation = self.operation if self.operation[-1] == "." else self.operation + "."

        operation = self.operation + " " + TextOperations.offsetSlots(secondLink.operation, len(self.links))

        links = self.links + secondLink.links

        newLink = Link(title, operation, links, name)

        newLink.normalize()

        return newLink
