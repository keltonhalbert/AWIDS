# cython: boundscheck=False

import numpy as np
import datetime
cimport cython
cimport numpy as np


cpdef tuple GetWeight( np.ndarray[double, ndim=2] gridX, np.ndarray[double, ndim=2] gridY, list xi, list yi, list zi, double Range ):
  
  cdef double RoI
  cdef double i, j, x, y, z, distance, weight
  cdef list keys
  cdef tuple grdkey
  
  ## This helps keep the weighting function balanced while saving
  ## computation power in calculating square roots
  RoI = Range * Range
  ## gridX and gridY are 2D arrays
  ## xi, yi, and zi are 1D arrays or lists
  ## RoI is the Range of Influence, given in kilometers
  dict = {}
  keys = []
  ## A dictionary to store the weights of the stations relative to each gridpoint
  ## Iterate through the 2D arrays gridX and gridY
  for GX, GY in zip( gridX, gridY ):
    for i, j in zip( GX, GY ):
      ## The key using the gridpoint to access weights
      grdkey = ( i, j )
      keys.append( grdkey )
      ## enumerate through every station relative to every gridpoint
      for x, y, z in zip( xi, yi, zi ):
        distance = ( x - i ) * ( x - i  ) + ( y - j ) * ( y - j ) 
        ## filter weight calculations based on the Range of Influence
        if distance <= RoI:
          ## Calculate the weight of the station relative to the gridpoint
          weight = 2.7182818284590451**( -( distance / RoI ) * ( distance / RoI) ) 
          ## if the gridpoint has not been used yet, create new entry
          try:
            dict[ grdkey ].append( ( z, weight) )
          ## add to existing entry for an existing gridpoint
          except KeyError:
            dict[ grdkey ] = [( z, weight)]
        else: continue
  ## return the dictionary of dict[ gridpoint ] = weight
  return ( dict, keys )

cpdef double FirstGuess( z_list, weights_list ):
  
  cpdef double first_guess
  
  ## z_list and weight_list are 1D arrays
  ## Calculate the first guess of the Barnes Analysis
  first_guess = np.sum( weights_list * z_list ) / np.sum( weights_list )
  return first_guess

 
def Interp( gridX, gridY, list xi, list yi, list zi, double RoI ):
  
  cdef list keys, interpolated_values
  cdef unsigned int ran, i
  cdef double FirstPass
  
  ## gridX and gridY are 2D arrays of points that correspond to eachother
  ## xi, yi, zi are 1D arrays or lists of corresponding values
  start_time = datetime.datetime.now()
  WeightFunc = GetWeight( gridX, gridY, xi, yi, zi, RoI )
  OADict = WeightFunc[0]
  keys = WeightFunc[1]
  ## get the weight of each observation relative to each gridpoint
  ## An empty list to store the gridpoints in propper order
  ## create an empty list for the interpolated values to be gridded
  interpolated_values = []
  ## loop through each gridpoint in ordered list keys
  for key in keys:
    obs = []
    weights = []
    ## if the gridpoint does have observations in the RoI...
    try:
      info_list = OADict[ key ]
      ## loop through the index of the dictionary value with the z values and weights
      ran = len( info_list )
      for i in xrange( ran ):
        obs.append( info_list[ i ][0] )
        weights.append( info_list[ i ][1] )
      obs = np.array( obs )
      weights = np.array( weights )
      ## calculate the first guess of the Barnes Analysis
      FirstPass = FirstGuess( obs, weights )
      ## add the interpolated values to an ordered list
      interpolated_values.append( FirstPass )
    ## if a gridpoint is not in the dictionary (i.e. there were no observations in the
    ## range of influence), assign NaN as a value
    except KeyError:
      interpolated_values.append( np.nan )
  ## turn the ordered list into an array
  result = np.array( interpolated_values )
  ## reshape the array to match the dimmensions of the given grid
  result = result.reshape( gridX.shape )
  end_time = datetime.datetime.now()
  secs = end_time - start_time
  print 'interpolation took', secs
  return result