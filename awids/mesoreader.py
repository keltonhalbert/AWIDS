#! /usr/bin/env python
#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

"""
  Given the argument filedate, it will pull mesonet data. if filedate starts
  with 'htt', it will pull the data from the mesonet server. Otherwise, it will
  look for a local file in your current directory. 
  
  Returns a dictionary of dictionaries, where
  dictionary[ STATION_ID ][ DATATYPE ] = value
"""
import vectors
from thermo import Thermo
import urllib
import numpy as np

def MesonetReader( filedate ):
  mesonet = {}
  if filedate[:4] == 'http':
    mesdat = urllib.urlopen( 'http://www.mesonet.org/data/public/mesonet/latest/latest.mdf' )
  else:
    mesdat = open( filedate + '.mdf', 'r' )
  data = mesdat.read().split('\n')
  for n in range(3, 123):
    StationData = data[ n ]
    StationData = StationData.split()
    if len( StationData ) < 16:
      continue
    stn = StationData[0]
   ## Initialize a dictionary of dictionaries for easy data access
    mesonet[ stn ] = {}
   ## Variable names come from the Oklahoma Mesonet Website 
    mesonet[ stn ][ 'RELH' ] = float( StationData[3] )
    mesonet[ stn ][ 'TMPC' ] = float( StationData[4] )
    mesonet[ stn ][ 'WSPD' ] = float( StationData[5] )
    mesonet[ stn ][ 'WVEC' ] = float( StationData[6] )
    mesonet[ stn ][ 'WDIR' ] = float( StationData[7] )
    mesonet[ stn ][ 'WDSD' ] = float( StationData[8] )
    mesonet[ stn ][ 'WSSD' ] = float( StationData[9] )
    mesonet[ stn ][ 'WMAX' ] = float( StationData[10] )
    mesonet[ stn ][ 'RAIN' ] = float( StationData[11] )
    mesonet[ stn ][ 'PRES' ] = float( StationData[12] )
    mesonet[ stn ][ 'SRAD' ] = float( StationData[13] )
    mesonet[ stn ][ 'TA9M' ] = float( StationData[14] )
    mesonet[ stn ][ 'WS2M' ] = float( StationData[15] )
    mesonet[ stn ][ 'TS10' ] = float( StationData[16] )
    mesonet[ stn ][ 'TB10' ] = float( StationData[17] )
    mesonet[ stn ][ 'TS05' ] = float( StationData[18] )
    mesonet[ stn ][ 'TB05' ] = float( StationData[19] )
    mesonet[ stn ][ 'TS30' ] = float( StationData[20] )
    mesonet[ stn ][ 'TR05' ] = float( StationData[21] )
    mesonet[ stn ][ 'TR25' ] = float( StationData[22] )
    mesonet[ stn ][ 'TR60' ] = float( StationData[23] )
   ## Filter out the bad values and convert to NaN
    for k in mesonet.keys():
      for v in mesonet[ k ].keys():
        if mesonet[ k ][ v ] == -999.0 or mesonet[ k ][ v ] == -998.0 or mesonet[ k ][ v ] == -997.0 or mesonet[ k ][ v ] == -996.0:
          mesonet[ k ][ v ] = np.nan
   ## Objects that must be calculated separately
    mesonet[ stn ][ 'UWIN' ] = vectors.UWIN( mesonet[ stn ][ 'WDIR' ], mesonet[ stn ][ 'WSPD' ] )
    mesonet[ stn ][ 'VWIN' ] = vectors.VWIN( mesonet[ stn ][ 'WDIR' ], mesonet[ stn ][ 'WSPD' ] )
    mesonet[ stn ][ 'UMET' ] = vectors.UMET( mesonet[ stn ][ 'WDIR' ], mesonet[ stn ][ 'WSPD' ] )
    mesonet[ stn ][ 'VMET' ] = vectors.VMET( mesonet[ stn ][ 'WDIR' ], mesonet[ stn ][ 'WSPD' ] )
    mesonet[ stn ][ 'TMPF' ] = Thermo().fahrenheit( mesonet[ stn ][ 'TMPC' ] )
    mesonet[ stn ][ 'DWPC' ] = Thermo().dewpoint_c( mesonet[ stn ][ 'TMPC' ], mesonet[ stn ][ 'RELH' ] )
    mesonet[ stn ][ 'DWPF' ] = Thermo().dewpoint_f( mesonet[ stn ][ 'TMPC' ], mesonet[ stn ][ 'RELH' ] ) 
  return mesonet



if __name__ == '__main__':
  data = MesonetReader( '201105241830.mdf' )
  print data[ 'ADAX' ][ 'UMET' ]
