#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

"""
  solver.kinematic_solver -- Howard Bluestein's method of solving for 
  the kinematic field using triangulation rather than the finite
  difference method.
  
  solver.triangulate -- preforms a Delaunay triangulation on
  the Oklahoma Mesonet
"""

import numpy as np
from Projection import Projection as P
import matplotlib.delaunay as md
import os

def kinematic_solver( u1,u2,u3, v1,v2,v3, x1,x2,x3, y1,y2,y3 ):
  U = np.array ( [ [u1],
                   [v1],
                   [u2],
                   [v2],
                   [u3],
                   [v3] ] )
  Xm = np.array( [ [2, 0, x1, -y1, x1, y1],
                   [0, 2, y1, x1, -y1, x1],
                   [2, 0, x2, -y2, x2, y2],
                   [0, 2, y2, x2, -y2, x2],
                   [2, 0, x3, -y3, x3, y3],
                   [0, 2, y3, x3, -y3, x3] ] )
  X = .5 * Xm
  D = np.dot( np.linalg.inv( X ), U )
  return D

def triangulate( datadict ):

  try:
   del datadict['BEAV']
   del datadict['SLAP']
   del datadict['HOOK']
   del datadict['GOOD']
   del datadict['BOIS']
   del datadict['KENT']
  except:
    pass

 

  stnfile = np.load( os.path.join( os.path.dirname(__file__), 'mesonet.npz' ) )
  m = P( stationdict=stnfile, area='MESONET' ).proj()
  gridX = []
  gridY = []
  stations = []
  for stn in datadict.keys():
    if np.isnan( datadict[ stn ][ 'UMET' ] ) == True or np.isnan( datadict[ stn ][ 'VMET' ] ) == True:
      del datadict[ stn ]
      continue
    else:
      gridX.append( stnfile[ stn ][0] )
      gridY.append( stnfile[ stn ][1] )
      stations.append( stn )
  x,y = m( gridX, gridY )
  x = np.array( x )
  y = np.array( y )
  centers,edges,tri,neighbors = md.delaunay( x, y )
  return ( centers, edges, tri, neighbors, stations, x, y )
