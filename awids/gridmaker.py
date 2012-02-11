#AWIDS - Advanced Weather Interactive Diagnostic System
#(c) <2012> Kelton Halbert

#Non-commercial license clause can be waived with written permission by the author. Contact Kelton Halbert <keltonhalbert@tempestchasing.com> for permission to use commercially. 

#This work is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License. To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/ or send a letter to Creative Commons, 444 Castro Street, Suite 900, Mountain View, California, 94041, USA.


import numpy as np
from matplotlib.mlab import griddata
from math import pow
from Projection import Projection  as proj
import matplotlib as mpl
import matplotlib.pyplot as plt
import sys
import os

class GRIDMAKER( object ):

  def __init__( self, **kwargs ):
    if sys.platform.startswith( 'win' ):
      self.StationDict = kwargs.get( 'StationDict', np.load( os.path.abspath( sys.prefix + '/lib/' + '/site-packages/AWIDS-1.0.0-py2.7.egg/awids/' + 'stations.npz' ) ) )
      self.GridFile = kwargs.get( 'GridFile', np.load( os.path.abspath( sys.prefix + '/lib/' + '/site-packages/AWIDS-1.0.0-py2.7.egg/awids/' + 'sfcoa_lonlats.npz' ) ) )
    else:
      self.StationDict = kwargs.get( 'StationDict', np.load( os.path.abspath( sys.prefix + '/lib/python' + sys.version[:3] + '/site-packages/AWIDS-1.0.0-py2.7.egg/awids/' + 'stations.npz' ) ) )
      self.GridFile = kwargs.get( 'GridFile', np.load( os.path.abspath( sys.prefix + '/lib/python' + sys.version[:3] + '/site-packages/AWIDS-1.0.0-py2.7.egg/awids/' + 'sfcoa_lonlats.npz' ) ) )
    self.gridlons = self.GridFile[ 'lons' ]
    self.gridlats = self.GridFile[ 'lats' ]
    self.area = kwargs.get( 'area', 'CONUS' )
    self.DataDict = kwargs.get( 'datdict' )
    self.TendDict = kwargs.get( 'tenddict' )
    mproj = proj( area=self.area, stations=self.StationDict )
    self.m = mproj.proj()

  def grid( self, **kwargs ):
    DataType = kwargs.get( 'datatype' )
    DataDict = kwargs.get( 'datdict', self.DataDict )
    plotparms = { 'TMPF': ('Temperature (F)', np.arange(-14,110,2), plt.cm.spectral), 'TMPC': ('Temperature (C)', np.arange(-25,44,1), plt.cm.spectral), 'DWPF': ('Dewpoint (F)', np.arange(0,80,2), plt.cm.BrBG), 'DWPC': ('Dewpoint (C)', np.arange(-20,26,1), plt.cm.BrBG), 'WSPD': ('Windspeed (kts)', np.arange(5,50,5), plt.cm.cool), 'MSLP': ('Sea Level Pressure (mb)', np.arange(925,1050,2), plt.cm.spectral), 'THTA': (r'Theta (K) $\theta$', np.arange(250,322,2), plt.cm.spectral), 'MIXR': (r'Mixing Ratio $\frac{g}{kg}$', np.arange(0,28,1), plt.cm.gist_earth_r), 'THTE': (r'Theta-E (K) $\theta_e$', np.arange(240,400,5), plt.cm.spectral), 'RELH': ('Relative Humidity (%)', np.arange(0,101,1), plt.cm.spectral), 'UWIN': ('U component of wind (kts)', np.arange(-50,50,2), plt.cm.BrBG), 'VWIN': ('V component of wind (kts)', np.arange(-50,50,2), plt.cm.BrBG), 'UMET': ('U component of wind (m/s)', np.arange(-50,50,2), plt.cm.BrBG), 'VMET': ('V component of wind (m/s)', np.arange (-50,50,2), plt.cm.BrBG) }
    StationID = DataDict.keys()
    data_to_plot = []
    lons = []
    lats = []
    name = plotparms[ DataType ][0]
    cmap = plotparms[ DataType ][2]
    levs = plotparms[ DataType ][1]
    for S in StationID:
      dat = DataDict[ S ][ DataType ]
      if dat == '-999.99' or dat == '': continue
      else:
        data_to_plot.append( dat )
        lon_lat_tuple = self.StationDict[ S ]
        lons.append( lon_lat_tuple[0] )
        lats.append( lon_lat_tuple[-1] )
    xi, yi = self.m( lons, lats )
    X, Y = self.m( self.gridlons, self.gridlats )
    Z = griddata( xi, yi, data_to_plot, X, Y, interp='nn' )
    return ( X, Y, Z, levs, cmap, name )
  
  def grid_3hr( self, **kwargs ):
    DataDict = self.DataDict
    TendDict = self.TendDict
    DataType = kwargs.get( 'datatype' )
    c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
    mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
    plotparms = { '3TPF': ('3 Hour Temperature (F) Tendency', np.arange(-20,20,1), plt.cm.RdBu_r, 'TMPF'), '3TPC': ('3 Hour Temperature (C) Tendency', np.arange(-15,16,1), plt.cm.RdBu_r, 'TMPC'), '3DWF': ('Three Hour Dewpoint (F) Tendency', np.arange(-20,20,1), plt.cm.RdBu_r, 'DWPF'), '3DWC': ('3 Hour Dewpoint (C) Tendency', np.arange(-15,16,1), plt.cm.RdBu_r, 'DWPC'), '3SLP': ('3 Hour Sea Level Pressure (mb) Tendency', np.arange(-8,8.5,.5),plt.cm.RdBu_r, 'MSLP'), '3THA': ('3 Hour Theta (K) Tendency', np.arange(-30,31,1), plt.cm.RdBu_r, 'THTA'), '3THE': ('3 Hour Theta-E (K) Tendency', np.arange(-30,31,1), plt.cm.RdBu_r, 'THTE'), '3VOR': (r'3 Hour Vorticity ($S^{-1}*{10^5}$) Tendency', np.arange(-20,21,1), mycm, 'VORT'), '3DIV': (r'3 Hour Surface Divergence ($S^{-1}*{10^5}$) Tendency', np.arange(-20,21,1), mycm, 'DIVR') }
    name = plotparms[ DataType ][0]
    levs = plotparms[ DataType ][1]
    cmap = plotparms[ DataType ][2]
    if DataType.upper() == '3VOR' or DataType.upper() == '3DIV':
      hour_1 = self.VectorGrid( datatype=plotparms[ DataType ][-1] )
      hour_3 = self.VectorGrid( datatype=plotparms[ DataType ][-1], datdict=TendDict )
    else:
      hour_1 = self.grid( datatype=plotparms[ DataType ][-1] )
      hour_3 = self.grid( datatype=plotparms[ DataType ][-1], datdict=TendDict )
    X = hour_1[0]
    Y = hour_1[1]
    Z = hour_1[2] - hour_3[2]
    return ( X, Y, Z, levs, cmap, name)
  
  def VectorGrid( self, **kwargs ):
    DataDict = kwargs.get( 'datdict', self.DataDict )
    DataType = kwargs.get( 'datatype' )
    u_grid = self.grid( datatype='UMET', datdict=DataDict )
    v_grid = self.grid( datatype='VMET', datdict=DataDict )
    u_grad = np.gradient( u_grid[2], 40000 )
    v_grad = np.gradient( v_grid[2], 40000 )
    X = u_grid[0]
    Y = u_grid[1]
    if DataType.upper() == 'VORT':
      name = r'Surface Vorticity ($\mathrm{s^{-1}*{10^5}}$)'
      levs = np.arange( 1, 21, 1 ) 
      cmap = plt.cm.gist_heat_r
      Z = ( v_grad[1] - -1 * u_grad[0] ) * pow( 10, 5 )
    if DataType.upper() == 'DIVR':
      name = 'Surface Divergence ($S^{-1}*{10^5}$)'
      levs = np.arange( -25, 26, 1 )
      c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
      mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
      cmap = mycm
      Z = ( u_grad[1] + -1 * v_grad[0] ) * pow( 10, 5 )
    return ( X, Y, Z, levs, cmap, name )
  
  def AdvectionGrid( self, **kwargs ):
    DataType = kwargs.get( 'datatype' )
    u_grid = self.grid( datatype='UMET' )
    v_grid = self.grid( datatype='VMET' )
    X = u_grid[0]
    Y = u_grid[1]
    if DataType.upper() == 'TPFA':
      name = r'Temperature (F) Advection $\frac{F^\circ}{Hour}$'
      levs = np.arange( -5, 6, 0.5 )
      c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
      mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
      cmap = mycm
      tf_grid = self.grid( datatype='TMPF' )
      tf_grad = np.gradient( tf_grid[2], 40000)
      Advection = -1 * (u_grid[2] * tf_grad[1] + v_grid[2] * -1 * tf_grad[0]) * 3600
    if DataType.upper() == 'TPCA':
      name = r'Temperature (C) Advection $\frac{F^\circ}{Hour}$'
      levs = np.arange( -5, 6, 0.5 )
      c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
      mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
      cmap = mycm
      tc_grid = self.grid( datatype='TMPC' )
      tc_grad = np.gradient( tc_grid[2], 40000)
      Advection = -1 * (u_grid[2] * tc_grad[1] + v_grid[2] * -1 * tc_grad[0]) * 3600
    if DataType.upper() == 'MXRA':
      name = r'Mixing Ratio Advection $\frac{W}{Hour}$'
      levs = np.arange(-5,6,0.5)
      c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
      mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
      cmap = mycm
      mx_grid = self.grid( datatype='MIXR' )
      mx_grad = np.gradient( mx_grid[2], 40000 )
      Advection = -1 * ( u_grid[2] * mx_grad[1] + v_grid[2] * -1 * mx_grad[0] ) * 3600
    if DataType.upper() == 'THEA':
      name = r'Theta-E (K) Advection $\frac{\theta_e}{Hour}$'
      levs = np.arange(-5,6,0.5)
      c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
      mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
      cmap = mycm
      the_grid = self.grid( datatype='THTE' )
      the_grad = np.gradient(the_grid[2],40000)
      Advection = -1 * ( u_grid[2]*the_grad[1] + v_grid[2]*-1*the_grad[0] ) * 3600
    return (X,Y,Advection,levs,cmap,name)