from Engine.Link import Link
from Engine import dbconnection
from Engine import TextOperations

def registerSimpleEntry (title, text):
    newEntry = Link(title, text, [], "")
    saveLink(newEntry)

def saveLink (link):
    dbconnection.addLink(link)

def existsLink(title):
    return dbconnection.existsLink(title)

def editLink (title, newLink):
    dbconnection.updateLink(title, newLink)

def editLinkPartially (title, newLink):
    editionLink = getLink(title)
    formattedNewLink = Link()
    formattedNewLink.fromJSON(newLink)
    print (formattedNewLink)

    if formattedNewLink.alias:
        print (editionLink.alias)
        print (formattedNewLink.alias)
        editionLink.alias = formattedNewLink.alias
    
    if formattedNewLink.operation:
        editionLink.operation = formattedNewLink.operation
    
    if formattedNewLink.links:
        editionLink.links = formattedNewLink.links

    editLinkByID(editionLink.id, editionLink)

def editLinkByID (id, newLink):
    dbconnection.updateLinkById(id, newLink)    

def deleteLinkByField(field, value):
    link = dbconnection.getLinkByField(field, value)
    if link:
        dbconnection.deleteLinkById(link.id)

    for alias in link.alias:
        mentions = seekManyByLink(alias)
        for mention in mentions:
            removeLinkFromEntity(mention.id, alias)

def deleteManyByField(field, value):
    links = dbconnection.getLinksByField(field, value)
    for link in links:
        dbconnection.deleteLinkById(link.id)

def editSimpleEntry (title, newText):
    entry = dbconnection.getLink(title)
    entry.operation = newText
    editLink(title, entry)

def getLink (title):
    entry = dbconnection.getLinksContainingWord("alias", title)
    return entry[0]

def getLinkByID (id):
    entry = dbconnection.getLinkByField("_id", id)
    return entry    

def addAliasToLink(title, newAlias):
    entry = getLink(title)
    entry.alias.append(newAlias)
    editLink(title, entry)

def registerEmptyEntry(title):
    newEntry = Link(title)
    saveLink(newEntry)

def registerSimpleLink(title, text):
    link = Link(title)
    link.fromUnformattedText(text)
    saveLink(link)

def editLinkAtPosition(title, linkPos, newLink):
    link = getLink(title)
    link.links[linkPos] = newLink
    editLink(title, link)

def registerTag (tag, text):
    registerSimpleEntry(tag, text + ": ")

def extendTag (tag, newLink):
    extendTagByMany (tag, [newLink])

def extendTagByMany (tag, newLinks):
    tagLink = getLink(tag)

    amountOfNewSlots = len(newLinks)

    newOperation = TextOperations.extendEnumerationByX(tagLink.operation, amountOfNewSlots)
    tagLink.operation = newOperation

    tagLink.links = tagLink.links + newLinks

    editLink(tag, tagLink)

def drawLinkBetween2 (title, operation, source, destination):

    if TextOperations.hasEnoughSlots(operation, 2):
        links = [source, destination]
        link = Link(title, operation, links)
        saveLink(link)
    

def groupLinks (title, operation, titles):
    if TextOperations.hasEnoughSlots(operation, len(titles)):
        link = Link(title, operation, titles)
        saveLink(link)

def enumerateLinks (title, operationBeginning, titles):
    operation = TextOperations.generateOperation(operationBeginning, len(titles))
    link = Link (title, operation, titles)
    saveLink(link)

def addLinkToEntry (title, wordToMakeLink):
    link = getLink(title)
    link.addLinkToOperation(wordToMakeLink)
    id = link.id
    editLinkByID(id, link)

def addLinkToEntryByID (id, wordToMakeLink):
    link = getLinkByID(id)
    link.addLinkToOperation(wordToMakeLink)
    id = link.id
    editLinkByID(id, link)

def followLink (title, link):
    topLink = getLink(title)
    if link in topLink.links:
        return getLink(link)

def severeLink (entity, link):
    pass

def seekByLink (link):
    return dbconnection.getLinkByLinks(link)

def getManyByField(value, field):
    if field == "id" or field == "_id":
        return dbconnection.getLinksByField("_id", value)
    else:
        return dbconnection.getLinksContainingWord(field, value)

def seekManyByTitle (title):
    return dbconnection.getLinksByField("alias", title)

def seekManyByLink (linkText):
    return dbconnection.getLinksByField("links", linkText)

def seekManyByOperation (operationSought):
    return dbconnection.getLinksByField("operation", operationSought)

def seekManyByAliasAndLink (link):
    linksByAlias = dbconnection.getLinksByField("alias", link)
    linksByLink = dbconnection.getLinksByField("links", link)
    return linksByAlias + linksByLink

def registerLink (title, operation, entitiesLinked = []):
    newLink = Link(title, operation, entitiesLinked)
    saveLink (newLink)

def addDecoratedName(aliasSought, decoratedName):
    link = getLink(aliasSought)
    link.name = decoratedName
    editLink(aliasSought, link)

def getLinkAndChildren(linkAlias):
    fatherLink = getLink(linkAlias)

    fatherAndChildren = []

    fatherAndChildren.append(fatherLink)
    
    for innerLink in fatherLink.links:
        childLink = getLink(innerLink)
        fatherAndChildren.append(childLink)

    return fatherAndChildren

def registerLinkFromFormattedText(title, text):
    newEntry = Link(title, text, [], "")
    newEntry.fromUnformattedText(text)
    saveLink(newEntry)

def getUndevelopedEntries():
    return seekManyByOperation("")

def mergeIdenticalLinks(title):
    mainLink = getLink(title)
    contador = 0
    id = mainLink.id
    links = seekManyByTitle(title)
    linksIdToDelete = []

    for link in links:
        #print (link)
        if contador > 0:
            mainLink = mainLink + link
            linksIdToDelete.append(link.id)
        contador += 1
    editLinkByID(id, mainLink)

    for id in linksIdToDelete:
        deleteLinkByField("_id", id)

def collectMentionsForTag(tagTitle):
    mentions = seekManyByLink(tagTitle)
    link = getLink(tagTitle)
    mentionsToAdd = []
    for mention in mentions:
        alreadyInLink = False
        for alias in mention.alias:
            if alias in link.links:
                alreadyInLink = True
                break
        if alreadyInLink == False:
            mentionsToAdd.append(mention.getName())

    if mentionsToAdd:
        newOperation = TextOperations.extendEnumerationByX(link.operation, len(mentionsToAdd))
        newLinks = link.links + mentionsToAdd
        link.operation = newOperation
        link.links = newLinks

        editLinkByID(link.id, link)

def registerAnotatedLink(title, text):
    anotatedText = TextOperations.AnotatedText(text)
    reducedText = anotatedText.getReducedText()
    sublinks = anotatedText.sublinks
    for sublink in sublinks:
        registerLink(sublink.title, sublink.text, sublink.links)

    registerLinkFromFormattedText(title, reducedText)

def unifyLinks(centerTitle, titlesToDelete):
    mainLink = getLink(centerTitle)
    id = mainLink.id
    links = []
    for titleToDelete in titlesToDelete:
        link = getLink(titleToDelete)
        if link:
            links.append(link)
    linksIdToDelete = []

    for link in links:
        link.alias.append(mainLink.getName())
        mainLink = mainLink + link
        linksIdToDelete.append(link.id)

    editLinkByID(id, mainLink)

    for id in linksIdToDelete:
        deleteLinkByField("_id", id)

def replaceOperationForLink(title, textToReplace, linkForSlot):
    pass

def getIndirectReferences(tagTitle):
    indirectMentions = dbconnection.getLinksContainingWord("operation", tagTitle)
    return indirectMentions

def turnIndirectReferencesIntoTag(tagTitle):
    indirectMentions = getIndirectReferences(tagTitle)
    tagReferences = []

    for mention in indirectMentions:
        
        addLinkToEntryByID(mention.id, tagTitle)
        tagReferences.append(mention.getName())

    registerTag(tagTitle, "")
    extendTagByMany(tagTitle, tagReferences)

def removeLinkFromEntity(id, wordToRemove):
    link = getLinkByID(id)
    link.removeLink(wordToRemove)
    editLinkByID(id, link)



##editSimpleEntry("hola", "quien eras tuu")
##addAliasToLink("hola", "chau")
##registerSimpleLink("hola", "<paquita> vivió en la selva de <gurgeld> 13 años")
##drawLinkBetween2("relacion", "<1> era enemigo de <2>", "hola", "articulo")
##groupLinks ("Guerra de maldor", "En ella lucharon <1>, <2>, y <3>", ["Gombarg", "Hazili", "Ferrush"])
##enumerateLinks("Muertos", "Murieron en la guerra", ["Gombarg", "Hazili", "Trubasc"])
##registerSimpleEntry("La iglesia escarlata", "esta iglesia fue fundada en el año 1320, por Teodorico 1ro")
##addLinkToEntry("La iglesia escarlata", "iglesia")
##registerSimpleEntry("Ruiseñor escarlata", "Este curioso pájaro, plaga de los bosques arqueados, tiene un origen desconocido")
##addLinkToEntry("Ruiseñor escarlata", "pájaro")
##print (seekManyByTitle("hola"))
##print (seekManyByLink("paquita"))
##registerLinkFromFormattedText("El castillo de Trento", "Construido por el <Duque Versillis>, posteriormente a la <Guerra de las Rosas>, sobre este castillo cayó una poderosa maldición por parte de <Tiresia>.")
##print (seekByLink("paquita"))
##for link in getLinkAndChildren("articulo"):
##    print(link)
##extendTagByMany("Muertos", ["Theron"])
#registerLink("La catarata escarlata", "Siete guerreros perecieron tratando de cruzar esta famosa catarata y encontrar su afamado tesoro, el <1>.", ["Grial de San Bernardo"])
##for entry in getUndevelopedEntries():
##    print (entry)
##print (getLink("Mijail").getFormattedText())
##registerSimpleEntry("Mijail", "Mijail es cascarrabias")
##getLink("Mijail") + getLink("AK")
##getLink("Mijail") + getLink("PJ")
##registerSimpleLink(["Mijail", "Sergei"], "En la guerra de la rebelión, Mijail fue prisionero de <Garruk>.")
##getLink("Mijail") + getLink("Sergei")
#registerSimpleLink("hola", "hola")
#deleteLinkByField("alias", "hola")
#mergeIdenticalLinks("Mijail")
#print(getLink("Mijail") + getLink("Sergei"))
#collectMentionsForTag("PJ")
#print(getLink("PJ"))
#registerAnotatedLink("Sesión 3", "Se encontró con [<<Aurigas>>, <teniente general> del <quinto ejército>.] Cenaron juntos en el <arcón gris>.")
#registerEmptyEntry("PJs")
#unifyLinks("PJ", ["PJs"])
#turnIndirectReferencesIntoTag("trasfondo")
#removeLinkFromEntity(getLink("PJ").id, "Nova")
#deleteLinkByField("alias", "Mikhail")
#for link in getManyByField("id", "600f8f9d6eb52f5b61dc5f49"):
#    print (link)