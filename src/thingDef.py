# pylint: disable=unused-argument


#Creatures
class creature():
    def __init__(self, name = "None", maxHp: int = 0, hp: int = 0, tempHp: int = 0, speed: int = 30, initiative: int = 10, AC: int = 10, stats: dict = {"strength":10, "dexterity":10, "constitutio":10, "intelligence":10, "wisdom":10, "charisma":10}, inventory: list = [], gear: list = [], conditions: list = []):
        """Base class for all living things"""
        self.name = name
        if hp == None:
            hp = maxHp
        self.maxHp = maxHp
        self.hp = hp
        self.speed = speed
        self.initiative = initiative
        self.stats = stats
        self.inventory = inventory
        self.gear = gear
        self.alive = True
        self.conditions = conditions
        self.tempHp = tempHp
        self.isActive = False
        self.AC = AC
    def takeDamage(self, amount):
        lowAmount = amount - self.tempHp
        if lowAmount < 0:
            lowAmount = 0
        self.tempHp -= amount
        if self.tempHp < 0:
            self.tempHp = 0
        self.hp -= lowAmount
        if self.hp <= -self.maxHp:
            self.alive = False
        elif self.hp < 0:
            self.hp = 0
            self.conditions.append("downed")
    def heal(self, amount):
        self.hp += amount
        self.alive = True
        if self.hp > self.maxHp:
            self.hp = self.maxHp
    def addTempHp(self, amount):
        self.tempHp += amount
    def removeTempHp(self):
        self.tempHp = 0
    def updateStat(self, stat, value):
        self.stats[stat]=value
    def addGear(self, thing):
        self.gear.append(thing)
    def removeGear(self, thing):
        self.gear.remove(thing)
    def addInventory(self, item, amount=1):
        for i in range(amount):
            self.inventory.append(item)
    def removeInventory(self, item, amount):
        for i in range(amount):
            self.inventory.remove(item)
    def setInitiative(self, value):
        self.initiative = value
    def giveCondition(self, condition):
        self.conditions.append(condition)
    def removeCondition(self, condition):
        self.conditions.remove(condition)

class player(creature):
    def __init__(self, maxHp: int, hp: int = None, tempHp: int = 0, speed: int = 30, initiative: int = 10, AC: int = 10, stats: dict = {"strength":10, "dexterity":10, "constitutio":10, "intelligence":10, "wisdom":10, "charisma":10}, inventory: list = [], gear: list = [], conditions: list = []):
        super().__init__(maxHp, hp, tempHp, speed, initiative, AC, stats, inventory, gear, conditions)

#Weapons
class weapon():
    def __init__(self, damage: int, atributes: list, range:int):
        self.baseDamage = damage
        self.atributes = atributes

class rangedWeapon(weapon):
    def __init__(self, damage:int, atributes: list, ammoType, minRange:int, maxRange:int, usesAmmo=True):
        super().__init__(damage, atributes, minRange)
        self.maxRange = maxRange

class meleeWeapon(weapon):
    def __init__(self, damage:int, atributes:list, meleeRange:int):
        super().__init__(damage, atributes, meleeRange)



#Conditions
class condition():
    def __init__(self, name, effect, duration):
        self.name = name
        self.effect = effect
        self.duration = duration

class blinded(condition):
    def __init__(self, duration):
        super().__init__("Blinded", "A blinded creature can’t see and automatically fails any ability check that requires sight.\nAttack rolls against the creature have advantage, and the creature’s Attack rolls have disadvantage.", duration)

class charmed(condition):
    def __init__(self, duration):
        super().__init__("Charmed", "A charmed creature can’t Attack the charmer or target the charmer with harmful Abilities or magical Effects.\nThe charmer has advantage on any ability check to interact socially with the creature.", duration)

class deafened(condition):
    def __init__(self, duration):
        super().__init__("Deafened", "A deafened creature can’t hear and automatically fails any ability check that requires hearing.", duration)

class fatigued(condition):
    def __init__(self, duration):
        super().__init__("Fatigued", "See Exhaustion.", duration)

class frightened(condition):
    def __init__(self, duration):
        super().__init__("Frightened", "A frightened creature has disadvantage on Ability Checks and Attack rolls while the source of its fear is within line of sight.\nThe creature can’t willingly move closer to the source of its fear.", duration)

class grappled(condition):
    def __init__(self, duration):
        super().__init__("Grappled", "A grappled creature’s speed becomes 0, and it can’t benefit from any bonus to its speed.\nThe condition ends if the Grappler is incapacitated (see the condition).\nThe condition also ends if an effect removes the grappled creature from the reach of the Grappler or Grappling effect, such as when a creature is hurled away by the Thunderwave spell.", duration)

class incapacitated(condition):
    def __init__(self, duration):
        super().__init__("Incapacitated", "An incapacitated creature can’t take Actions or reactions.", duration)

class invisible(condition):
    def __init__(self, duration):
        super().__init__("Invisible", "An invisible creature is impossible to see without the aid of magic or a Special sense. For the purpose of Hiding, the creature is heavily obscured. The creature’s location can be detected by any noise it makes or any tracks it leaves.\nAttack rolls against the creature have disadvantage, and the creature’s Attack rolls have advantage.", duration)

class paralyzed(condition):
    def __init__(self, duration):
        super().__init__("Paralyzed", "A paralyzed creature is incapacitated (see the condition) and can’t move or speak. The creature automatically fails Strength and Dexterity Saving Throws. Attack rolls against the creature have advantage. Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.", duration)

class petrified(condition):
    def __init__(self, duration):
        super().__init__("Petrified", "A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into a solid inanimate substance (usually stone). Its weight increases by a factor of ten, and it ceases aging.\nThe creature is incapacitated (see the condition), can’t move or speak, and is unaware of its surroundings.\nAttack rolls against the creature have advantage.\nThe creature automatically fails Strength and Dexterity Saving Throws.\nThe creature has Resistance to all damage.\nThe creature is immune to poison and disease, although a poison or disease already in its system is suspended, not neutralized.", duration)

class poisoned(condition):
    def __init__(self, duration):
        super().__init__("Poisoned", "A poisoned creature has disadvantage on Attack rolls and Ability Checks.", duration)

class prone(condition):
    def __init__(self, duration):
        super().__init__("Prone", "A prone creature’s only Movement option is to crawl, unless it stands up and thereby ends the condition.\nThe creature has disadvantage on Attack rolls.\nAn Attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the Attack roll has disadvantage.", duration)

class restrained(condition):
    def __init__(self, duration):
        super().__init__("Restrained", "A restrained creature’s speed becomes 0, and it can’t benefit from any bonus to its speed. Attack rolls against the creature have advantage, and the creature’s Attack rolls have disadvantage. The creature has disadvantage on Dexterity Saving Throws.", duration)

class stunned(condition):
    def __init__(self, duration):
        super().__init__("Stunned", "A stunned creature is incapacitated (see the condition), can’t move, and can speak only falteringly. The creature automatically fails Strength and Dexterity Saving Throws. Attack rolls against the creature have advantage.", duration)

class unconscious(condition):
    def __init__(self, duration):
        super().__init__("Unconcious", "An unconscious creature is incapacitated (see the condition), can’t move or speak, and is unaware of its surroundings. The creature drops whatever it’s holding and falls prone. The creature automatically fails Strength and Dexterity Saving Throws. Attack rolls against the creature have advantage. Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.", duration)



#Exhaustion
class exhaustionOne(condition):
    def __init__(self):
        super().__init__("Exhaustion Level 1", "Disadvantage on Ability Checks", 0)

class exhaustionTwo(condition):
    def __init__(self):
        super().__init__("Exhaustion Level 2", "Disadvantage on Ability Checks, Speed halved", 0)

class exhaustionThree(condition):
    def __init__(self):
        super().__init__("Exhaustion Level 3", "Disadvantage on Ability Checks, Speed halved, Disadvantage on Attack rolls and Saving Throws", 0)

class exhaustionFour(condition):
    def __init__(self):
        super().__init__("Exhaustion Level 4", "Disadvantage on Ability Checks, Speed halved, Disadvantage on Attack rolls and Saving Throws, Hit point maximum halved", 0)

class exhaustionFive(condition):
    def __init__(self):
        super().__init__("Exhaustion Level 5", "Disadvantage on Ability Checks, Speed reduced to 0, Disadvantage on Attack rolls and Saving Throws, Hit point maximum halved", 0)

class exhaustionSix(condition):
    def __init__(self):
        super().__init__("Exhaustion Level 6", "Death", 0)



