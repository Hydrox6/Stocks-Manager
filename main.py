from Tkinter import *

import math as maths

w = 1366
h = 768

tw = 120

root = Tk()
root.geometry(str(w)+"x"+str(h))
root.resizable(0,0)

def redraw():
    for x in main.children.values():
        x.destroy()
    for x in range(top,top+n):
        e = buildEntry(x)
        e.grid(column=0,row=x-top)

def redrawScroll(up):
    if up:
        v = main.children.values()
        for x in range(0,len(v)):
            if x == 0:
                v[x].destroy()
            else:
                v[x].grid(column=0,row=x-1)

def fetch():
    print "blargh"

def gen():
    print "blarghgen"

def actuallyAdd(t,d):
    t.destroy()
    redraw()
    

def add():
    top = Toplevel()
    top.title("Add a share")

    v1 = StringVar()
    v2 = StringVar()
    
    
    l1 = Label(top,text="Code")
    l1.grid(row=0,column=0)
    e1 = Entry(top,textvar=v1,width=30)
    e1.grid(row=0,column=1)

    l2 = Label(top,text="Amount")
    l2.grid(row=1,column=0)
    e2 = Entry(top,textvar=v2,width=30)
    e2.grid(row=1,column=1)

    b = Button(top,text="Add",command=lambda:actuallyAdd(top,[e1.get(),e2.get()]))
    b.grid(row=256,column=0,columnspan=2)

    

font = ("lucida","14")

def getSide(i):
    print i

def buildEntry(i):
    d = data[i]
    entry = PanedWindow(main,orient=HORIZONTAL)
    for x in d:
        l=Label(entry,text=x,font=font,width=cw,relief="groove")
        l.pack(side=LEFT)
        l.bind("<Button-1>",lambda e: getSide(i))
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



mainr = Frame(root,height=800,width=800)
mainr.grid(row=1,column=0)
main = Frame(mainr)
main.grid(row=1,column=0)
root.bind_all("<MouseWheel>",mainscroll)

maintop = Frame(mainr)
maintop.grid(row=0,column=0)

maintopf = Frame(maintop)
maintopf.grid(row=0,column=0)

columns = ["x","y","x+y","x*y","x-y"]
cw = tw/len(columns)
for x in columns:
    Label(maintopf,text=x,font=font,width=cw).pack(side=LEFT)

c = Canvas(maintop,width=w,height=5,bg="#000000")
c.grid(row=1,column=0)


data = []
for x in range(0,25):
    for y in range(0,25):
        d = [str(x),str(y),str(x+y),str(x*y),str(x-y)]
        data.append(d)

ids = []

n = 23
top = 0

for x in range(top,top+n):
    e = buildEntry(x)
    e.pack()
    ids.append(e)

for x in range(0,n):
    ids[x].pack()
    

topbar = Frame(root)
topbar.grid(row=0,column=0,columnspan=2,sticky="nw")

get = Button(topbar,text="Fetch Data",command=fetch,height=2,width=12)
get.pack(side=LEFT,anchor="nw")

generate = Button(topbar,text="Generate Report",command=gen,height=2,width=17)
generate.pack(side=LEFT,anchor="nw")

addB = Button(topbar,text="Add Stock",command=add,height=2,width=11)
addB.pack(side=LEFT,anchor="nw")



root.mainloop()
