creatureDict = {}
creatureIndex = []

def getInitiative(creatureName):
    return creatureDict[creatureName].initiative

def addCreature(creature):
    if creature.name in creatureIndex:
        return -1
    else:
        creatureDict[creature.name] = creature
        creatureIndex.append(creature.name)
        sortIndex()
        return 0

def sortIndex():
    creatureIndex.sort(key=getInitiative, reverse=True)

def turn():
    creatureObj = [creatureDict[i] for i in creatureIndex]
    nextCreature = False
    found = False
    for creature in creatureObj:
        if nextCreature:
            creature.isActive = True
            found = True
            break
        if creature.isActive:
            nextCreature = True
            creature.isActive = False
    if not found:
        try:
            creatureObj[0].isActive = True
        except IndexError:
            pass

def deleteChar(creatureName):
    del creatureDict[creatureName]
    creatureIndex.remove(creatureName)