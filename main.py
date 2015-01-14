# -*- coding: utf-8 -*-
import mtTkinter as Tkinter
from Tkinter import *

import math as maths

from get import get

import os, threading, time

w = 1366
h = 768

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
        if not x >= len(data):
            e = buildEntry(x)
            e.grid(column=0,row=x-top)

def redrawScroll(ev):
    global top
    up = ev.delta > 0
    if len(data) > n:
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
    do = data[:]
    for x in range(0,len(do)):
        o = datad[do[x]]
        extra = get(do[x]).dictify()
        o["Total Price"] = float(extra["Price"])*float(o["Amount"])
        o["Total Price"] = 12762.00
        o.update(extra)
        datad[do[x]] = o
    redraw()
        

def gen():
    #TODO: stub
    print "blarghgen"

def actuallyAdd(t,d):
    global datad,data
    t.destroy()
    nd = {}
    nd["Code"] = d[0].strip().upper()
    nd["Amount"] = d[1].strip()
    extra = get(nd["Code"]).dictify()
    nd["Total Price"] = float(extra["Price"])*float(nd["Amount"])
    nd.update(extra)
    datad[nd["Code"]] = nd
    data.append(nd["Code"])
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
    dre = re.compile("{(.*?)}")
    for x in columns:
        form = x[2]
        final = ""
        eform = form
        while dre.match(eform) != None:
            mat = dre.match(eform)
            final += eform[:mat.start()]
            raw = eform[mat.start():mat.end()][1:-1]
            final += str(d[raw])
            eform = eform[mat.end():]
        l=Label(entry,text=final,font=font,width=cw,relief="groove")
        l.pack(side=LEFT)
        l.bind("<Button-1>",lambda e,i=i: getSide(i))
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

#columns = [["x","n"],["x*x","n"]]
columns = [["Code","a","{Code}"],["Price","n","{Price} {Currency}"],["Amount","n","{Amount}"],["Total Price","n","{Total Price} {Currency}"]]
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
        l.bind("<Button-1>",lambda e,x=x: sortby(x))
        l.pack(side=LEFT)
        
    

def sortby(col):
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
            pivot = l.pop(0)
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
        nd.append(x["Code"])
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

getD = Button(topbar,text="Fetch Data",command=fetch,height=2,width=12)
getD.pack(side=LEFT,anchor="nw")

generate = Button(topbar,text="Generate Report",command=gen,height=2,width=17)
generate.pack(side=LEFT,anchor="nw")

addB = Button(topbar,text="Add Stock",command=add,height=2,width=11)
addB.pack(side=LEFT,anchor="nw")


auto = BooleanVar()
auto.set(False)

def save():
    fl = open("store.csv","w")
    for _,v in datad.iteritems():
        f = v["Code"]+","+v["Amount"]+"\n"
        fl.write(f)
    fl.close()
        

def drawnone():
    countdown.delete(ALL)
    countdown.create_text((20,20),text="Auto")

def drawthing(c):
    countdown.delete(ALL)
    cp = float(c)/1000.0
    countdown.create_arc((5,5,35,35),start=90.0,extent=-cp*360.0,fill="#0080c0",outline="#0080c0",activefill="#40c0ff",activeoutline="#40c0ff")

def autothread():
    current = 1000
    while True:
        if auto.get() == 1:
            current -= 1
            print current
            drawthing(current)
            if current == 0:
                current = 1000
                fetch()
                save()
        else:
            drawnone()
            current = 1000 
        time.sleep(0.1)

countdown = Canvas(topbar,height=40,width=40)
countdown.pack(side=RIGHT,anchor="ne")

countdown.bind("<Button-1>", lambda e: auto.set(not auto.get()))

at = threading.Thread(target=autothread)
at.start()


data = []
datad = {}


root.update_idletasks()

n = int(maths.floor((h-topbar.winfo_height()-25-fh)/float(fh+2)))#23
top = 0

def init():
    if os.path.exists("store.csv"):
        fl = open("store.csv","r")
        r = fl.read().split("\n")[:-1]
        fl.close()
        for x in r:
            d = x.split(",")
            code = d[0]
            dictt = {}
            for y in range(0,len(d)):
                dictt[columns[y*2][0]] = d[y]
            extra = get(code).dictify()
            dictt.update(extra)
            dictt["Total Price"] = float(dictt["Price"])*float(dictt["Amount"])
            datad[code] = dictt
            data.append(code)

init()

sortby(0)
"""
for x in range(0,100):
    d1 = [str(x),str(x*x)]
    d = {}
    for z in range(0,len(d1)):
        d[columns[z][0]] = d1[z]
    datad[str(x)] = d
    data.append(str(x))
"""


"""
for x in range(0,n):
    e = buildEntry(top+x)
    e.grid(row=x,column=
"""
redraw()



root.mainloop()
