from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import datetime
import time as gmtime
import urllib
import re

def get_satellite( **kwargs ):
  type = kwargs.get( 'SAT', 'VIS' )
  ## open the directory that holds the latest files
  if type == 'IR':
    url = urllib.urlopen( 'http://motherlode.ucar.edu/thredds/dodsC/satellite/IR/EAST-CONUS_4km/current/' )
  else:
    url = urllib.urlopen( 'http://motherlode.ucar.edu/thredds/dodsC/satellite/VIS/EAST-CONUS_1km/current/' )
  ## read in the file to be sorted
  page = url.read()
  ## find all instances of this match
  search = re.findall( '/' + type + '/EAST-CONUS_[0-9]km/current/EAST-CONUS_[0-9]km_'+ type + '_[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9].gini', page )
  ## orient in descending order
  search = sorted( search, reverse=True )
  ## assign a variable to the latest time frame
  latest_file = search[0]
  ncfile = 'http://motherlode.ucar.edu/thredds/dodsC/satellite/' + latest_file
  ## load the netCDF file
  d = Dataset( ncfile )
  x = d.variables[ 'x' ][:]*1000
  y = d.variables[ 'y' ][:]*1000
  ## shift the data to fir the projection units
  x = x + -1*x.min()
  y = y + -1*y.min()
  sat = d.variables[ type.upper() ][0][:]
  sat = sat.data
  ## convert data from unsigned bytes to shorts
  sat = sat & 0xff
  return ( x, y, sat )