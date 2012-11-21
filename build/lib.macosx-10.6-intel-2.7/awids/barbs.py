#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import numpy as np
from loadgrids import Grids
import sys
import os

class Plotbarbs( Grids ):
  def __init__( self, **kwargs ):
    Grids.__init__( self, **kwargs )
    self.m = kwargs.get( 'projection' )
    self.DataDict = kwargs.get( 'DatDict' )

  def StnBarbs( self, **kwargs ):
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
      if not stn in StationIDs: continue
      lon_lat_tuple = self.StationDict[ stn ]
      barblons.append( lon_lat_tuple[0] )
      barblats.append( lon_lat_tuple[-1] )
      U.append( u )
      V.append( v )
    bx, by = self.m( barblons, barblats )
    return self.m.barbs( bx, by, U, V, fill_empty=False, length=5.7 )
    
#  def GridBarbs( self, **kwargs ):
#    gmaker = gridmaker.GRIDMAKER( GridFile=self.GridFile, datdict=DataDict, area=self.area, StationDict=self.StationDict )
 #   u = gmaker.grid( datatype='UWIN' )
 #   v = gmaker.grid( datatype='VWIN' )
 #   return self.m.barbs( u[0], u[1], u[2], v[2], fill_empty=False, length=5.7 )
