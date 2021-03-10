from Engine.Link import Link
from Engine import dbconnection
from Engine import TextOperations
from Engine.TextOperations import propertyExists
from flask import current_app

#Normalize: functions should return updated and created links

def registerSimpleEntry (title: str, text: str):
    #TODO rewrite and normalize
    newEntry = Link(title, text, [], "")
    saveLink(newEntry)

def saveLink (link: object) -> list:
    return dbconnection.addLink(link)

def existsLink(title: str) -> bool:
    #TODO rewrite for query by id, check if needed
    return dbconnection.existsLink(title)

def editLink (title, newLink):
    #TODO rewrite for query by id, check if needed
    dbconnection.updateLink(title, newLink)

def editLinkPartially (title, newLink):
    #TODO rewrite for query by id, check if needed
    editionLink = getLink(title)
    formattedNewLink = Link()
    formattedNewLink.fromJSON(newLink)

    if formattedNewLink.alias:
        editionLink.alias = formattedNewLink.alias
    
    if formattedNewLink.operation:
        editionLink.operation = formattedNewLink.operation
    
    if formattedNewLink.links:
        editionLink.links = formattedNewLink.links

    editLinkByID(editionLink.id, editionLink)

def editLinkByID (id: str, newLink):
    #TODO normalize
    if (isinstance(newLink, Link)):
        dbconnection.updateLinkById(id, newLink)
    else:
        link = Link()
        link.fromJSON(newLink)
        dbconnection.updateLinkById(id, link)

def deleteLinkByField(field: str, value: str) -> list:
    #TODO normalize (use returned value by dbconnection function)
    deletedLinks = []
    link = dbconnection.getLinkByField(field, value)
    if link:
        dbconnection.deleteLinkById(link.id)
        deletedLinks.append(link.toJSON())
        #current_app.logger.info(link)

        for alias in link.alias:
            mentions = seekManyByLink(alias)
            for mention in mentions:
                removeLinkFromEntity(mention.id, alias)
                deletedLinks.append(mention.toJSON())

    return deletedLinks

def deleteManyByField(field: str, value: str):
    #TODO normalize and check if needed
    links = dbconnection.getLinksByField(field, value)
    for link in links:
        dbconnection.deleteLinkById(link.id)

def editSimpleEntry (title, newText):
    #TODO normalize and check if needed
    entry = dbconnection.getLink(title)
    entry.operation = newText
    editLink(title, entry)

def getLink (title: str) -> object:
    entry = dbconnection.getLinksContainingWord("alias", title)
    if entry:
        return entry[0]
    else:
        return False

def getLinkByID (id: str) -> object:
    entry = dbconnection.getLinkByField("_id", id)
    return entry    

def addAliasToLink(title: str, newAlias: str):
    #TODO normalize
    entry = getLink(title)
    entry.alias.append(newAlias)
    editLink(title, entry)

def registerEmptyEntry(title: str):
    #TODO normalize and check if needed
    newEntry = Link(title)
    saveLink(newEntry)

def registerSimpleLink(jsonInput: object) -> list:
    """
    Creates and saves a new link to the database, using a json as input. Validates that the json has the required format. The created link will either have just an alias (an empty link), or be complete (alias, plus operation and links). The function returns the created link.

    Parameters
    ----------
    name : jsonInput
        A json provided as input, which will be validated against the TextOperations.validateJSON function (an "alias" property is the only requirement).

    Raises
    ------
    TypeError
        If jsonInput parameter doesn't pass the validation, an error is raised.
    """    
    if (TextOperations.validateJSON(jsonInput)):
        linkAlias = jsonInput["alias"]
        link = Link(linkAlias)
        if propertyExists(jsonInput, "text"):
            link.fromUnformattedText(jsonInput["text"])
        createdLinks = saveLink(link)
        return createdLinks
    else:
        raise TypeError("Inadequate json input format. JSON input must have a name attribute, at least.")

def editLinkAtPosition(title: str, linkPos: int, newLink: str):
    #TODO normalize and check if needed and rewrite to query by id
    link = getLink(title)
    link.links[linkPos] = newLink
    editLink(title, link)

def registerTag (tag: str, text: str):
    #TODO normalize
    registerSimpleEntry(tag, text + ": ")

def extendTag (tag: str, newLink: str):
    #TODO normalize and check if needed and rewrite to query by id
    extendTagByMany (tag, [newLink])

def extendTagByMany (tag: str, newLinks: list):
    #TODO normalize and rewrite to query by id
    tagLink = getLink(tag)

    amountOfNewSlots = len(newLinks)

    newOperation = TextOperations.extendEnumerationByX(tagLink.operation, amountOfNewSlots)
    tagLink.operation = newOperation

    tagLink.links = tagLink.links + newLinks

    editLink(tag, tagLink)

def drawLinkBetween2 (title: str, operation: str, source: str, destination: str):
    #TODO normalize and rewrite to query by id

    if TextOperations.hasEnoughSlots(operation, 2):
        links = [source, destination]
        link = Link(title, operation, links)
        saveLink(link)
    

def groupLinks (title: str, operation: str, titles: list):
    #TODO normalize and raise exception if conditions aren't fulfilled and rewrite to query by id
    if TextOperations.hasEnoughSlots(operation, len(titles)):
        link = Link(title, operation, titles)
        saveLink(link)

def enumerateLinks (title: str, operationBeginning: str, titles: list):
    #TODO normalize and rewrite to query by id
    operation = TextOperations.generateOperation(operationBeginning, len(titles))
    link = Link (title, operation, titles)
    saveLink(link)

def addLinkToEntry (title: str, wordToMakeLink: str):
    #TODO normalize and rewrite to query by id
    link = getLink(title)
    link.addLinkToOperation(wordToMakeLink)
    id = link.id
    editLinkByID(id, link)

def addLinkToEntryByID (id: str, wordToMakeLink: str):
    #TODO normalize
    link = getLinkByID(id)
    link.addLinkToOperation(wordToMakeLink)
    id = link.id
    editLinkByID(id, link)

def followLink (title: str, link: str) -> object:
    #TODO normalize and rewrite to query by id
    topLink = getLink(title)
    if link in topLink.links:
        return getLink(link)

def severeLink (entity, link):
    #TODO
    pass

def seekByLink (link: str) -> object:
    #TODO check if needed
    return dbconnection.getLinkByLinks(link)

def getManyByField(value: str, field: str) -> list:
    current_app.logger.info("call to getManyByField")
    if field == "id" or field == "_id":
        return dbconnection.getLinksByField("_id", value)
    else:
        return dbconnection.getLinksContainingWord(field, value)

def seekManyByTitle (title: str) -> list:
    #TODO check if needed
    return dbconnection.getLinksByField("alias", title)

def seekManyByLink (linkText: str) -> list:
    #TODO check if needed
    return dbconnection.getLinksByField("links", linkText)

def seekManyByOperation (operationSought: str) -> list:
    #TODO check if needed
    return dbconnection.getLinksByField("operation", operationSought)

def seekManyByAliasAndLink (link: str) -> list:
    linksByAlias = dbconnection.getLinksByField("alias", link)
    linksByLink = dbconnection.getLinksByField("links", link)
    return linksByAlias + linksByLink

def registerLink (title: str, operation: str, entitiesLinked:list = []):
    #TODO normalize and check if needed
    newLink = Link(title, operation, entitiesLinked)
    saveLink (newLink)

def addDecoratedName(aliasSought: str, decoratedName: str):
    #TODO normalize
    link = getLink(aliasSought)
    link.name = decoratedName
    editLink(aliasSought, link)

def getLinkAndChildren(linkAlias: str) -> list:
    fatherLink = getLink(linkAlias)

    fatherAndChildren = []

    fatherAndChildren.append(fatherLink)
    
    for innerLink in fatherLink.links:
        childLink = getLink(innerLink)
        fatherAndChildren.append(childLink)

    return fatherAndChildren

def registerLinkFromUnformattedText(title: str, text: str):
    #TODO normalize and check if needed
    newEntry = Link(title, text, [], "")
    newEntry.fromUnformattedText(text)
    saveLink(newEntry)

def getUndevelopedEntries() -> list:
    return seekManyByOperation("")

def mergeIdenticalLinks(title: str):
    #TODO normalize
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

def collectMentionsForTag(tagTitle: str):
    #TODO normalize
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

def registerAnnotatedLink(title: str, text: str):
    #TODO normalize
    annotatedText = TextOperations.annotatedText(text)
    reducedText = annotatedText.getReducedText()
    sublinks = annotatedText.sublinks
    for sublink in sublinks:
        registerLink(sublink.title, sublink.text, sublink.links)

    registerLinkFromUnformattedText(title, reducedText)

def unifyLinks(centerTitle: str, titlesToDelete: list):
    #TODO normalize and check if needed
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
    #TODO
    pass

def getIndirectReferences(tagTitle: str) -> list:
    indirectMentions = dbconnection.getLinksContainingWord("operation", tagTitle)
    return indirectMentions

def turnIndirectReferencesIntoTag(tagTitle: str):
    #TODO normalize
    indirectMentions = getIndirectReferences(tagTitle)
    tagReferences = []

    for mention in indirectMentions:
        
        addLinkToEntryByID(mention.id, tagTitle)
        tagReferences.append(mention.getName())

    registerTag(tagTitle, "")
    extendTagByMany(tagTitle, tagReferences)

def removeLinkFromEntity(id: str, wordToRemove: str):
    #TODO normalize
    link = getLinkByID(id)
    link.removeLink(wordToRemove)
    editLinkByID(id, link)

#TODO: develop a function to seek a link that contains a particular slot.


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
##registerLinkFromUnformattedText("El castillo de Trento", "Construido por el <Duque Versillis>, posteriormente a la <Guerra de las Rosas>, sobre este castillo cayó una poderosa maldición por parte de <Tiresia>.")
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
#registerAnnotatedLink("Sesión 3", "Se encontró con [<<Aurigas>>, <teniente general> del <quinto ejército>.] Cenaron juntos en el <arcón gris>.")
#registerEmptyEntry("PJs")
#unifyLinks("PJ", ["PJs"])
#turnIndirectReferencesIntoTag("trasfondo")
#removeLinkFromEntity(getLink("PJ").id, "Nova")
#deleteLinkByField("alias", "Mikhail")
#for link in getManyByField("id", "600f8f9d6eb52f5b61dc5f49"):
#    print (link)