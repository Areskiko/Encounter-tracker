#region Imports
#region Kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
#endregion Kivy
from backend import *
import thingDef
import inspect
import pickle
#endregion Imports

rootLayout = BoxLayout(orientation="vertical")

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
            if str(arg)=="self":
                pass
            else:
                self.inputLayout.add_widget(argScreen(arg))

        addBtn = Button(text="Add")
        addBtn.bind(on_press=lambda x: self.callback(x))

        swapButton = Button(text="Combat")
        swapButton.bind(on_press=lambda x: self.swap(x))

        self.inputLayout.add_widget(addBtn)
        self.inputLayout.add_widget(swapButton)
        self.layout.add_widget(self.inputLayout)
        self.add_widget(self.layout)


    def callback(self, instance):
        ints = ["maxHp", "hp", "tempHp", "speed", "initiative", "AC"]
        strings = ["name"]
        lists = ["Inventory", "gear", "conditions"]
        dicts = ["stats"]
        args = []
        for argField in self.inputLayout.children:
            if type(argField) == type(Button()):
                pass
            else:
                arg = argField.inputField.text
                _type = argField.inputName.text
                if _type in ints:
                    args.append(int(arg))
                if _type in strings:
                    args.append(str(arg))
                if _type in lists:
                    args.append(arg.split(", "))
                if _type in dicts:
                    statsList = arg.split(", ")
                    args.append({"strength":statsList[0], "dexterity":statsList[1], "constitution":statsList[2], "intelligence":statsList[3], "wisdom":statsList[4], "charisma":statsList[5]})
        args.reverse()
        createCreature(*args)
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
        self.actionArea = BoxLayout(orientation="vertical")
        self.layout.add_widget(self.actionArea)
        self.statArea = BoxLayout(orientation="vertical")
        self.layout.add_widget(self.statArea)





        updateButton = Button(text="Turn")
        updateButton.bind(on_press=lambda x: update())
        self.layout.add_widget(updateButton)

        swapButton = Button(text="Create")
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
        self.orientation="horizontal"
        self.add_widget(Label(text=creature.name))
        self.add_widget(Label(text=f"hp:{creature.hp}/{creature.maxHp}"))
def createCreature(*args):
    addCreature(thingDef.creature(*args))
    print(creatureIndex)
    update()

def save():
    with open("chars.p", "wb") as f:
        pickle.dump([creatureDict, creatureIndex], f)
def load():
    with open("chars.p", "rb") as f:
        dat = pickle.load(f)
    creatureDict.update(dat[0])
    creatureIndex.extend(dat[1])
def trn():
    turn()
    update()

def update():
    sortIndex()
    combat.creatureArea.clear_widgets()
    for creature in creatureIndex:
        combat.creatureArea.add_widget(CreatureField(creatureDict[creature]))


sm = ScreenManager()
combat = CombatScreen(name="combat")
create = CreatorScreen(name="create")
sm.add_widget(create)
sm.add_widget(combat)

class Main(App):
    def build(self):
        return sm

if __name__ == "__main__":
    Main().run()