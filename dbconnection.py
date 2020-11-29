import pymongo
from Link import Link

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["linktity"]

docsCollection = mydb["docs"]

def addLink(link):
    jsonLink = link.toJSON()
    query = {"alias": link.alias}
    print(docsCollection.find_one(query))
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

def getLinkByLinks(link):
    query = {"links": link}
    entity = docsCollection.find_one(query)
    link = Link()
    link.fromJSON(entity)
    return link

def updateLink(title, modifiedLink):
    query = {"alias": title}
    link = modifiedLink.toJSON()
    entity = docsCollection.update_one(query, {"$set" : link})

    for linkInside in link.links:
        if not existsLink(linkInside):
            newLink = Link(linkInside)
            addLink(newLink)

def existsLink(title):
    query = {"alias": title}
    return bool(docsCollection.find_one(query))

##link = Link (["Grumbarg"], "<0> es <1> del ejército de <2>", ["general", "Rahash"], "Grumbarg el grande", 1)
##addLink(link)
##newLink = getLink(link.getName())
##print(newLink.getFullText())
##print (existsLink("holaa"))
print (getLinkByLinks("pájaro").getName())
