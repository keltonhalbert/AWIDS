#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import os

class Projection( object ):
  def __init__( self, **kwargs ):
    self.StationDict = kwargs.get( 'stationdict', np.load( os.path.join( os.path.dirname(__file__), 'stations.npz' ) ) )
    self.area = kwargs.get( 'area', 'CONUS')
    
  def proj( self ):
    StationID = self.StationDict.keys()
    area = self.area
    if not area:
      print 'Error: No map area specified!'
      sys.exit()
    area = area.upper()
    if area == 'INTL':
      map =  Basemap(width=8000000,height=5000000,
                   rsphere=(6378137.00,6356752.3142),\
                   resolution='l',area_thresh=1000.,projection='lcc',\
                   lat_1=40,lat_2=30,lat_0=38.5,lon_0=-98.5)
    if area == 'CONUS' or area == 'US':
      map =  Basemap(width=5000000,height=3000000,
                   rsphere=(6378137.00,6356752.3142),\
                   resolution='l',area_thresh=1000.,projection='lcc',\
                   lat_1=40,lat_2=30,lat_0=38.5,lon_0=-98.5)
    if area == 'TN' or area == 'TENNESSEE':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=35,lon_0=-87)
    if area == 'MS' or area == 'MISSISSIPPI':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=33,lon_0=-90)
    if area == 'AL' or area == 'ALABAMA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=33,lon_0=-87)
    if area == 'GA' or area == 'GEORGIA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=33,lon_0=-85)
    if area == 'FL' or area == 'FLORIDA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=30,lon_0=-87)
    if area == 'LA' or area == 'LOUISIANA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=32,lon_0=-92)
    if area == 'AR' or area == 'ARKANSAS':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=35,lon_0=-93)
    if area == 'TX' or area == 'TEXAS':
      map = Basemap(width=1700000,height=1300000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=31.5,lon_0=-98)
    if area == 'OK' or area == 'OKLAHOMA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=35,lon_0=-98)
    if area == 'NM' or area == 'NEW MEXICO':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=35,lon_0=-106)
    if area == 'AZ' or area == 'ARIZONA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=34,lon_0=-113)
    if area == 'CA' or area == 'CALIFORNIA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=37.5,lon_0=-120)
    if area == 'NV' or area == 'NEVADA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=39,lon_0=-116)
    if area == 'UT' or area == 'UTAH':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=39.5,lon_0=-112)
    if area == 'CO' or area == 'COLORADO':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=39,lon_0=-105)
    if area == 'KS' or area == 'KANSAS':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=38.5,lon_0=-98.5)
    if area == 'MO' or area == 'MISSOURI':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=38.5,lon_0=-92.5)
    if area == 'KY' or area == 'KENTUCKY':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=38,lon_0=-86)
    if area == 'SC' or area == 'SOUTH CAROLINA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=34.5,lon_0=-84)
    if area == 'NC' or area == 'NORTH CAROLINA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=36,lon_0=-84.5)
    if area == 'VA' or area == 'VIRGINIA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=38,lon_0=-82)
    if area == 'WV' or area == 'WEST VIRGINIA':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=39.5,lon_0=-81)
    if area == 'MD' or area == 'MARYLAND':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=40,lon_0=-76)
    if area == 'DE' or area == 'DELAWARE':
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=40,lon_0=-76)
    if area in StationID:
      lon_lat = self.StationDict[ area ]
      map = Basemap(width=1500000,height=1100000,
                  rsphere=(6378137.00,6356752.3142),\
                  resolution='l',area_thresh=1000.,projection='lcc',\
                  lat_1=40,lat_2=30,lat_0=lon_lat[1],lon_0=lon_lat[0])
    return map