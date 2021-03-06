# pylint: disable=unused-import
# pylint: disable=unused-argument

#region Imports
#region Kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
#endregion Kivy
from backend import *
import thingDef
import inspect
import pickle
import re
#endregion Imports

#rootLayout = BoxLayout(orientation="vertical")
errorPopup = Popup(title="Error", size_hint=(0.5, 0.5))

class argScreen(Screen):
    def __init__(self, argument, **kwargs):
        """Initializes the screen"""
        super(argScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation="horizontal")
        self.inputName = Label(text=argument)
        layout.add_widget(self.inputName)
        self.inputField = TextInput(multiline=False)
        layout.add_widget(self.inputField)
        self.add_widget(layout)

class CreatorScreen(Screen):
    def __init__(self, **kwargs):
        """Initializes the screen"""
        super(CreatorScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")

        #Generate Input Fields
        self.inputLayout = BoxLayout(orientation="vertical")
        inputList = []
        for arg, nr in zip(inspect.getfullargspec(thingDef.creature.__init__)[0], range(len(inspect.getfullargspec(thingDef.creature.__init__)[0])-1)):
            if str(arg) in ["self", "inventory", "gear"]:
                pass
            elif str(arg) == "stats":
                arg = "Stats (Str, Dex, Con, Int, Wis, Cha)"
                self.inputLayout.add_widget(argScreen(arg))
            else:
                self.inputLayout.add_widget(argScreen(str(arg).capitalize()))

        addBtn = Button(text="Add")
        addBtn.bind(on_press=lambda x: self.callback(x))

        swapButton = Button(text="Combat", size_hint=(1, 0.8))
        swapButton.bind(on_press=lambda x: self.swap(x))

        self.inputLayout.add_widget(addBtn)
        self.inputLayout.add_widget(swapButton)
        self.layout.add_widget(self.inputLayout)
        self.add_widget(self.layout)


    def callback(self, instance):
        try:
            ints = ["Maxhp", "Hp", "Temphp", "Speed", "Initiative", "Ac"]
            strings = ["Name"]
            lists = ["Inventory", "Gear", "Conditions"]
            dicts = ["Stats (Str, Dex, Con, Int, Wis, Cha)"]
            args = []
            for argField in self.inputLayout.children:
                if type(argField) == type(Button()):
                    pass
                else:
                    arg = argField.inputField.text
                    _type = argField.inputName.text
                    if _type in ints:
                        if arg == "":
                            arg = 1
                        args.append(int(arg))
                    if _type in strings:
                        args.append(str(arg))
                    if _type in lists:
                        args.append(arg.split(", "))
                    if _type in dicts:
                        statsList = arg.split(", ")
                        try:
                            args.append({"strength":statsList[0], "dexterity":statsList[1], "constitution":statsList[2], "intelligence":statsList[3], "wisdom":statsList[4], "charisma":statsList[5]})
                        except IndexError:
                            args.append({"strength":10, "dexterity":10, "constitution":10, "intelligence":10, "wisdom":10, "charisma":10})
            args.reverse()
            createCreature(*args)
        except Exception as e:
            errorhandling(e)
    def swap(self, instance):
        sm.transition.direction = "left"
        sm.current = "combat"

class CombatScreen(Screen):
    def __init__(self, **kwargs):
        """Initializes the screen"""
        super(CombatScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation="vertical")
        self.creatureArea = BoxLayout(orientation="vertical")
        self.layout.add_widget(self.creatureArea)
        self.actionArea = ActionField()
        self.layout.add_widget(self.actionArea)
        self.statArea = BoxLayout(orientation="vertical")
        self.layout.add_widget(self.statArea)

        updateButton = Button(text="Turn", size_hint=(1,0.2))
        updateButton.bind(on_press=lambda x: trn())
        self.layout.add_widget(updateButton)

        self.saveBox = BoxLayout(size_hint=(1, 0.2))
        self.fileName = TextInput(text="chars")
        self.saveBox.add_widget(self.fileName)

        self.saveLoad = BoxLayout(orientation="horizontal")
        self.save = Button(text="Save")
        self.save.bind(on_press=lambda x: save(self.fileName.text))
        self.saveLoad.add_widget(self.save)

        self.load = Button(text="Load")
        self.load.bind(on_press=lambda x: load(self.fileName.text))
        self.saveLoad.add_widget(self.load)
        self.saveBox.add_widget(self.saveLoad)
        self.layout.add_widget(self.saveBox)

        swapButton = Button(text="Create", size_hint=(1,0.2))
        swapButton.bind(on_press=lambda x: self.swap(x))

        self.layout.add_widget(swapButton)
        self.add_widget(self.layout)


    def swap(self, instance):
        sm.transition.direction = "right"
        sm.current = "create"   
       
class CreatureField(BoxLayout):
    def __init__(self, creature, **kwargs):
        """Initializes the Layout"""
        super(CreatureField, self).__init__(**kwargs)
        self.creature = creature
        self.orientation="horizontal"
        nColor = [1, 1, 1, 1]
        if creature.isActive:
            nColor = [0.8, 0.67, 0, 1]
        if self.creature.alive:
            name = self.creature.name
        else:
            name = f"[s]{self.creature.name}[/s]"
        self.add_widget(Label(text=name, color=nColor, markup=True))
        rate = self.creature.hp/self.creature.maxHp
        if rate < 0.3:
            hColor = [1, 0, 0, 1]
        elif rate < 0.6:
            hColor = [1, 1, 0, 1]
        else:
            hColor = [0, 1, 0, 1]
        self.add_widget(Label(text=f"hp:{self.creature.hp}/{self.creature.maxHp}", color=hColor))
        self.add_widget(Label(text=f"tmp:{self.creature.tempHp}"))
        self.add_widget(Label(text=f"Ac:{self.creature.AC}"))
        delButton = Button(text="[X]", background_color = [0, 0, 0, 0])
        delButton.bind(on_press=lambda x: self.delete(x))
        self.add_widget(delButton)
    
    def delete(self, instance):
        deleteChar(self.creature.name)
        update()

class ActionField(BoxLayout):
    def __init__(self, **kwargs):
        """Initializes the Layout"""
        super(ActionField, self).__init__(**kwargs)
        self.orientation="horizontal"
        self.size_hint = (1, 0.3)
        self.action = Spinner(
            text="Action",
            values=("Damage", "Heal", "Give Temp Hp", "Remove Temp Hp", "Set Initiative")
        )
        self.add_widget(self.action)

        self.target = Spinner(
            text="Target",
            values=[creature for creature in creatureIndex]
        )
        self.add_widget(self.target)

        self.amount = TextInput()
        self.add_widget(self.amount)

        self.do = Button(text="Do!")
        self.do.bind(on_press=self.doIt)
        self.add_widget(self.do)

    def doIt(self, instance):
        try:
            action = self.action.text
            creature = creatureDict[self.target.text]
            if action == "Damage":
                creature.takeDamage(eval(self.amount.text))
            elif action == "Heal":
                creature.heal(eval(self.amount.text))
            elif action == "Give Temp Hp":
                creature.addTempHp(eval(self.amount.text))
            elif action == "Remove Temp Hp":
                creature.removeTempHp()
            elif action == "Set Initiative":
                creature.setInitiative(eval(self.amount.text))
            update()
        except Exception as e:
            errorhandling(e)

class InfoField(GridLayout):
    def __init__(self, creature, **kwargs):
        """Initializes the Layout"""
        super(InfoField, self).__init__(**kwargs)
        self.creature = creature
        self.cols=3
        self.rows=3

        #Stats
        self.add_widget(Label(text=f"Strength:{creature.stats['strength']}"))
        self.add_widget(Label(text=f"Dexterity:{creature.stats['dexterity']}"))
        self.add_widget(Label(text=f"Constitution:{creature.stats['constitution']}"))
        self.add_widget(Label(text=f"Intelligence:{creature.stats['intelligence']}"))
        self.add_widget(Label(text=f"Wisdom:{creature.stats['wisdom']}"))
        self.add_widget(Label(text=f"Charisma:{creature.stats['charisma']}"))

        #Misc
        self.add_widget(Label(text=f"AC:{creature.AC}"))
        self.add_widget(Label(text=f"Speed:{creature.speed}"))

class ErrorScreen(Screen):
    def __init__(self, **kwargs):
        """Initializes the screen"""
        super(ErrorScreen, self).__init__(**kwargs)
        errorPopup.bind(on_dismiss=self.swap)
        self.bind(on_enter=self.disp)
    def swap(self, instance):
        sm.transition.direction = "down"
        sm.current = "create"
    def disp(self, instance):
        errorPopup.open()

def createCreature(*args):
    def createAndDismiss(popup, newName):
        newArgs = [newName, *args[1:]]
        addCreature(thingDef.creature(*newArgs))
        popup.dismiss()
        update()

    if addCreature(thingDef.creature(*args)) == 0:
        update()
    else:
        regex = re.search("(\D*?)([0-9]+)", args[0])
        if regex:
            pass
            names = [name for name in creatureIndex if regex.group(1) in name]
            #r = re.compile("\D*[0-9]+")
            #matchList = list(filter(r.match, names))
            nr = int(regex.group(2)) + 1
            newName = regex.group(1) + str(nr)
            while newName in names:
                newName = regex.group(1) + str(nr)
                nr += 1
        else:
            pass
            names = [name for name in creatureIndex if args[0] in name]
            newName = args[0] + str(len(names))

        content = BoxLayout(orientation="vertical")
        alert = Popup(title="Creature allready exists", content=content, size_hint=(0.5, 0.5), auto_dismiss=False)
        content.add_widget(Label(text=f"There is allready a creature named {args[0]}\nDo you want to name it {newName} instead?"))
        content.add_widget(Button(text="Yes", on_press= lambda x: createAndDismiss(alert, newName)))
        content.add_widget(Button(text="No", on_press=alert.dismiss))
        alert.open()


  
def trn():
    turn()
    update()
def save(fileName):
    with open(fileName+".p", "wb") as f:
        pickle.dump([creatureDict, creatureIndex], f)
def load(fileName):
    try:
        with open(fileName+".p", "rb") as f:
            dat = pickle.load(f)
        for d0 in dat[0]:
            if d0 in creatureIndex:
                pass
            else:
                temp = {d0:dat[0][d0]}
                creatureDict.update(temp)
                creatureIndex.append(d0)
        update()
    except:
        pass
  
def update():
    sortIndex()
    combat.creatureArea.clear_widgets()
    for creature in creatureIndex:
        combat.creatureArea.add_widget(CreatureField(creatureDict[creature]))
    combat.statArea.clear_widgets()
    for creature, i in zip(creatureIndex, range(len(creatureIndex))):
        if creatureDict[creature].isActive:
            combat.statArea.add_widget(InfoField(creatureDict[creature]))

    combat.actionArea.target.values=[creature for creature in creatureIndex]

sm = ScreenManager()
dur = sm.transition.duration
combat = CombatScreen(name="combat")
create = CreatorScreen(name="create")
sm.add_widget(create)
sm.add_widget(combat)
sm.add_widget(ErrorScreen(name="error"))

def errorhandling(e):
        errorPopup.content=Label(text=str(e))
        sm.transition.direction = "up"
        sm.current = "error"
class Main(App):
    def build(self):
        return sm
        

if __name__ == "__main__":
    Main().run()
