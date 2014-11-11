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

def redrawScroll(ev):
    global top
    up = ev.delta > 0
    if up:
        if not top == 0:
            top -= 1
            v = main.children.keys()
            d = main.children
            new = [None for x in range(0,n)]
            for x in range(0,len(v)):
                e = d[v[x]]
                if e.grid_info()["row"] == str(len(v)-1):
                    e.destroy()
                else:
                    new[int(e.grid_info()["row"])+1] = e
            for x in range(1,len(new)):
                e = new[x]
                e.grid(column=0,row=x)
            e = buildEntry(top)
            e.grid(column=0,row=0)
    else:
        if not top == len(data)-1-n:
            top += 1
            v = main.children.keys()
            d = main.children
            new = [None for x in range(0,n)]
            for x in range(0,len(v)):
                e = d[v[x]]
                if e.grid_info()["row"] == "0":
                    e.destroy()
                else:
                    new[int(e.grid_info()["row"])-1] = e
            for x in range(0,len(new)-1):
                e = new[x]
                e.grid(column=0,row=x)
            e = buildEntry(top+n-1)
            e.grid(column=0,row=n-1)

def fetch():
    #TODO: stub
    print "blargh"

def gen():
    #TODO: stub
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
    #TODO: stub
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
root.bind_all("<MouseWheel>",redrawScroll)

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


n = 23
top = 0

for x in range(0,n):
    e = buildEntry(top+x)
    e.grid(row=x,column=0)

    

topbar = Frame(root)
topbar.grid(row=0,column=0,columnspan=2,sticky="nw")

get = Button(topbar,text="Fetch Data",command=fetch,height=2,width=12)
get.pack(side=LEFT,anchor="nw")

generate = Button(topbar,text="Generate Report",command=gen,height=2,width=17)
generate.pack(side=LEFT,anchor="nw")

addB = Button(topbar,text="Add Stock",command=add,height=2,width=11)
addB.pack(side=LEFT,anchor="nw")



root.mainloop()
