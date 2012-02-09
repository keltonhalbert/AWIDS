#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


import numpy as np

def UWIN( dir, spd ):
  if dir == '-999.99' or spd == '-999.99':
    U = '-999.99'
  else:
    dir = int(dir)
    spd = float(spd)
    dir_radian = np.radians( dir )
    U = spd * -np.sin( dir_radian )
  return U
  
def VWIN( dir, spd ):
  if dir == '-999.99' or spd == '-999.99':
    V = '-999.99'
  else:
    dir = int(dir)
    spd = float(spd)
    dir_radian = np.radians( dir )
    V = spd * -np.cos( dir_radian )
  return V
  
def UMET( dir, spd ):
  if dir == '-999.99' or spd == '-999.99':
    U = '-999.99'
  else:
    U = UWIN( dir, int(spd)*0.514444)
  return U

def VMET( dir, spd ):
  if dir == '-999.99' or spd == '-999.99':
    V = '-999.99'
  else:
    V = VWIN( dir, int(spd)*0.514444 )
  return V