import pymongo
import os
#from Constants import dbsettings
from bson.objectid import ObjectId
from Engine.Link import Link
from Engine.TextOperations import jsonify
import re
from flask import abort, render_template, current_app

try:
    USERNAME = os.environ['USERNAME']
    PASSWORD = os.environ['PASSWORD']
    connnectionString = os.environ['connnectionString']
except:
    from Constants import dbsettings
    USERNAME = dbsettings.USERNAME
    PASSWORD = dbsettings.PASSWORD
    connnectionString = dbsettings.connnectionString

USERNAME = "readandwrite"
PASSWORD = "5uORJJ9eootiprml"
connnectionString = "mongodb+srv://{username}:{password}@clasenodejsmongodb.63fs3.mongodb.net/<dbname>?retryWrites=true&w=majority"


userMap = {
    "username" : USERNAME,
    "password" : PASSWORD
}

#myclient = pymongo.MongoClient("mongodb://localhost:27017/")
connnectionString = connnectionString.format_map(userMap)
myclient = pymongo.MongoClient(connnectionString)


mydb = myclient["linktity"]

docsCollection = mydb["ScumAndVillainy"]

def addLink(link):
    jsonLink = link.toJSON()
    createdLinks = []
    query = {"alias": link.alias}
    if not docsCollection.find_one(query):
        x = docsCollection.insert_one(jsonLink)
        createdLinks.append(jsonify(jsonLink))

    for linkInside in link.links:
        if not existsLink(linkInside):
            newLink = Link(linkInside)
            createdLinks.append(addLink(newLink))

    return createdLinks

def addOrUpdateLink(link):
    jsonLink = link.toJSON()
    query = {"alias": link.alias}
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
    if field == "_id":
        query = {field: ObjectId(value)}
    else:
        query = {field: value}
    entity = docsCollection.find_one(query)
    if entity:
        link = Link()
        link.fromJSON(entity)
        return link
    else:
        return False


def getLinksByField(field, value):
    if field == "_id":
        query = {field: ObjectId(value)}
    else:
        query = {field: value}
    entities = docsCollection.find(query)
    entitiesFormatted = []
    for entity in entities:
        #current_app.logger.info("prueba")
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

def updateLinkById(id, modifiedLink):
    query = {"_id": ObjectId(id)}
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

def deleteLinkById(id):
    query = {"_id": ObjectId(id)}
    docsCollection.delete_one(query)

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
##for link in getLinksByField("_id", "5fd2bcf54e318fc347906f78"):
#    print (link)
# link = getLink("Mijail")
# print (link.id)
# link.alias.append("Mikhail")
# updateLinkById(link.id, link)