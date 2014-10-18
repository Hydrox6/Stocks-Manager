from Tkinter import *
import math as maths



def interpolate(r1,r2,f1,f2,rd):
    """
    Interpolates. Simple as.
    """
    r2 -= r1
    rd -= r1
    r1 -= r1
    pr = float(rd)/float(r2-r1)
    pf = pr*(f2-f1)
    return f1 +pf

def plot(canvas,points,axes,title,mode):
    """
    Takes a Tkinter Canvas, a list of points, relevant titles, and a joining mode, and plots the graph complete with dynamic axes.

    Keyword arguments:
    
    canvas = Tkinter.Canvas
    points = List<List<float>> e.g. [[1.0,2.0],[2.0,3.0]]
    axes = List<String> e.g. ["Distance","Time"]
    title = String e.g. "Graph of Distance versus Time"
    mode type = String, either "join" or "best fit"
    """
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
        posx = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,rawx)
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

    if not len(axes) == 0:
        canvas.create_text(yaxisx,margin-15,text=axes[0],font=("Calibri","12","bold"))
        canvas.create_text(width/2,xaxisy+15,text=axes[1],font=("Calibri","12","bold"),anchor="n")


    if not len(title) == 0: canvas.create_text(width/2,margin/2,text=title,font=("Calibri","14","bold","underline"))

    if mode.lower() == "join":
        for x in range(1,len(points)):
            posx1 = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,points[x][0])
            posy1 = interpolate(maxx["-y"],maxx["+y"],height-margin,margin,points[x][1])
            posx2 = interpolate(maxx["-x"],maxx["+x"],margin,width-margin,points[x-1][0])
            posy2 = interpolate(maxx["-y"],maxx["+y"],height-margin,margin,points[x-1][1])
            canvas.create_line(posx1,posy1,posx2,posy2,width=1.5)

    elif mode.lower() == "best fit":
        ax = 0.0
        ay = 0.0
        for p in points:
            ax += p[0]
            ay += p[1]
        ax = ax/float(len(points))#average of x values
        ay = ay/float(len(points))#average of y values
        xy = 0.0
        xx = 0.0
        yy = 0.0
        for p in points:
            xy += (p[0]-ax)*(p[1]-ay)
            xx += maths.pow((p[0]-ax),2)
            yy += maths.pow((p[1]-ay),2)
        
        r = float(xy)/maths.sqrt(xx*yy)


        x1 = maxx["-x"]
        x2 = maxx["+x"]
        y1 = height-ppy*(r*x1 + (ay-ax*r))
        y2 = height-ppy*(r*x2 + (ay-ax*r))

        x1 = (x1-maxx["-x"])*ppx
        x2 = (x2-maxx["-x"])*ppx
                
        
        canvas.create_line(x1,y1,x2,y2,width=1.5)
            
        
