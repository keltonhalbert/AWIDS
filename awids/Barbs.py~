#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import numpy as np
from Projection import Projection as proj
import gridmaker
import sys
import os

class PlotBarbs( object ):
  def __init__( self, **kwargs ):
    if kwargs.get('StationDict') == 'mesonet.npz':
      self.StationDict = np.load( os.path.join( os.path.dirname(__file__), 'mesonet.npz' ) )
    else:
      self.StationDict = np.load( os.path.join( os.path.dirname(__file__), 'stations.npz' ) ) 
    self.area = kwargs.get( 'area', 'CONUS' )
    self.DataDict = kwargs.get( 'DatDict' )
    pmap = proj( area=self.area )
    self.m = pmap.proj()
    
  def StnBarbs( self ):
    StationIDs = self.StationDict.keys()
    U = []
    V = []
    barblons = []
    barblats = []
    for stn in self.DataDict.keys():
      u = self.DataDict[ stn ][ 'UWIN' ]
      v = self.DataDict[ stn ][ 'VWIN' ]
      if np.isnan( u ) == True or np.isnan( v ) == True:
        continue
      if not stn in self.StationDict.keys(): continue
      lon_lat_tuple = self.StationDict[ stn ]
      barblons.append( lon_lat_tuple[0] )
      barblats.append( lon_lat_tuple[-1] )
      U.append( u )
      V.append( v )
    bx, by = self.m( barblons, barblats )
    return self.m.barbs( bx, by, U, V, fill_empty=False, length=5.7 )
    
  def GridBarbs( self ):
    gmaker = gridmaker.GRIDMAKER( datdict=self.DataDict, area=self.area, StationDict=self.StationDict )
    u = gmaker.grid( datatype='UWIN' )
    v = gmaker.grid( datatype='VWIN' )
    return self.m.barbs( u[0], u[1], u[2], v[2], fill_empty=False, length=5.7 )
