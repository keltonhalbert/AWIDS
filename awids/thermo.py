#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.

import numpy as np
from math import pow

class Thermo(object):
  def dewpoint_c( self, tpc, rh ):
    a = 17.271
    b = 237.7
    term = ( ( a * tpc ) / ( b + tpc ) ) + np.log( rh / 100 )
    self.dewpoint = ( b * term ) / ( a - term )
    return self.dewpoint
  
  def dewpoint_f( self, tpc, rh ):
    self.dewpoint = ( Thermo().dewpoint_c( tpc, rh ) * 1.8 ) + 32
    return self.dewpoint
 
  def fahrenheit( self, tpc ):
    self.fahrenheit = ( tpc * 1.8 ) + 32
    return self.fahrenheit

  def theta( self, altimiter, tpc ):
    hpa = 33.8639 * altimiter
    tpk = int(tpc) + 273.15
    self.theta = tpk * pow( ( 1000 / hpa ), 0.286 )
    return self.theta
  
  def mixingratio( self, altimiter, tpc, tdc ):
    hpa = 33.8639 * altimiter
    tpk = int(tpc) + 273.15
    tdk = int(tdc) + 273.15
    func2 = ( -1 * 5420 )/tdk
    e = (2.53 * pow( 10, 11 ))*np.exp(func2)
    e_hpa = e / 100
    self.mixr = ( ( 0.622 * e_hpa )/( hpa - e_hpa ) ) * ( 1000/1 )
    return self.mixr
  
  def thetae( self, altimiter, tpc, tdc ):
    therm = Thermo()
    theta = therm.theta( altimiter, int(tpc) )
    hpa = 33.8639 * altimiter
    tdk = int(tdc) + 273.15
    tpk = int(tpc) + 273.15
    func2 = ( -1*5420 )/tdk
    e = ( 2.53 * pow( 10,11 ) ) * np.exp( func2 )
    e_hpa = e / 100
    mixr = ( ( 0.622 * e_hpa )/( hpa - e_hpa ) )
    self.thetae = theta*np.exp( ( ( 2.50 * pow( 10, 6 ) ) * mixr )/( 1005 * tpk ) )
    return self.thetae
    
  def relhumid( self, tpc, tdc ):
    tpk = int(tpc) + 273.15
    tdk = int(tdc) + 273.15
    es_func = ( 2.53 * pow( 10, 11 ) ) * np.exp( -5420/tpk )
    e_func = ( 2.53 * pow( 10, 11 ) ) * np.exp( -5420/tdk )
    relfrac = e_func / es_func
    self.relh = relfrac * 100
    return self.relh
