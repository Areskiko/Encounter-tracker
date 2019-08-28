import tkinter as tk
import tools
main = tk.Tk()
creatures = {}
crList = []


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
    for i in range(len(crList)):
        tk.Label(display, text=crList[i].name).grid(column=1, row=i)
        tk.Button(display, text="Delete", bg="black", fg="white", command= lambda: tools.removeCreature(crList[i].name, creatures)).grid(column=0, row=i)


addBtn = tk.Button(additions, text="Add Creature", command=newCreature)
addBtn.grid(row=1, column = 0)








def start():
    strtBtn.destroy()
    print(display.winfo_children())
    #display.rowconfigure(0, background="red")
    nxtBtn.pack(side=tk.BOTTOM)

strtBtn = tk.Button(text="Start!", command=start)
strtBtn.pack(side=tk.BOTTOM)
nxtBtn = tk.Button(text="Next")

additions.pack(side=tk.TOP)
display.pack()
main.mainloop()