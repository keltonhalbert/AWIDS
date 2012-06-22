#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.




"""  
  This module takes wind speed observations ( direction, speed )
  and converts it into the U and V components of wind. Direction is
  represented by a value of degrees up to 360. Speed is typically 
  given in knots, but can be any unit (mph, m/s, etc).
  
  The vectors.UWIN and vectors.VWIN functions will return the desired 
  component of wind, in the units of the wind speed observation. So, 
  if the wind speed observation is given in knots, U and V will 
  be returned in knots. 
  
  The vectors.UMET and vectors.VMET functions are used for converting
  wind speed observations from knots into meters per second. They return 
  U and V in units of meters per second. 
  
  EXAMPLE:
  
    from awids import vectors
  
    dir = 270 ## degrees on a compass
    spd = 20  ## knots
  
    U = vectors.UWIN( dir, spd )
    V = vectors.VWIN( dir, spd ) 
  
  And U and V are returned as the unit of spd. If using UMET and VMET,
  speed units must be in knots.
  
"""

import numpy as np

def UMET( dir, spd ):
  dir_radian = np.radians( dir )
  U = spd * -np.sin( dir_radian )
  return U
  
def VMET( dir, spd ):
  dir_radian = np.radians( dir )
  V = spd * -np.cos( dir_radian )
  return V
  
def UWIN( dir, spd ):
  U = UMET( dir, spd*1.943846)
  return U

def VWIN( dir, spd ):
  V = VMET( dir, spd*1.943846 )
  return V
