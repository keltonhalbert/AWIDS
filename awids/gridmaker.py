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
import barnesinterp
import solver

class GRIDMAKER( object ):

  def __init__( self, **kwargs ):
    if kwargs.get('StationDict') == 'mesonet.npz':
      self.StationDict = np.load( os.path.join( os.path.dirname(__file__), 'mesonet.npz' ) ) 
    else:
      self.StationDict = np.load( os.path.join( os.path.dirname(__file__), 'stations.npz' ) )
    if kwargs.get( 'GridFile' ) == 'mesonet_oa.npz':
      self.GridFile = np.load( os.path.join( os.path.dirname(__file__), 'mesonet_oa.npz' ) )
    else:
      self.GridFile = np.load( os.path.join( os.path.dirname(__file__), 'sfcoa_lonlats.npz' ) )
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
    c = [(0.0,'#FFFFFF'), (0.2,'#66FF33'), (0.3,'#006600'), (0.4,'#00FFFF'), (0.5,'#000099'), (0.7, '#FF0000'), (1.0, '#FF00CC')]
    mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
    plotparms = { 'TMPF': ('Temperature (F)', np.arange(-14,110,2), plt.cm.spectral), 'TMPC': ('Temperature (C)', np.arange(-25,44,1), plt.cm.spectral), 'DWPF': ('Dewpoint (F)', np.arange(0,80,2), plt.cm.BrBG), 'DWPC': ('Dewpoint (C)', np.arange(-20,26,1), plt.cm.BrBG), 'WSPD': ('Windspeed (kts)', np.arange(5,50,5), plt.cm.cool), 'PRES': ('Sea Level Pressure (mb)', np.arange(825,1050,5), plt.cm.spectral), 'THTA': (r'Theta (K) $\theta$', np.arange(250,322,2), plt.cm.spectral), 'MIXR': (r'Mixing Ratio $\frac{g}{kg}$', np.arange(0,28,1), plt.cm.gist_earth_r), 'THTE': (r'Theta-E (K) $\theta_e$', np.arange(240,400,5), plt.cm.spectral), 'RELH': ('Relative Humidity (%)', np.arange(0,101,1), plt.cm.spectral), 'UWIN': ('U component of wind (kts)', np.arange(-50,50,2), plt.cm.BrBG), 'VWIN': ('V component of wind (kts)', np.arange(-50,50,2), plt.cm.BrBG), 'UMET': ('U component of wind (m/s)', np.arange(-50,50,2), plt.cm.BrBG), 'VMET': ('V component of wind (m/s)', np.arange(-50,50,2), plt.cm.BrBG), 'VISI': ('Surface Visibility (Miles)', np.arange(0,13,1), plt.cm.pink ), 'RAIN': ('Precipitation Since 00Z', np.arange(0,100,1), mycm) }
    StationID = DataDict.keys()
    data_to_plot = []
    lons = []
    lats = []
    name = plotparms[ DataType ][0]
    cmap = plotparms[ DataType ][2]
    levs = plotparms[ DataType ][1]
    for S in StationID:
      dat = DataDict[ S ][ DataType ]
      if np.isnan( dat ) == True: continue
      else:
        if not S in self.StationDict.keys(): continue
        else:
          data_to_plot.append( dat )
          lon_lat_tuple = self.StationDict[ S ]
          lons.append( lon_lat_tuple[0] )
          lats.append( lon_lat_tuple[-1] )
    xi, yi = self.m( lons, lats )
    X, Y = self.m( self.gridlons, self.gridlats )
    Z = barnesinterp.Interp( X, Y, xi, yi, data_to_plot, 50000)
   # Z = griddata( xi, yi, data_to_plot, X, Y, interp='nn' )
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
      hour_1 = self.TriangulateKinematics( datatype=plotparms[ DataType ][-1], datdict=DataDict )
      hour_3 = self.TriangulateKinematics( datatype=plotparms[ DataType ][-1], datdict=TendDict )
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
     # Z = ( v_grad[1] - -1 * u_grad[0] ) * pow( 10, 5 )
      Z = ( v_grad[1] - -1 * u_grad[0] )
    if DataType.upper() == 'DIVR':
      name = 'Surface Divergence ($S^{-1}*{10^5}$)'
      levs = np.arange( -25, 26, 1 )
      c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
      mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
      cmap = mycm
      Z = ( u_grad[1] + -1 * v_grad[0] )
    return ( X, Y, Z, levs, cmap, name )

  def TriangulateKinematics( self, **kwargs ):
    DataType = kwargs.get( 'datatype' )
    DataDict = kwargs.get( 'datdict' )
    stations = self.StationDict.keys()
    filename = kwargs.get( 'filename', 'mesonet.npz' )
    triangulate = solver.triangulate( DataDict )
    triangles = triangulate[2]
    centers = triangulate[0]
    x = triangulate[-2]
    y = triangulate[-1]
    cent = []
    data_to_plot = []
    cx = []
    cy = []
    c = [(0.0,'#29452B'), (0.4,'#89FC92'), (0.5,'#FEFEFE'), (0.6,'#FFAE00'), (1.0,'#7A4E1B')]
    mycm=mpl.colors.LinearSegmentedColormap.from_list('mycm',c)
    for idx, t in enumerate( triangles ):
      index = [ t[0], t[1], t[2] ]
      centers[ idx ] = np.array( [ x[ t ].mean(), y[ t ].mean() ] )
      c = centers[ idx ]
      x_points = x[ index ]
      y_points = y[ index ]
      x1,y1 = x_points[0], y_points[0]
      x2,y2 = x_points[1], y_points[1]
      x3,y3 = x_points[2], y_points[2]
      for stn in stations:
        stn_x,stn_y = self.m( self.StationDict[ stn ][0], self.StationDict[ stn ][1] )
        if ( stn_x, stn_y ) == ( x1, y1 ):
          stn1 = stn
        if ( stn_x, stn_y ) == ( x2, y2 ):
          stn2 = stn
        if ( stn_x, stn_y ) == ( x3, y3 ):
          stn3 = stn
      u1,u2,u3 = DataDict[ stn1 ][ 'UMET' ],DataDict[ stn2 ][ 'UMET' ],DataDict[ stn3 ][ 'UMET' ]
      v1,v2,v3 = DataDict[ stn1 ][ 'VMET' ],DataDict[ stn2 ][ 'VMET' ],DataDict[ stn3 ][ 'VMET' ]
      kinematics = solver.kinematic_solver( u1,u2,u3, v1,v2,v3, x1,x2,x3, y1,y2,y3 )
      cx.append( c[0] )
      cy.append( c[1] )
      if DataType == 'VORT':
        data_to_plot.append( kinematics[3] * pow(10,5) )
        levs = np.arange( 1, 21, 1 )
        cmap = plt.cm.gist_heat_r
      if DataType == 'DIVR':
        data_to_plot.append( kinematics[2] * pow(10,5) )
        levs = np.arange( -25, 26, 1 )
        cmap = mycm
    X, Y = self.m( self.gridlons, self.gridlats )
    Z = barnesinterp.Interp( X, Y, cx, cy, data_to_plot, 60000)
    return ( X, Y, Z, levs, cmap, 'Surface Divergence' )
  
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
