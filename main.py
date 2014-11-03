from Tkinter import *

import math as maths

w = 1366
h = 768

tw = 120

root = Tk()
root.geometry(str(w)+"x"+str(h))
root.resizable(0,0)

def fetch():
    print "blargh"

def gen():
    print "blarghgen"

font = ("lucida","14")

def buildEntry(i):
    d = data[i]
    entry = PanedWindow(main,orient=HORIZONTAL)
    for x in d:
        Label(entry,text=x,font=font,width=cw,relief="groove").pack(side=LEFT)
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



root.mainloop()
