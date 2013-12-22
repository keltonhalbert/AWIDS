#! /usr/bin/env python
# -*- coding: utf-8 -*-

#GUI for AWIDS
#Based on AWIDS.py by Kelton Halbert
#Tkinter GUI by Tarmo Tanilsoo(tarmotanilsoo@gmail.com)

from awids.readmetar import OBSWX
from awids.loadgrids import Grids
from awids.projection import Projection
import datetime
import matplotlib.pyplot as plt
from awids.gridmaker import Gridmaker
from awids.barbs import Plotbarbs
from awids.satellite import get_satellite as sat
import numpy as np
import Tkinter


def code(prod,tunit):
    if prod == "Temperature":
        return "TMP"+tunit
    elif prod == "Dewpoint":
        return "DWP"+tunit
    elif prod == "Wind speed":
        return "WSPD"
    elif prod == "Sea level pressure":
        return "PRES"
    elif prod == "Theta":
        return "THTA"
    elif prod == "Theta-E":
        return "THTE"
    elif prod == "Mixing ratio":
        return "MIXR"
    elif prod == "Relative humidity":
        return "RELH"
    elif prod == "Vorticity":
        return "VORT"
    elif prod == "Divergence":
        return "DIVR"
    elif prod == "Temperature advection":
        return "TP"+tunit+"A"
    elif prod == "Mixing ratio advection":
        return "MXRA"
    elif prod == "Theta-E advection":
        return "THEA"
    elif prod == "Three hour temperature tendency":
        return "3TP"+tunit
    elif prod == "Three hour dewpoint tendency":
        return "3DW"+tunit
    elif prod == "Three hour sea level pressure tendency":
        return "3PRS"
    elif prod == "Three hour Theta tendency":
        return "3THA"
    elif prod == "Three hour Theta-E tendency":
        return "3THE"
    elif prod == "Three hour vorticity tendency":
        return "3VOR"
    elif prod == "Three hour divergence tendency":
        return "3DIV"
    else:
        return None
def tostatus(text): #Updating status
    statustext.config(text=text)
    aken.update()
def startgen():
    fp=filled.get()
    cp=contoured.get()
    if fp == "None" and cp == "None":
        tostatus("Error: No variables selected")
        return -1
    tunit=tempunit.get()
    wstyle=windstyle.get()
    dtype=displaytype.get()
    if dtype == "SINGLE": dtype=site.get()
    stype=sattype.get()
    fcode=code(fp,tunit) #Determine the product code for filled content
    ccode=code(cp,tunit) #Determine the product code for contours
    tostatus("Working...")
    try:
        gmaker = Gridmaker( area=dtype, RoI=250000 )
    except:
        tostatus("Failed to create grid. Is the station code correct?")
        return
    m = gmaker.mproj()
    tostatus("Drawing coastlines...")
    m.drawcoastlines()
    tostatus("Drawing countries...")
    m.drawcountries()
    tostatus("Drawing states...")
    m.drawstates()
    if fp != "None":
        tostatus("Interpolating...")
        if fcode.startswith( '3' ):
            fgrid = gmaker.grid_3hr( datatype=fcode, datdict=data, tenddict=tend )
        elif fcode == 'VORT' or fcode == 'DIVR':
            fgrid = gmaker.VectorGrid( datatype=fcode, datdict=data )
        elif fcode == 'TPFA' or fcode == 'TPCA' or fcode == 'MXRA' or fcode == 'THEA':
            fgrid = gmaker.AdvectionGrid( datatype=fcode, datdict=data )
        else:
            fgrid = gmaker.grid( datatype=fcode, datdict=data )[0]
    if cp != "None":
        tostatus("Interpolating data for contours")
        if fp != cp:
            if ccode.startswith( '3' ):
                cgrid = gmaker.grid_3hr( datatype=ccode, datdict=data, tenddict=tend )
            elif ccode == 'VORT' or ccode == 'DIVR':
                cgrid = gmaker.VectorGrid( datatype=ccode, datdict=data )
            elif ccode == 'TPFA' or ccode == 'TPCA' or ccode == 'MXRA' or ccode == 'THEA':
                cgrid = gmaker.AdvectionGrid( datatype=ccode, datdict=data )
            else:
                cgrid = gmaker.grid( datatype=ccode, datdict=data )[0]
        else: #If wanting contours for same product as 
            cgrid = fgrid
    if dtype == "GOES-E":
        tostatus('Downloading Satellite Data')
        satellite = sat( projection=m, SAT=stype )
        x, y = satellite[0], satellite[1]
        vis = satellite[2]
        tostatus('Plotting Satellite')
        m.pcolormesh( x, y, vis, cmap=plt.get_cmap( 'gist_gray' ) )
        tostatus('Contouring Data')
        CS = m.contourf( grid[0], grid[1], grid[2], grid[3], cmap=grid[4], alpha=.20 )
        tostatus('Finished With Satellite')
    else:
        tostatus("Plotting...")
        if fp != "None":
            CS = m.contourf( fgrid[0], fgrid[1], fgrid[2], fgrid[3], cmap=fgrid[4], extend='both' )
        if cp != "None":
            CS2 = m.contour( cgrid[0], cgrid[1], cgrid[2], cgrid[3], extend='both', linewidths=0.5, colors='#000000')
            plt.clabel(CS2,fmt="%1.1f",fontsize=10,inline=False,linestyles="solid",colors='#000000')
    if wstyle == 'BARB':
        tostatus("Plotting wind barbs...")
        b = Plotbarbs( projection=m, DatDict=data, RoI=250000, area=dtype )
        barbs = b.StnBarbs()
    if wstyle == 'STRM':
        tostatus("Plotting streamlines...")
        b = Plotbarbs( projection=m, DatDict=data, RoI=250000, area=dtype )
        barbs = b.StreamLines(density=3,arrowsize=2,color='#00FFFF',linewidth=1.2)
    if fp !="None": plt.colorbar(CS, orientation='vertical', pad=.01, fraction=.05, shrink=.95)
    if fp !="None" and cp != "None":
        plt.title(fgrid[5] if fgrid[5] == cgrid[5] else fgrid[5]+", "+cgrid[5])
    elif fp == "None":
        plt.title(cgrid[5])
    elif cp == "None":
        plt.title(fgrid[5])
    plt.xlabel(current_time[2:4] + '/' + current_time[4:6] + '/' + current_time[:2] + '    ' + current_time[-2:] + 'Z' + '\n' + bottomtxt.get())
    #plt.savefig(plotvar['PFUNC'] + '_' + plotvar['PAREA'] + '_' + current_time + '.pdf',bbox_inches='tight')
    plt.tight_layout(pad=2.08)
    tostatus("Done")
    plt.show()
    return 0

obs = OBSWX()

## load the current surface data
data = obs.Surface()

## get the time 3 hours ago for tendency plots
current_time = obs.cycle
curtime = datetime.datetime( int( obs.year ), int( obs.month ), int( obs.day ), int( obs.hour ) )
tendency_interval = datetime.timedelta( hours=3 )
three_hours_ago = str( curtime - tendency_interval ).replace( '-', '').replace( ':', '' ).replace( ' ', '' )[2:-4]
## load the tendency data
tend = obs.Surface( cycle=three_hours_ago )

##GUI
aken=Tkinter.Tk()
aken.title("AWIDS GUI")
filled=Tkinter.StringVar(aken)
filled.set("None")
contoured=Tkinter.StringVar(aken)
contoured.set("None")
filledlabel=Tkinter.Label(aken,text="Filled:")
filledlabel.grid(column=0,row=0,sticky="e")
product1=Tkinter.OptionMenu(aken,
                            filled,
                            "None",
                            "Temperature",
                            "Dewpoint",
                            "Wind speed",
                            "Sea level pressure",
                            "Theta",
                            "Theta-E",
                            "Mixing ratio",
                            "Relative humidity",
                            "Vorticity",
                            "Divergence",
                            "Temperature advection",
                            "Mixing ratio advection",
                            "Theta-E advection",
                            "Three hour temperature tendency",
                            "Three hour dewpoint tendency",
                            "Three hour sea level pressure tendency",
                            "Three hour Theta tendency",
                            "Three hour Theta-E tendency",
                            "Three hour vorticity tendency",
                            "Three hour divergence tendency")
product1.config(width=30)
product1.grid(column=1,row=0,columnspan=3,sticky="w")
contouredlabel=Tkinter.Label(aken,text="Contours:")
contouredlabel.grid(column=0,row=1,sticky="e")
product2=Tkinter.OptionMenu(aken,
                            contoured,
                            "None",
                            "Temperature",
                            "Dewpoint",
                            "Wind speed",
                            "Sea level pressure",
                            "Theta",
                            "Theta-E",
                            "Mixing ratio",
                            "Relative humidity",
                            "Vorticity",
                            "Divergence",
                            "Temperature advection",
                            "Mixing ratio advection",
                            "Theta-E advection",
                            "Three hour temperature tendency",
                            "Three hour dewpoint tendency",
                            "Three hour sea level pressure tendency",
                            "Three hour Theta tendency",
                            "Three hour Theta-E tendency",
                            "Three hour vorticity tendency",
                            "Three hour divergence tendency")
product2.config(width=30)
product2.grid(column=1,row=1,columnspan=3,sticky="w")
tunitlabel=Tkinter.Label(aken,text="Temperature/Dewpoint unit:")
tunitlabel.grid(column=0,row=2,sticky="e")
tempunit=Tkinter.StringVar(aken)
tempunit.set("F")
tunit_f=Tkinter.Radiobutton(aken,text="Fahrenheit",variable=tempunit,value="F")
tunit_f.grid(column=1,row=2,sticky="w")
tunit_c=Tkinter.Radiobutton(aken,text="Celsius",variable=tempunit,value="C")
tunit_c.grid(column=3,row=2,sticky="w")
wstylelabel=Tkinter.Label(aken,text="Wind display:")
wstylelabel.grid(column=0,row=3,sticky="e")
windstyle=Tkinter.StringVar(aken)
windstyle.set("None")
wstyle_none=Tkinter.Radiobutton(aken,text="None",variable=windstyle,value="None")
wstyle_none.grid(column=1,row=3,sticky="w")
wstyle_barb=Tkinter.Radiobutton(aken,text="Barbs",variable=windstyle,value="BARB")
wstyle_barb.grid(column=2,row=3,sticky="w")
wstyle_strm=Tkinter.Radiobutton(aken,text="Streamlines",variable=windstyle,value="STRM")
wstyle_strm.grid(column=3,row=3,sticky="w")
displaylabel=Tkinter.Label(aken,text="Display:")
displaylabel.grid(column=0,row=4,sticky="e")
displaytype=Tkinter.StringVar(aken)
displaytype.set("CONUS")
conus=Tkinter.Radiobutton(aken,text="CONUS",variable=displaytype,value="CONUS")
conus.grid(column=1,row=4,sticky="w")
goese=Tkinter.Radiobutton(aken,text="GOES-E",variable=displaytype,value="GOES-E")
goese.grid(column=2,row=4,sticky="w")
singlesite=Tkinter.Frame(aken)
single=Tkinter.Radiobutton(singlesite,variable=displaytype,value="SINGLE")
single.grid(column=0,row=0,sticky="w")
site=Tkinter.Entry(singlesite,width=5)
site.grid(column=1,row=0,sticky="w")
singlesite.grid(column=3,row=4,sticky="w")
sattypelabel=Tkinter.Label(aken,text="Satellite image:")
sattypelabel.grid(column=0,row=5,sticky="e")
sattype=Tkinter.StringVar(aken)
sattype.set("VIS")
sattype1=Tkinter.Radiobutton(aken,text="Visible",variable=sattype,value="VIS")
sattype1.grid(column=1,row=5,sticky="w")
sattype2=Tkinter.Radiobutton(aken,text="Infrared",variable=sattype,value="IR")
sattype2.grid(column=3,row=5,sticky="w")
bottomtextl=Tkinter.Label(aken,text="Bottom text:")
bottomtextl.grid(column=0,row=6,sticky="e")
bottomtxt=Tkinter.StringVar(aken)
bottomtxt.set("Generated using AWIDS")
bottomtextf=Tkinter.Entry(aken,width=30,textvariable=bottomtxt)
bottomtextf.grid(column=1,row=6,columnspan=3)
genbutton=Tkinter.Button(aken,text="Generate map",command=startgen)
genbutton.grid(column=1,row=7,columnspan=2)
statustext=Tkinter.Label(aken,text="")
statustext.grid(column=0,row=8,columnspan=4,sticky="w")
aken.mainloop()
