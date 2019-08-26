import tkinter as tk
import tools
main = tk.Tk()
creatures = {}


#Display
display = tk.Frame()









#Addition labels and inputs
additions = tk.Frame(main)

tk.Label(additions, text="Name").grid(row=0, column=1)
nameInput = tk.Entry(additions)
nameInput.grid(row=1, column = 1)

tk.Label(additions, text="Speed").grid(row=0, column=2)
speedInput = tk.Entry(additions)
speedInput.grid(row=1, column = 2)

tk.Label(additions, text="Max Hp").grid(row=0, column=3)
maxHpInput = tk.Entry(additions)
maxHpInput.grid(row=1, column = 3)

tk.Label(additions, text="Initiative").grid(row=0, column=4)
initiativeInput = tk.Entry(additions)
initiativeInput.grid(row=1, column = 4)

tk.Label(additions, text="Hp*").grid(row=0, column=5)
hpInput = tk.Entry(additions)
hpInput.grid(row=1, column = 5)

def getInit(e):
    return e.initiative


def newCreature():
    global creatures
    if hpInput.get() == "":
        hp = None
    else:
        hp = int(hpInput.get())
    creatures = tools.addCreature(nameInput.get(), int(speedInput.get()), int(maxHpInput.get()), int(initiativeInput.get()), creatures, hp=hp)
    crList = []
    for key in creatures:
        crList.append(creatures[key])
    crList.sort(key=getInit, reverse=True)
    for child in display.winfo_children():
        child.destroy()
    for creature in crList:
        tk.Label(display, text=creature.name).pack()


addBtn = tk.Button(additions, text="Add Creature", command=newCreature)
addBtn.grid(row=1, column = 0)










additions.pack(side=tk.TOP)
display.pack()
main.mainloop()