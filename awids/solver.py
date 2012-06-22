import numpy as np
from Projection import Projection as P
import matplotlib.delaunay as md

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

  if 'WALT' in datadict.keys():
    datadict['WAL2'] = datadict['WALT']
    del datadict['WALT']

  stnfile = np.load( os.path.join( os.path.dirname(__file__), 'mesonet.npz' ) )
  m = P( stationdict=stnfile, area='OK' ).proj()
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
