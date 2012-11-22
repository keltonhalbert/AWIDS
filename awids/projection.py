#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially.

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import numpy as np
import os
import sys
from loadgrids import Grids
from mpl_toolkits.basemap import Basemap

class Projection( Grids ):
  def __init__( self, **kwargs ):
    Grids.__init__( self, **kwargs ) 
    self.area = kwargs.get( 'area', 'CONUS' )
    self.StationIDs = self.StationDict.keys()
  
  def mproj( self ):
    if self.area == 'MESONET':
      self.m = Basemap(projection='lcc', resolution='l', width=550000, height=400000,
                       lat_0=35.4, lon_0=-97.2, lat_1=30., lat_2=45.)
    if self.area in self.StationIDs:
      lon_lat = self.StationDict[ self.area ]
      self.m = Basemap(width=1500000,height=1100000,
                       rsphere=(6378137.00,6356752.3142),\
                       resolution='l',area_thresh=1000.,projection='lcc',\
                       lat_1=40,lat_2=30,lat_0=lon_lat[1],lon_0=lon_lat[0])
    if self.area == 'CONUS' or self.area == 'US':
      self.m = Basemap(width=5000000,height=3000000,
                       rsphere=(6378137.00,6356752.3142),\
                       resolution='l',area_thresh=1000.,projection='lcc',\
                       lat_1=40,lat_2=30,lat_0=38.5,lon_0=-98.5)
    return self.m