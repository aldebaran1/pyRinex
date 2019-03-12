#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:09:46 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""

import matplotlib.pyplot as plt
import h5py
from numpy import array
import cartopy.crs as ccrs
from cartomap import geogmap as gm
import os

def getCoord(fn):
    fn = h5py.File(fn, 'r')
    lat = fn['data/table'][:,0]
    lon = fn['data/table'][:,1]
    
    return lon, lat

def plotMap(fn,lonlim=None,latlim=None):
    if latlim is None:
        latlim = [-89.5,89.5]
    if lonlim is None:
        lonlim = [-179.5,180]
    else:
        latlim = array(latlim, dtype=float)
        lonlim = array(lonlim, dtype=float)
    gm.plotCartoMap(latlim=latlim,lonlim=lonlim, projection='merc')
    lon, lat = getCoord(fn)
    root, fname = os.path.split(fn)
    plt.title(fname)
    for i in range(lon.shape[0]):
        plt.plot(lon[i],lat[i], '.r', ms=3, transform=ccrs.PlateCarree())
    plt.show()
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    
    p.add_argument('hdffile',type=str)
    p.add_argument('-x', '--lonlim', type=str, nargs=2, default = None)
    p.add_argument('-y', '--latlim', type=str, nargs=2, default = None)
    
    P = p.parse_args()
    plotMap(P.hdffile, P.lonlim, P.latlim)