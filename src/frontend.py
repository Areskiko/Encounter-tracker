import tkinter as tk
from tkinter import ttk
from backend import *
import thingDef
import inspect

root = tk.Tk()
root.title = "DM Toolbox"

tab_parent = ttk.Notebook(root)

creature_creator = ttk.Frame(tab_parent)
creature_viewer = ttk.Frame(tab_parent)
combat_viewer = ttk.Frame(tab_parent)

###REATURE CREATOR
class inputField():
    def __init__(self, arg, nr):
        self.frame = inputFrame
        self.attrLabel = ttk.Label(self.frame, text=str(arg).lower().capitalize())
        self.attrLabel.grid(row=nr, column=0)

        self.attrInput = ttk.Entry(self.frame)
        self.attrInput.delete(0, tk.END)
        self.attrInput.grid(row=nr, column=1)

inputFrame = ttk.Frame(creature_creator)
inputList = []
#Generate Input Fields
for arg, nr in zip(inspect.getfullargspec(thingDef.creature.__init__)[0], range(len(inspect.getfullargspec(thingDef.creature.__init__)[0])-1)):
    if str(arg)=="self":
        pass
    else:
        inputList.append(inputField(arg, nr))

def createCreature():
    ints = ["Maxhp", "Hp", "Temphp", "Speed", "Initiative", "Ac"]
    strings = ["Name"]
    lists = ["Inventory", "Gear", "Conditions"]
    dicts = ["Stats"]
    try:
        args = []
        for argField in inputList:
            arg = argField.attrInput.get()
            if argField.attrLabel.cget("text") in ints:
                args.append(int(arg))
            elif argField.attrLabel.cget("text") in strings:
                args.append(str(arg))
            elif argField.attrLabel.cget("text") in lists:
                args.append(arg.split(", "))
            elif argField.attrLabel.cget("text") in dicts:
                statsList = arg.split(", ")
                args.append({"strength":statsList[0], "dexterity":statsList[1], "constitution":statsList[2], "intelligence":statsList[3], "wisdom":statsList[4], "charisma":statsList[5]})
            else:
                print("Error")
        addCreature(thingDef.creature(*args))
    except Exception as e:
        print(e)
    print(creatureIndex)
    update()

addBtn = ttk.Button(inputFrame, text="Add!", command=createCreature)
addBtn.grid(row=11, column=0)



inputFrame.pack()
###CREATURE VIEWER



###COMBAT VIEWER
s = ttk.Style()
s.configure("green.TLabel", background="green", font=('Helvetica', 12))
s.configure("orange.TLabel", background="orange", font=('Helvetica', 12))
s.configure("red.TLabel", background="red", font=('Helvetica', 12))
s.configure("blue.TLabel", foreground="blue", font=('Helvetica', 16))
s.configure("txt.TLabel", font=("Helvetica", 12))
s.configure("dead.TLabel", font=("Helvetica", 12, "overstrike"))
class creatureFrame():
    def __init__(self, creature, i):
        self.creature = creature
        self.frame = orderList#ttk.Frame(orderList)

        if self.creature.hp > self.creature.maxHp * 2/3:
            style = "green.TLabel"
            

        elif self.creature.hp < self.creature.maxHp * 1/3:
            style = "red.TLabel"

        else:
            style = "orange.TLabel"
        
        self.hpLabel = ttk.Label(self.frame, text=f"{creature.hp}hp", style=style)
        
        if self.creature.alive:
            style="txt.TLabel"
        else:
            style="dead.TLabel"

        self.nameLabel = ttk.Label(self.frame, text=str(creature.name), style=style)
        self.acLabel = ttk.Label(self.frame, text=f"AC:{self.creature.AC}", style="txt.TLabel")

        if self.creature.isActive:
            self.act = ttk.Label(self.frame, text="*", style="blue.TLabel")
            self.act.grid(row=i, column=5)
        
        self.nameLabel.grid(row=i, column=0, sticky=tk.W)
        self.hpLabel.grid(row=i, column=3, sticky=tk.E)
        self.acLabel.grid(row=i, column=2, sticky=tk.E)
        self.delete = ttk.Button(self.frame, text="x", width="2", command= lambda: deleteChar(self.creature.name))
        self.delete.grid(row=i, column=4)
        tk.Label(self.frame, text=" ").grid(row=i, column=1)
        self.frame.pack()


orderList = ttk.Frame(combat_viewer)
frem = ttk.Frame(combat_viewer)
orderList.pack()
frem.pack()
creatureFrames = []

def trn():
    turn()
    update()
nextButton = ttk.Button(combat_viewer, text="Next!", command=trn)
nextButton.pack()



class infoFrame():
    def __init__(self, creature):
        self.frame = frem
        self.creature = creature
        ttk.Label(self.frame, text="Info").grid(row=0, column=2, columnspan=2, sticky=tk.N)
        ttk.Label(self.frame, text=f"Strength:{self.creature.stats['strength']}").grid(sticky=tk.W, row=1, column=0)
        ttk.Label(self.frame, text=f"Dexterity:{self.creature.stats['dexterity']}").grid(sticky=tk.W, row=1, column=1)
        ttk.Label(self.frame, text=f"Constitution:{self.creature.stats['constitution']}").grid(sticky=tk.W, row=1, column=2)
        ttk.Label(self.frame, text=f"Intelligence:{self.creature.stats['intelligence']}").grid(sticky=tk.W, row=1, column=3)
        ttk.Label(self.frame, text=f"Wisdom:{self.creature.stats['wisdom']}").grid(sticky=tk.W, row=1, column=4)
        ttk.Label(self.frame, text=f"Charisma:{self.creature.stats['charisma']}").grid(sticky=tk.W, row=1, column=5)

        ttk.Label(self.frame, text=f"Hp:{self.creature.hp}").grid(sticky=tk.W, row=2, column=0)
        ttk.Label(self.frame, text=f"Max:{self.creature.maxHp}").grid(sticky=tk.W, row=2, column=1)
        ttk.Label(self.frame, text=f"Temp:{self.creature.tempHp}").grid(sticky=tk.W, row=2, column=2)
        ttk.Label(self.frame, text=f"Speed:{self.creature.speed}").grid(sticky=tk.W, row=2, column=3)

        self.invFrame = ttk.Frame(self.frame)
        self.gearFrame = ttk.Frame(self.frame)
        self.condFrame = ttk.Frame(self.frame)
        for thing in self.creature.gear:
            ttk.Label(self.gearFrame, text=str(thing)).pack(side=tk.LEFT)
        for thing in self.creature.inventory:
            ttk.Label(self.invFrame, text=str(thing)).pack(side=tk.LEFT)
        for thing in self.creature.conditions:
            ttk.Label(self.condFrame, text=str(thing)).pack(side=tk.LEFT)

        ttk.Label(self.frame, text="Gear").grid(row=3, column=2, columnspan=2, sticky=tk.N)
        self.gearFrame.grid(row=4, column=0, columnspan=6, rowspan=6)
        ttk.Label(self.frame, text="Inventory").grid(row=10, column=2, columnspan=2, sticky=tk.N)
        self.invFrame.grid(row=11, column=0, columnspan=6, rowspan=6)
        ttk.Label(self.frame, text="Conditions").grid(row=17, column=2, columnspan=2, sticky=tk.N)
        
        self.frame.pack()

def setUpViewer():
    for child in orderList.winfo_children():
        child.destroy()
    for child in frem.winfo_children():
        child.destroy()
    for creature, i in zip(creatureIndex, range(len(creatureIndex))):
        creatureFrames.append(creatureFrame(creatureDict[creature], i))
        if creatureDict[creature].isActive:
            infoFrame(creatureDict[creature])

def update():
    sortIndex()
    setUpViewer()







tab_parent.add(combat_viewer, text="Combat")
tab_parent.add(creature_creator, text="Create Creature")
tab_parent.add(creature_viewer, text="View Creature")
tab_parent.pack()
update()
root.mainloop()