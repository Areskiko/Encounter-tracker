class creature():
    def __init__(self, maxHp: int, hp: int = None, tempHp: int = 0, speed: int = 30, initiative: int = 10, stats: dict = {"strength":10, "dexterity":10, "constitutio":10, "intelligence":10, "wisdom":10, "charisma":10}, inventory: list = [], gear: list = [], conditions: list = []):
        """Base class for all living things"""
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
    def takeDamage(self, amount):
        self.hp -= amount
        if self.hp <= self.maxHp:
            self.alive = False
        elif self.hp < 0:
            self.hp = 0
            self.conditions.append("downed")
    def heal(self, amount):
        lowAmount = amount - self.tempHp
        self.tempHp -= amount
        self.hp -= lowAmount
        if self.hp > self.maxHp:
            self.hp = self.maxHp
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
