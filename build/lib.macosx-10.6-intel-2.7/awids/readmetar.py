#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import sys
import os
import urllib
import re
import thermo as therm
import vectors as vect
import numpy as np
import time as gmtime
from loadgrids import Grids

class OBSWX( Grids ):
  def __init__( self, **kwargs ): ## This function chooses how to initialize the time 
## the program will use to download the data
    Grids.__init__( self, **kwargs )
    gmt = gmtime.gmtime()
    self.year = str( gmt[0] )
    self.month = str( gmt[1] ).zfill( 2 )
    self.day = str( gmt[2] ).zfill( 2 )
    self.hour = str( gmt[3] ).zfill( 2 )
    datestring = self.year[-2:] + self.month  + self.day + self.hour
    self.cycle = datestring
    
  def Surface( self, **kwargs ): ## Here begins the METAR decoder
    self.DatDict = {} ## this will serve as the intermediate dictionary for sorting
    self.RESULT = {} ## this is the result dictionary
    self.count = 0 ## will be used to tell us how many stations were not found
    stations = self.StationDict
    cycle = kwargs.get( 'cycle', self.cycle )
    file = urllib.urlopen( 'http://metfs1.agron.iastate.edu/data/text/sao/'+ cycle + '.sao' )
    text = file.read().replace( '\n' , '' ).replace( '\x03' , '' ).replace( '\x03\x01' , '' ).replace( '\r' , '' ).strip().split( '=' )
    
    ## process the text 
    for line in text:
      if line.startswith( 'METAR' ):
        line = line.strip( 'METAR' )
      if line.startswith( 'K' ) == False and line.startswith( 'C' ) == False and line.startswith( 'M' ) == False and line.startswith( 'P' ) == False:  ## ignore lines with no metar station
        continue
      else:
        stn_key = line[:4] ## grab the station identifies, i.e. KBNA
        try:
        ## repeat observations are filtered by choosing the longest list of observations
          if len( self.DatDict[ stn_key ].split() ) < len( line[4:].split() ):
            self.DatDict[ stn_key ] = line[4:]
        except:
        ## if no observation, initialize it in the dictionary
          self.DatDict[ stn_key ] = line[4:]
          
    for stn in self.DatDict.keys():
      if not stn in stations:
        self.count += 1 ## count the stations missing from the file
        continue
      stndat = self.DatDict[ stn ]
      if re.search( '([0-9][0-9][0-9])([0-9][0-9])(G[0-9][0-9]KT)', stndat ): 
        ## These various regular expressions search for patterns
        ## that correspond with a certain type of data
        windat = re.search( '([0-9][0-9][0-9])([0-9][0-9])(G[0-9][0-9]KT)', stndat ).group()
        self.wdir = int( windat[:3] )
        self.wspd = int( windat[3:-5] )
        self.gust = int( windat[-4:-2] )
      elif re.search( '([0-9][0-9][0-9])([0-9][0-9]KT)', stndat ):
        windat = re.search( '([0-9][0-9][0-9])([0-9][0-9])KT', stndat ).group()
        self.wdir = int( windat[:3] )
        self.wspd = int( windat[3:-2] )
        self.gust = np.nan
      else:
        self.wdir = np.nan
        self.wspd = np.nan
        self.gust = np.nan
      if re.search( '\s(M[0-9][0-9])/(M[0-9][0-9])\s|\s([0-9][0-9])/(M[0-9][0-9])\s|\s(M[0-9][0-9])/(NIL)\s|\s([0-9][0-9])/(NIL)\s|\s([0-9][0-9])/([0-9][0-9])\s', stndat ):
        self.tempdat = re.search( '\s(M[0-9][0-9])/(M[0-9][0-9])\s|\s([0-9][0-9])/(M[0-9][0-9])\s|\s(M[0-9][0-9])/(NIL)\s|\s([0-9][0-9])/(NIL)\s|\s([0-9][0-9])/([0-9][0-9])\s', stndat ).group().replace( 'M','-' ).split( '/' )
        self.tempdat[0] = int( self.tempdat[0] )
        self.tempdat[1] = int( self.tempdat[1] )
      else:
        self.tempdat = [np.nan, np.nan]
      if re.search( 'SLP[0-9][0-9][0-9]',stndat ):
        self.slpdat = re.search( 'SLP[0-9][0-9][0-9]', stndat ).group().replace( 'SLP', '' )
        if int(self.slpdat) <= 500:
          self.slpdat = 1000 + int(self.slpdat[:2]) + int(self.slpdat[2])/10
        elif int(self.slpdat) > 500:
          self.slpdat = 900 + int(self.slpdat[:2]) + int(self.slpdat[2])/10
      else:
        self.slpdat = np.nan
      if re.search( 'A[0-9][0-9][0-9][0-9]',stndat ):
        self.altdat = re.search( 'A[0-9][0-9][0-9][0-9]', stndat ).group().strip( 'A' )
        self.altdat = int(self.altdat[:2]) + float(self.altdat[2:])/100
      else:
        self.altdat = np.nan
      if re.search( '[0-9][0-9]SM|[0-9]SM', stndat ):
        self.vis = re.search( '[0-9][0-9]SM|[0-9]SM', stndat ).group().replace( 'SM', '' )
      else:
        self.vis = np.nan
      if re.search ('\s(P[0-9][0-9][0-9][0-9])', stndat ):
        self.precip = re.search ('\s(P[0-9][0-9][0-9][0-9])', stndat ).group().replace( 'P', '' )
        self.precip = float( str( self.precip )[:2] + '.' + str( self.precip )[3:] )
      else:
        self.precip = np.nan
      self.RESULT[ stn ] = {}
      self.RESULT[ stn ][ 'TMPC' ] =  self.tempdat[0] 
      self.RESULT[ stn ][ 'TMPF' ] = self.tempdat[0] * 1.8 + 32
      self.RESULT[ stn ][ 'DWPC' ] = self.tempdat[1]
      self.RESULT[ stn ][ 'DWPF' ] = self.tempdat[1] * 1.8 + 32
      self.RESULT[ stn ][ 'THTA' ] = therm.theta( self.altdat, self.tempdat[0] )
      self.RESULT[ stn ][ 'MIXR' ] = therm.mixingratio( self.altdat, self.tempdat[0], self.tempdat[1] )
      self.RESULT[ stn ][ 'THTE' ] = therm.thetae( self.altdat, self.tempdat[0], self.tempdat[1] )
      self.RESULT[ stn ][ 'RELH' ] = therm.relhumid( self.tempdat[0], self.tempdat[1] )
      self.RESULT[ stn ][ 'WDIR' ] = self.wdir
      self.RESULT[ stn ][ 'WSPD' ] = self.wspd
      self.RESULT[ stn ][ 'GUST' ] = self.gust
      self.RESULT[ stn ][ 'VWIN' ] = vect.VWIN( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'UWIN' ] = vect.UWIN( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'UMET' ] = vect.UMET( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'VMET' ] = vect.VMET( self.wdir, self.wspd )
      self.RESULT[ stn ][ 'PRES' ] = self.slpdat
      self.RESULT[ stn ][ 'ALTI' ] = self.altdat
      self.RESULT[ stn ][ 'VISI' ] = self.vis
      self.RESULT[ stn ][ 'PCPN' ] = self.precip
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
