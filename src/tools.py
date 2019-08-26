import thingDef


def addCreature(name, speed, maxHp, initiative, creatureList, hp=None):
    if hp == None:
        hp = maxHp
    creature = thingDef.creature(name, hp, speed)
    creature.takeDamage(maxHp-hp)
    creature.rollInitiative(initiative)
    creatureList[name]=(creature)
    return creatureList