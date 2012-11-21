#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially.

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import numpy as np
import os
import sys

class Grids( object ):
  def __init__( self, **kwargs ):
    ## Check the keyword arguments to see if the user wants to use Mesonet data or METAR
    ## data, and then load the appropriate station and grid dictionaries
    if kwargs.get('StationDict') == 'mesonet':
      stations = np.load( os.path.join( os.path.dirname( __file__ ), 'mesonet.npz' ) )
    else:
      stations = np.load( os.path.join( os.path.dirname( __file__ ), 'stations.npz' ) )
    if kwargs.get('GridFile') == 'mesonet_oa':
      gridfile = np.load( os.path.join( os.path.dirname( __file__ ), 'mesonet_oa.npz' ) )
    else:
      gridfile = np.load( os.path.join( os.path.dirname( __file__ ), 'sfcoa_lonlats.npz' ) )
    ## assign the loaded npz files
    self.StationDict = stations
    self.GridFile = gridfile
    self.gridlons = self.GridFile[ 'lons' ]
    self.gridlats = self.GridFile[ 'lats' ]