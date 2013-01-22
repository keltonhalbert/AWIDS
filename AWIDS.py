#! /usr/bin/env python

from awids.readmetar import OBSWX
from awids.loadgrids import Grids
from awids.projection import Projection
import datetime
import matplotlib.pyplot as plt
from awids.gridmaker import Gridmaker
from awids.barbs import Plotbarbs
from awids.satellite import get_satellite as sat
import numpy as np

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

## Lists/Dictionaries for plotting functions
syntax = []
plotvar = { 'PAREA': 'CONUS', 'SAT': 'VIS', 'PFUNC': 'TMPF', 'WIND': 'BARB' }
uservars = []
print 'Plot Variables:\n  PAREA = \n  SAT = \n  PFUNC = \n  WIND = \ntype "exit" to exit\ntype "run" or "r" to run'
## while loop that serves as command line UI
while True:
  plt.close()
  while True:
    vars = raw_input('==> ')
    if vars.upper() == 'R' or vars.upper() == 'RUN' or vars.upper() == 'EXIT':
      break
    else:
      syntax.append( vars.upper() )
      plt.close()
  if vars.upper() == 'EXIT':
    break
  else:
    for d in syntax:
      newlist = d.split( '=' )
      plotvar[ newlist[0].strip(' ') ] = newlist[1].strip(' ')
  ## Draw the map
  print plotvar['PFUNC']
  gmaker = Gridmaker( area=plotvar[ 'PAREA' ], RoI=250000 )
  m = gmaker.mproj()
  m.drawcoastlines()
  m.drawcountries()
  m.drawstates()
  ## Contour the data grids
  if plotvar[ 'PFUNC' ].startswith( '3' ):
    grid = gmaker.grid_3hr( datatype=plotvar[ 'PFUNC' ], datdict=data, tenddict=tend )
  elif plotvar[ 'PFUNC' ] == 'VORT' or plotvar[ 'PFUNC' ] == 'DIVR':
    grid = gmaker.VectorGrid( datatype=plotvar[ 'PFUNC' ], datdict=data )
  elif plotvar[ 'PFUNC' ] == 'TPFA' or plotvar[ 'PFUNC' ] == 'TPCA' or plotvar[ 'PFUNC' ] == 'MXRA' or plotvar[ 'PFUNC' ] == 'THEA':
    grid = gmaker.AdvectionGrid( datatype=plotvar[ 'PFUNC' ], datdict=data )
  else:
    grid = gmaker.grid( datatype=plotvar[ 'PFUNC' ], datdict=data )
  if plotvar[ 'PAREA' ] == 'GOES-E':
    print 'Downloading Satellite Data'
    satellite = sat( projection=m, SAT=plotvar['SAT'] )
    x, y = satellite[0], satellite[1]
    vis = satellite[2]
    print 'Plotting Satellite'
    m.pcolormesh( x, y, vis, cmap=plt.get_cmap( 'gist_gray' ) )
    print 'Contouring Data'
    CS = m.contourf( grid[0], grid[1], grid[2], grid[3], cmap=grid[4], alpha=.20 )
    print 'Finished With Satellite'
  else:
    CS = m.contourf( grid[0], grid[1], grid[2], grid[3], cmap=grid[4], extend='both' )
  ## Plot the wind barbs
  #  if plotvar['WIND'] == 'GRID':
  #    barbplot = b.PlotBarbs( area=plotvar['PAREA'], DatDict=data )
  #    barb = barbplot.GridBarbs()
  if plotvar['WIND'] == 'BARB':
    b = Plotbarbs( projection=m, DatDict=data, RoI=250000, area=plotvar[ 'PAREA' ] )
    barbs = b.StnBarbs()
  if plotvar['WIND'] == 'STRM':
    b = Plotbarbs( projection=m, DatDict=data, RoI=250000, area=plotvar[ 'PAREA' ] )
    barbs = b.StreamLines(density=3,arrowsize=2,color='#00FFFF',linewidth=1.2)
  plt.colorbar(CS, orientation='vertical', pad=.01, fraction=.05, shrink=.95)
  plt.title(grid[5])
  plt.xlabel(current_time[2:4] + '/' + current_time[4:6] + '/' + current_time[:2] + '    ' + current_time[-2:] + 'Z' + '\n' + '(C) awids')
  #plt.savefig(plotvar['PFUNC'] + '_' + plotvar['PAREA'] + '_' + current_time + '.pdf',bbox_inches='tight')
  plt.tight_layout(pad=2.08)
  plt.show()