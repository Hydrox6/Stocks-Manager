from Tkinter import *
import math as maths



def interpolate(r1,r2,f1,f2,rd):
    r2 -= r1
    rd -= r1
    r1 -= r1
    pr = float(rd)/float(r2-r1)
    pf = pr*(f2-f1)
    print r1,r2,rd,pr,pf
    return f1 +pf


def plot(canvas,points,axis,title,mode):
    margin = 40
    height = canvas.winfo_height()
    width = canvas.winfo_width()
    draww = width-margin*2
    drawh = height-margin*2
    maxx = {"+y":0.0,"-y":0.0,"+x":0.0,"-x":0.0}
    for x in points:
        if   x[0] < maxx["-x"]:maxx["-x"] = maths.floor(x[0])
        elif x[0] > maxx["+x"]:maxx["+x"] = maths.ceil(x[0])
        if   x[1] < maxx["-y"]:maxx["-y"] = maths.floor(x[1])
        elif x[1] > maxx["+y"]:maxx["+y"] = maths.ceil(x[1])
    rangex = maxx["+x"]-maxx["-x"]
    rangey = maxx["+y"]-maxx["-y"]
    dpx = rangex/float(width)
    dpy = rangey/float(height)
    ppx = 1/dpx
    ppy = 1/dpy
    fourpx = rangex/25
    fourpy = rangey/25
    xaxisy = height-margin-maxx["-y"]*ppy
    yaxisx = 0+margin-maxx["-x"]*ppx
    canvas.create_line(margin,xaxisy,width-margin,xaxisy,width=2)#x axis
    canvas.create_line(yaxisx,margin,yaxisx,height-margin,width=2)#y axis
    for x in range(0,26):
        #X Axis Markers
        rawx = maxx["-x"]+fourpx*x
        print rawx
        posx = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,rawx)
        print posx
        if not rawx == 0:
            canvas.create_line(posx,xaxisy,posx,xaxisy+3,width=1.5)
            canvas.create_text(posx,xaxisy+10,text=str(rawx))
        #Y Axis Markers
        rawy = maxx["-y"]+fourpy*x
        posy = interpolate(maxx["-y"],maxx["+y"],height-margin,margin,rawy)
        if not rawy == 0:
            canvas.create_line(yaxisx,posy,yaxisx-3,posy,width=1.5)
            canvas.create_text(yaxisx-10,posy,text=str(rawy),anchor="e")
    
    for p in points:
        posx = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,p[0])
        posy = interpolate(maxx["-y"],maxx["+y"],height-margin,margin,p[1])
        canvas.create_line(posx-3,posy-3,posx+3,posy+3,width=1.75)
        canvas.create_line(posx-3,posy+3,posx+3,posy-3,width=1.75)
        canvas.create_oval(posx+3,posy+2,posx+3,posy+2,width=1)#fixes corner pixel
        canvas.create_oval(posx+3,posy-3,posx+3,posy-3,width=1)#fixes corner pixel

    if mode.lower() == "join":
        for x in range(1,len(points)):
            posx1 = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,points[x][0])
            posy1 = interpolate(maxx["-y"],maxx["+y"],height-margin,margin,points[x][1])
            posx2 = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,points[x-1][0])
            posy2 = interpolate(maxx["-y"],maxx["+y"],height-margin,margin,points[x-1][1])
            canvas.create_line(posx1,posy1,posx2,posy2,width=1.5)

    elif mode.lower() == "best fit":pass
        

#test code         
"""
root = Tk()
point = [[-1,0],[1,2],[3,7],[6,2],[10,10]]
c = Canvas(width=800,height=800)
c.pack()
Button(root,text="go",command=lambda:plot(c,point,["x","y"],"Thing","join")).pack()
root.mainloop()
"""
