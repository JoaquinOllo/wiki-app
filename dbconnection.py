import pymongo
from Link import Link
import re

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["linktity"]

docsCollection = mydb["docs"]

def addLink(link):
    jsonLink = link.toJSON()
    query = {"alias": link.alias}
    if not docsCollection.find_one(query):
        x = docsCollection.insert_one(jsonLink)

    for linkInside in link.links:
        if not existsLink(linkInside):
            newLink = Link(linkInside)
            addLink(newLink)

def addOrUpdateLink(link):
    jsonLink = link.toJSON()
    query = {"alias": link.alias}
    print(docsCollection.find_one(query))
    if not docsCollection.find_one(query):
        x = docsCollection.insert_one(jsonLink)
    else:
        updateLink(link.alias, link)

def getLink(title):
    query = {"alias": title}
    entity = docsCollection.find_one(query)
    link = Link()
    link.fromJSON(entity)
    return link

def getLinkByField(field, value):
    query = {field: value}
    print(query)
    entity = docsCollection.find_one(query)
    print(entity)
    link = Link()
    link.fromJSON(entity)
    return link

def getLinksByField(field, value):
    query = {field: value}
    entities = docsCollection.find(query)
    entitiesFormatted = []
    for entity in entities:
        link = Link()
        link.fromJSON(entity)
        entitiesFormatted.append(link)
    return entitiesFormatted

def getLinkByLinks(link):
    return getLinkByField("links", link)

def updateLink(title, modifiedLink):
    query = {"alias": title}
    link = modifiedLink.toJSON()
    entity = docsCollection.update_one(query, {"$set" : link})

    for innerLink in link["links"]:
        if not existsLink(innerLink):
            newLink = Link(innerLink)
            addLink(newLink)

def existsLink(title):
    query = {"alias": title}
    return bool(docsCollection.find_one(query))

def getLinksContainingWord(field, word):
    regularExpression = "^.*" + word + ".*$"
    regularExpression = re.compile(regularExpression, re.IGNORECASE)
    query = { field: { "$regex": regularExpression } }
    entities = docsCollection.find(query)
    entitiesFormatted = []
    for entity in entities:
        link = Link()
        link.fromJSON(entity)
        entitiesFormatted.append(link)
    return entitiesFormatted

##link = Link (["Grumbarg"], "<0> es <1> del ejército de <2>", ["general", "Rahash"], "Grumbarg el grande", 1)
##addLink(link)
##newLink = getLink(link.getName())
##print(newLink.getFullText())
##print (existsLink("holaa"))
##print (getLinkByLinks("pájaro").getName())
##print (getLinksByField("alias", "hola"))
##for i in getLinksContainingWord("alias", "guerra"):
##    print (i)
##print (getLink("Ruiseñor escarlata").getFormattedText())
##print (getLink("Ruiseñor escarlata").getFullText())
##print (getLinkByField("alias", "Muertos"))