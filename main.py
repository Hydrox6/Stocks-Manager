from Tkinter import *

root = Tk()

def buildEntry(i):
    d = data[i]
    entry = PanedWindow(main,orient=HORIZONTAL)
    for x in d:
        Label(entry,text=x).pack(side=LEFT)
    return entry

def mainscroll(e):
    global top,ids
    up = e.delta > 0
    if up:
        if not top == 0:
            i = ids
            for x in range(0,n):
                ids[x].destroy()
            top -= 1
            i.insert(0,"")
            for x in range(top,top+n):
                e = buildEntry(x)
                e.pack()
                i[x-top] = e
            ids = i
    if not up:
        if not top+n == len(data):
            i = ids
            for x in range(0,n):
                ids[x].destroy()
            top += 1
            i.insert(-1,"")
            for x in range(top,top+n):
                e = buildEntry(x)
                e.pack()
                i[x-top] = e
            ids = i
                
        

main = Frame(root,height=800,width=800)
main.pack()
root.bind_all("<MouseWheel>",mainscroll)

data = []
for x in range(0,25):
    for y in range(0,25):
        d = [str(x),str(y)]
        data.append(d)

ids = []

n = 5
top = 0

for x in range(top,top+n):
    e = buildEntry(x)
    e.pack()
    ids.append(e)

for x in range(0,n):
    ids[x].pack()
    


root.mainloop()
