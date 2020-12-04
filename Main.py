from Link import Link
import dbconnection
import TextOperations

def registerSimpleEntry (title, text):
    newEntry = Link([title], text, [], "")
    saveLink(newEntry)

def saveLink (link):
    dbconnection.addLink(link)

def existsLink(title):
    return dbconnection.existsLink(title)

def editLink (title, newLink):
    dbconnection.updateLink(title, newLink)

def editSimpleEntry (title, newText):
    entry = dbconnection.getLink(title)
    entry.operation = newText
    editLink(title, entry)

def getLink (title):
    entry = dbconnection.getLink(title)
    return entry

def addAliasToLink(title, newAlias):
    entry = getLink(title)
    entry.alias.append(newAlias)
    editLink(title, entry)

def registerEmptyEntry(title):
    newEntry = Link([title])
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
    pass

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
    editLink(title, link)

def followLink (title, link):
    topLink = getLink(title)
    if link in topLink.links:
        return getLink(link)

def severeLink (entity, link):
    blank

def seekByLink (link):
    return dbconnection.getLinkByLinks(link)

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

def addDecoratedName(aliasSought, decoratedName):
    blank

def getLinkAndChildren(linkAlias):
    blank

def registerLinkFromFormattedText(title, text):
    newEntry = Link(title, text, [], "")
    newEntry.fromUnformattedText(text)
    saveLink(newEntry)

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