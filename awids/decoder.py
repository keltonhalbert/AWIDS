#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import sys
import os
import time as gmtime
import urllib
import re
import thermo as therm
import vectors as vect
import numpy as np

class OBSWX(object):
  def __init__( self ): ## This function chooses how to initialize the time 
## the program will use to download the data
    gmt = gmtime.gmtime()
    year = str( gmt[0] )
    month = str( gmt[1] ).zfill( 2 )
    day = str( gmt[2] ).zfill( 2 )
    hour = str( gmt[3] ).zfill( 2 )
    datestring = year[-2:] + month  + day + hour
    self.cycle = datestring
    
  def Surface( self, **kwargs ): ## Here begins the METAR decoder
    self.DatDict = {} ## this will serve as the intermediate dictionary for sorting
    self.RESULT = {} ## this is the result dictionary
    self.count = 0 ## will be used to tell us how many stations were not found
    if sys.platform.startswith( 'win' ):
      stations = kwargs.get( 'stations', np.load( os.path.abspath( sys.prefix + '/lib/' + '/site-packages/AWIDS-1.0.0-py2.7.egg/awids/' + 'stations.npz' ) ) ).keys()
    else:
      stations = kwargs.get( 'stations', np.load( os.path.abspath( sys.prefix + '/lib/python' + sys.version[:3] + '/site-packages/AWIDS-1.0.0-py2.7.egg/awids/' + 'stations.npz' ) ) ).keys()
    cycle = kwargs.get( 'cycle', self.cycle )
    file = urllib.urlopen( 'http://metfs1.agron.iastate.edu/data/text/sao/'+ cycle + '.sao' )
    text = file.read().replace( '=' , '' ).replace( '\x03' , '' ).replace( '\x03\x01' , '' ).replace( '\r' , '' ).strip().split( '\n' )
    ## process the text 
    for line in text:
      if line.startswith( 'METAR' ):
        line = line.strip( 'METAR' )
      if line.startswith( 'K' ) == False and line.startswith( 'C' ) == False and line.startswith( 'M' ) == False:  ## ignore lines with no metar station
        continue
      else:
        stn_key = line[:4] ## grab the station identifies, i.e. KBNA
        if stn_key in self.DatDict.keys(): ## this check is used to see if another version of the data has more info
          if len( self.DatDict[ stn_key ].split() ) < len( line[4:].split() ):
            self.DatDict[ stn_key ] = line[4:]
        else:
          self.DatDict[ stn_key ] = line[4:]
    for stn in self.DatDict.keys():
      if not stn in stations:
        self.count += 1 ## count the stations missing from the file
        continue
      stndat = self.DatDict[ stn ]
      if re.search( '([0-9][0-9][0-9])([0-9][0-9])(G[0-9][0-9]KT)', stndat ): ## These various regular expressions search for patterns
        ## that correspond with a certain type of data
        windat = re.search( '([0-9][0-9][0-9])([0-9][0-9])(G[0-9][0-9]KT)', stndat ).group()
        self.wdir = windat[:3]
        self.wspd = windat[3:-5]
        self.gust = windat[-4:-2]
      elif re.search( '([0-9][0-9][0-9])([0-9][0-9]KT)', stndat ):
        windat = re.search( '([0-9][0-9][0-9])([0-9][0-9])KT', stndat ).group()
        self.wdir = windat[:3]
        self.wspd = windat[3:-2]
        self.gust = '-999.99'
      else:
        self.wdir = '-999.99'
        self.wspd = '-999.99'
        self.gust = '-999.99'
      if re.search( '(M[0-9][0-9])/(M[0-9][0-9])|([0-9][0-9])/(M[0-9][0-9])|(M[0-9][0-9])/(NIL)|([0-9][0-9])/(NIL)|([0-9][0-9])/([0-9][0-9])', stndat ):
        self.tempdat = re.search( '(M[0-9][0-9])/(M[0-9][0-9])|([0-9][0-9])/(M[0-9][0-9])|(M[0-9][0-9])/(NIL)|([0-9][0-9])/(NIL)|([0-9][0-9])/([0-9][0-9])', stndat ).group().replace( 'M','-' ).split( '/' )
      else:
        self.tempdat = ['-999.99', '-999.99']
      if re.search( 'SLP[0-9][0-9][0-9]',stndat ):
        self.slpdat = re.search( 'SLP[0-9][0-9][0-9]', stndat ).group().replace( 'SLP', '' )
        if int(self.slpdat) <= 500:
          self.slpdat = 1000 + int(self.slpdat[:2]) + int(self.slpdat[2])/10
        elif int(self.slpdat) > 500:
          self.slpdat = 900 + int(self.slpdat[:2]) + int(self.slpdat[2])/10
      else:
        self.slpdat = '-999.99'
      if re.search( 'A[0-9][0-9][0-9][0-9]',stndat ):
        self.altdat = re.search( 'A[0-9][0-9][0-9][0-9]', stndat ).group().strip( 'A' )
        self.altdat = int(self.altdat[:2]) + float(self.altdat[2:])/100
      else:
        self.altdat = '-999.99'
      if re.search( '[0-9][0-9]SM|[0-9]SM', stndat ):
        self.vis = re.search( '[0-9][0-9]SM|[0-9]SM', stndat ).group().replace( 'SM', '' )
      else:
        self.vis = '-999.99'
      
      self.RESULT[ stn ] = {}
      if self.tempdat[0] != '-999.99':
        self.RESULT[ stn ][ 'TMPC' ] = int( self.tempdat[0] )
      else:
        self.RESULT[ stn ][ 'TMPC' ] = self.tempdat[0]
      if self.tempdat[0] != '-999.99':
        self.RESULT[ stn ][ 'TMPF' ] = int( self.tempdat[0] ) * 1.8 + 32
      else:
        self.RESULT[ stn ][ 'TMPF' ] = self.tempdat[0]
      if self.tempdat[1] != '-999.99':
        self.RESULT[ stn ][ 'DWPC' ] = int( self.tempdat[1] )
      else:
        self.RESULT[ stn ][ 'DWPC' ] = self.tempdat[1]
      if self.tempdat[1] != '-999.99':
        self.RESULT[ stn ][ 'DWPF' ] = int( self.tempdat[1] ) * 1.8 + 32
      else:
        self.RESULT[ stn ][ 'DWPF' ] = self.tempdat[1]
      self.RESULT[ stn ][ 'THTA' ] = therm.Thermo().theta( self.altdat, self.tempdat[0] )
      self.RESULT[ stn ][ 'MIXR' ] = therm.Thermo().mixingratio( self.altdat, self.tempdat[0], self.tempdat[1] )
      self.RESULT[ stn ][ 'THTE' ] = therm.Thermo().thetae( self.altdat, self.tempdat[0], self.tempdat[1] )
      self.RESULT[ stn ][ 'RELH' ] = therm.Thermo().relhumid( self.tempdat[0], self.tempdat[1] )
      self.RESULT[ stn ][ 'WDIR' ] = self.wdir
      self.RESULT[ stn ][ 'WSPD' ] = self.wspd
      self.RESULT[ stn ][ 'GUST' ] = self.gust
      self.RESULT[ stn ][ 'VWIN' ] = vect.VWIN( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'UWIN' ] = vect.UWIN( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'UMET' ] = vect.UMET( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'VMET' ] = vect.VMET( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'MSLP' ] = self.slpdat
      self.RESULT[ stn ][ 'ALTI' ] = self.altdat
      self.RESULT[ stn ][ 'VISI' ] = self.vis
    file.close()
    return self.RESULT
  def UpperAir(self, cycle, stations):
    self.SoundingLevels = {}
    newlist = []
    for stn in stations:
      file = urllib.urlopen('http://www.spc.noaa.gov/exper/soundings/'+ self.cycle + '_OBS/' + stn + '.txt')
      text = file.read().split('\n')
      for line in text:
        line = line.strip(' ').split(',')
        try:
          level = float(line[0])
          hght = float(line[1])
          temp = float(line[2])
          dwpt = float(line[3])
          wdir = float(line[4])
          wspd = float(line[5])
          key = str(stn) + '_' + str(level)
          SoundingLevels[key] = (hght, temp, dwpt, wdir, wspd)
        except:
          continue
      print 'Finished Station ' + stn
      file.close()
    return SoundingLevels
