# -*- coding: utf-8 -*-
from Tkinter import *

import math as maths

w = 1600
h = 900

tw = w/11#120
fh = 27


root = Tk()
root.geometry(str(w)+"x"+str(h))
root.resizable(0,0)

def redraw():
    try:
        for x in main.children.values():
            x.destroy()
    except:pass
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
        if not top == len(data)-n:
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
    global datad,data
    t.destroy()
    datad[d[0].strip()] = d
    data.append(d[0].strip())
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
    e1.focus_set()
    b = Button(top,text="Add",command=lambda:actuallyAdd(top,[e1.get(),e2.get()]))
    b.grid(row=256,column=0,columnspan=2)

    

font = ("lucida","14")

def getSide(i):
    #TODO: stub
    print i

def buildEntry(i):
    d1 = data[i]
    d = datad[d1]
    entry = PanedWindow(main,orient=HORIZONTAL)
    for x in columns:
        l=Label(entry,text=d[x[0]],font=font,width=cw,relief="groove")
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



mainr = Frame(root)
mainr.grid(row=1,column=0)
main = Frame(mainr)
main.grid(row=1,column=0)
root.bind_all("<MouseWheel>",redrawScroll)


maintop = Frame(mainr)
maintop.grid(row=0,column=0)

maintopf = Frame(maintop)
maintopf.grid(row=0,column=0)

columns = [["x","n"],["x*x","n"]]
#      [col,asc] (int,boolean) 
sort = [0,True]
cw = tw/len(columns)

def drawcol():
    try:
        for x in maintopf.children.values():
            x.destroy()
    except:pass
    for x in range(0,len(columns)):
        t = unicode(columns[x][0])
        if x == sort[0]:
            t += u"▲" if sort[1] else u"▼"
        l = Label(maintopf,text=t,font=font,width=cw)
        l.bind("<Button-1>",lambda e: sortby(x))
        l.pack(side=LEFT)
        
    

def sortby(col):
    print col
    global sort, data
    d = datad.values()
    selector = columns[col][0]
    if col == sort[0]:
        asc = not sort[1]
    else:
        asc = True
    
    def swivel(l):
        if len(l) <= 1: return l
        else:
            pivot = l[0]
            l = l[1:]
            high = []
            low = []
            for x in l:
                if columns[col][1] == "n":
                    if float(x[selector]) > float(pivot[selector]):
                        high.append(x)
                    else:
                        low.append(x)
                elif columns[col][1] == "a":
                    for y in range(0,len(x)):
                        if ord(x[selector][y]) > ord(pivot[selector][y]):
                            high.append(x)
                            break
                        elif ord(x[selector][y]) < ord(pivot[selector][y]):
                            low.append(x)
                            break
                    if not x in high and not x in low:
                        low.append(x)
                        
            if not asc:low,high = high[::-1],low[::-1]
            if len(high) <= 1 and len(low) <= 1:
                return low + [pivot] + high
            else:
                return swivel(low)+[pivot]+swivel(high)

    n = swivel(d)
    nd = []
    for x in n:
        nd.append(x["x"])
    data = nd
    redraw()
    sort = [col,asc]
    drawcol()

cls = []

drawcol()

c = Canvas(maintop,width=w,height=5,bg="#000000")
c.grid(row=1,column=0,sticky="w")

topbar = Frame(root)
topbar.grid(row=0,column=0,columnspan=2,sticky="nw")

get = Button(topbar,text="Fetch Data",command=fetch,height=2,width=12)
get.pack(side=LEFT,anchor="nw")

generate = Button(topbar,text="Generate Report",command=gen,height=2,width=17)
generate.pack(side=LEFT,anchor="nw")

addB = Button(topbar,text="Add Stock",command=add,height=2,width=11)
addB.pack(side=LEFT,anchor="nw")


data = []
datad = {}
for x in range(0,100):
    d1 = [str(x),str(x*x)]
    d = {}
    for z in range(0,len(d1)):
        d[columns[z][0]] = d1[z]
    datad[str(x)] = d
    data.append(str(x))


root.update_idletasks()

n = int(maths.floor((h-topbar.winfo_height()-25-fh)/float(fh+2)))#23
top = 0
"""
for x in range(0,n):
    e = buildEntry(top+x)
    e.grid(row=x,column=
"""
redraw()



root.mainloop()
