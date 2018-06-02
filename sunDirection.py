from pylab import *
from sunposition import sunpos
from datetime import datetime
from argparse import ArgumentParser
import sys

"""
    coords : ndarray, (...,2)
        The shape of the array is parameters broadcast together, plus a final dimension for the coordinates.
        coords[...,0] = observed azimuth angle, measured eastward from north
        coords[...,1] = observed zenith angle, measured down from vertical
"""
   
# group room coordinates
# lat = 57.014409272643
# lon = 9.98590855145591
# alt = 10

lat = 57.014409272643
lon = 9.98590855145591
alt = 10
time = datetime.utcnow()
az, zen, ra, dec, h = sunpos(time,lat,lon,alt)
#az,zen = sunpos(time,lat,lon,alt)
#

print("azimuth: ", az)
print("zenith: ", zen)
