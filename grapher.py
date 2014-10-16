from Tkinter import *
import math as maths




def plot(canvas,points,axis,title,mode):
    height = winfo_height()
    width = winfo_width()
    draww = width-20
    drawh = height-20
    maxx = {"+y":0.0,"-y":0.0,"+x":0.0,"-x":0.0}
    for x in points:
        if   x[0] < maxx["-x"]:maxx["-x"] = maths.floor(x[0])
        elif x[0] > maxx["+x"]:maxx["+x"] = maths.ceil(x[0])
        elif x[1] < maxx["-y"]:maxx["-y"] = maths.floor(x[1])
        elif x[1] > maxx["+y"]:maxx["+y"] = maths.ceil(x[1])
    rangex = maxx["+x"]-maxx["-x"]
    rangey = maxx["+y"]-maxx["-y"]
    dpx = rangex/float(width)
    dpy = rangey/float(height)
    ppx = 1/dpx
    ppy = 1/dpy
    fourpx = rangex*0.04
    fourpy = rangey*0.04
    xaxisy = maxx["+y"]-maxx["+y"]/dpy
    yaxisx = maxx["+x"]-maxx["+x"]/dpx
    canvas.create_line(10,xaxisy,width-10,xaxisy)#x axis
    canvas.create_line(yaxisx,10,yaxisx,height-10)#y axis
    for x in range(0,26):
        posx = maxx["-x"]+fourpx*x
        if not posx == 0:
            canvas.create_line(posx,yaxisx,posx,yaxisx-3)
            #text
        posy = maxx["-y"]+fourpy*x
        if not posy == 0:
            canvas.create_line(xaxisy,posy,xaxisy-3,posy)
            #text
