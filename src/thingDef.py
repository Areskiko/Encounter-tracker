class creature():
    def __init__(self, name, maxHp, speed):
        self.name = name
        self.maxHp = maxHp
        self.hp = maxHp
        self.speed = speed
        self.tempHp = 0

    def rollInitiative(self, roll):
        self.initiative = roll
    
    def takeDamage(self, damage):
        self.hp -= damage
        if self.hp >= self.maxHp:
            self.isDead = True
        elif self.hp < 0:
            self.hp = 0
    
    def Heal(self, amount, temprorary=False):
        if temprorary:
            self.tempHp += amount
        else:
            self.hp += amount
            if self.hp > self.maxHp:
                self.hp = self.maxHp

