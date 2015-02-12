# -*- coding: utf-8 -*-
import mtTkinter as Tkinter
from Tkinter import *

import math as maths

from get import *

import os, time, uuid, threading

w = 1366
h = 768

tw = w/11#120
fh = 27


root = Tk()
root.geometry(str(w)+"x"+str(h))
root.resizable(0,0)

root.title("Stocks Manager")

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


def fetchone(uuid):
    o = datad[uuid]
    cc = o["Currency"]
    extraraw = get(o["Code"])
    extra = extraraw.dictify()
    o["Total Price"] = float(extra["Price"])*float(o["Amount"])
    if not cc == extra["Currency"]:
        extraraw.curconv(cc)
        extra = extraraw.dictify()
    o.update(extra)
    datad[uuid] = o

def fetch():
    do = data[:]
    for x in range(0,len(do)):
        fetchone(do[x])
    redraw()
        

def gen():
    #TODO: stub
    print "blarghgen"

def actuallyAdd(t,d):
    global datad,data
    t.destroy()
    try: float(d[1])
    except ValueError: pass
    else:
        d[1] = int(d[1].strip())
        nd = {}
        nd["Code"] = d[0].strip().upper()
        nd["Amount"] = d[1]
        extra = get(nd["Code"]).dictify()
        nd["Total Price"] = float(extra["Price"])*float(nd["Amount"])
        nd["initPrice"] = extra["Price"]
        nd["initCur"] = extra["Currency"]
        date = time.gmtime()
        nd["buydate"] = str(date[2])+"/"+str(date[1])+"/"+str(date[0])
        nd.update(extra)
        while True:
            ucode = uuid.uuid4()
            if not ucode in data:break
        nd["uuid"] = ucode
        datad[ucode] = nd
        data.append(ucode)
        save()
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
    top.bind_all("<Return>",lambda e:actuallyAdd(top,[e1.get(),e2.get()]))

    

font = ("lucida","14")

selected = -1
currentf = PanedWindow(root,orient=HORIZONTAL)

def colourise(obj,sel):
    widgets = wdata[obj].winfo_children()
    for w in widgets:
        if sel:
            w.config(bg="#55CCFF")
        else:
            w.config(bg="#FFFFFF")
        


def subEdit(top,ev,i):
    new = ev.get().strip()
    top.destroy()
    try: float(new)
    except ValueError: pass
    else:
        new = int(new)
        uu = data[i]
        cud = datad[uu]
        cud["Amount"] = new
        fetchone(uu)
        redraw()
        c = i
        save()
        getSide(c)
        getSide(c)
    
    

def editS(i):
    top = Toplevel()
    l = Label(top,text="Amount:")
    l.grid(column=0,row=0)
    ev = StringVar()
    e = Entry(top,textvariable=ev)
    e.grid(column=1,row=0)
    e.focus_set()
    b = Button(top,text="Submit",command=lambda top=top,ev=ev,i=i: subEdit(top,ev,i))
    b.grid(column=0,row=1,columnspan=2)
    top.bind_all("<Return>",lambda e,top=top,ev=ev,i=i: subEdit(top,ev,i))


def acrem(top,i):
    top.destroy()
    uu = data[i]
    del datad[uu]
    getSide(i)
    data.pop(i)
    wdata.pop(i)
    save()
    redraw()

def remS(i):
    top = Toplevel()
    l = Label(top,text="Are you sure?",width=15,height=3)
    l.grid(row=0,column=0,columnspan=2)
    b1 = Button(top,text="Yes",width=15,height=3,command=lambda top=top,i=i: acrem(top,i))
    b1.grid(row=1,column=0)
    b2 = Button(top,text="No",width=15,height=3,command=top.destroy)
    b2.grid(row=1,column=1)
    top.bind_all("<Return>",lambda e,top=top: top.destroy())

def subConv(top,ev,i):
    to = ev.get().upper()
    top.destroy()
    uu = data[i]
    cud = datad[uu]
    h = Stock(cud)
    h.curconv(to)
    datad[uu] = h.dictify()
    redraw()
    c = i
    getSide(c)
    getSide(c)
    

def convS(i):
    top = Toplevel()
    l = Label(top,text="Convert to:\n(Codes only)",width=15,height=3)
    l.grid(row=0,column=0)
    ev = StringVar()
    e = Entry(top,textvariable=ev)
    e.grid(row=0,column=1)
    e.focus_set()
    b = Button(top,text="Convert",command=lambda top=top,ev=ev,i=i:subConv(top,ev,i))
    b.grid(row=1,column=0,columnspan=2)
    top.bind_all("<Return>",lambda e,top=top,ev=ev,i=i: subConv(top,ev,i))
    
def Pass():pass

root.bind_all("<Delete>",lambda e: Pass())

def getSide(i):
    global selected,currentf
    if selected == i:
        selected = -1
        currentf.destroy()
        currentf = PanedWindow(root,orient=HORIZONTAL)
        colourise(i,False)
        root.bind_all("<Delete>",lambda e: Pass())
    else:
        colourise(selected,False)
        selected = i
        currentf.destroy()
        currentf = PanedWindow(topside,orient=HORIZONTAL)
        currentf.pack()
        dat = datad[data[i]]
        initprice = dat["initPrice"]
        formatted = "Initial Price: {initp}\nNet Change: {ch}".format(initp=initprice,ch=float(datad[data[i]]["Total Price"])-float(initprice)*int(datad[data[i]]["Amount"]))
        
        infol1 = Label(currentf,text=formatted,height=2,relief=RIDGE,padx=5)
        
        infol2 = Label(currentf,text="Bought on: "+datad[data[i]]["buydate"],relief=RIDGE,height=2,padx=5)

        currentf.add(infol2)
        currentf.add(infol1)
        
        #EDIT
        bEdit = Button(currentf,text="Edit Stock",height=2,command=lambda i=i:editS(i))
        currentf.add(bEdit)
        #CONVERT
        bConvert = Button(currentf,text="Convert to Currency",height=2,command=lambda i=i:convS(i))
        currentf.add(bConvert)
        #REMOVE
        bDelete = Button(currentf,text="Remove Stock",height=2,command=lambda i=i:remS(i))
        currentf.add(bDelete)
        root.bind_all("<Delete>",lambda e,i=i: remS(i))
        colourise(i,True)
        

def buildEntry(i):
    d1 = data[i]
    d = datad[d1]
    entry = PanedWindow(main,orient=HORIZONTAL)
    dre = re.compile("{(.*?)}")
    for x in columns:
        form = x[2]
        final = ""
        eform = form
        while dre.search(eform) != None:
            mat = dre.search(eform)
            final += eform[:mat.start()]
            raw = eform[mat.start():mat.end()][1:-1]
            final += str(d[raw])
            eform = eform[mat.end():]
        l=Label(entry,text=final,font=font,width=cw,relief="groove")
        l.pack(side=LEFT)
        l.bind("<Button-1>",lambda e,i=i: getSide(i))
    try:wdata[i] = entry
    except IndexError: wdata.append(entry)
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
mainr.grid(row=1,column=0,columnspan=2)
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
                    shorter = x[selector] if len(x[selector]) < pivot[selector] else pivot[selector]
                    for y in range(0,len(shorter)):                        
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
        nd.append(x["uuid"])
    data = nd
    redraw()
    sort = [col,asc]
    drawcol()

cls = []

drawcol()

c = Canvas(maintop,width=w,height=5,bg="#000000")
c.grid(row=1,column=0,sticky="w")

topbar = Frame(root)
topbar.grid(row=0,column=0,columnspan=1,sticky="nw")

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
        f = v["Code"]+","+str(v["Amount"])+","+v["initPrice"]+","+v["buydate"]+"\n"
        fl.write(f)
    fl.close()
        
"""
def animate(io):
    if io:
        for x in range(0,16):
            countdown.delete(ALL)
            countdown.create_arc((20-x,20-x,20+x,20+x),start=90.0,extent=360.0,fill="#33AADD",outline="#33AADD")
            if x-7 > 0:
                countdown.create_arc((13-x,13-x,13+x,13+x),extent=359,start=0,fill="#aaaaaa",outline="#aaaaaa")
            if x-10 > 0:
                countdown.create_rectangle((10-x,10-x,10+x,10+x),fill="#666666",outline="#666666",activefill="#777777",activeoutline="#777777")
    else:
        for x in range(0,16):
            countdown.delete(ALL)
            countdown.create_arc((5,5,35,35),start=90.0,extent=360.0,fill="#33AADD",outline="#33AADD")
            if x-s[1] > 0:
                countdown.create_arc((12,12,28,28),extent=359,start=0,fill="#aaaaaa",outline="#aaaaaa")
            if x-s[2] > 0:
                countdown.create_rectangle((15,15,25,25),fill="#666666",outline="#666666",activefill="#777777",activeoutline="#777777")
    auto.set(not auto.get())
 """           
    
        

def drawnone():
    countdown.delete(ALL)
    countdown.create_text((20,20),text="Auto")



def drawthing(c):
    countdown.delete(ALL)
    cp = float(c)/1000.0
    countdown.create_arc((5,5,35,35),start=90.0,extent=-cp*360.0,fill="#33AADD",outline="#33AADD")#,fill="#0080c0",outline="#0080c0")
    countdown.create_arc((12,12,28,28),extent=359,start=0,fill="#aaaaaa",outline="#aaaaaa")
    countdown.create_rectangle((15,15,25,25),fill="#666666",outline="#666666",activefill="#777777",activeoutline="#777777")

threadgo = True

def autothread():
    current = 1000
    while threadgo:
        if auto.get() == 1:
            current -= 1
            #print current
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
countdown.pack(side=LEFT,anchor="ne")

countdown.bind("<Button-1>", lambda e: auto.set(not auto.get()))

spacer = Canvas(topbar,height=40,width=0,bg="#000000")

spacer.pack(side=LEFT,anchor="ne")

topside = Frame(root)
topside.grid(column=1,row=0,sticky="ne",padx=25)

at = threading.Thread(target=autothread)
at.daemon = True
at.start()

def stopthepress():
    global threadgo
    threadgo = False
    save()
    time.sleep(0.5)
    root.destroy()

root.wm_protocol("WM_DELETE_WINDOW",stopthepress)


data = []
wdata = []
datad = {}


root.update_idletasks()

n = int(maths.floor((h-topbar.winfo_height()-25-fh)/float(fh+2)))#23
top = 0

def init():
    if os.path.exists("store.csv"):
        fl = open("store.csv","r")
        r = fl.read().split("\n")[:-1]
        fl.close()
        try:
            for x in r:
                d = x.split(",")
                code = d[0]
                dictt = {}
                for y in range(0,2):
                    dictt[columns[y*2][0]] = d[y]
                dictt["initPrice"] = d[2]
                dictt["buydate"] = d[3]
                extra = get(code).dictify()
                dictt.update(extra)
                dictt["Total Price"] = float(dictt["Price"])*float(dictt["Amount"])
                while True:
                    ucode = uuid.uuid4()
                    if not ucode in data:break
                dictt["uuid"] = ucode
                datad[ucode] = dictt
                data.append(ucode)
        except:
            top = Toplevel()
            Label(top,text="The format of store.csv is incorrect.\nData could not be loaded").pack()
            Button(top,text="Ok",command=top.destroy).pack()

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
