#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:09:46 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""

import matplotlib.pyplot as plt
import h5py
import cartopy.crs as ccrs
from cartomap import geogmap as gm

def getCoord(fn):
    fn = h5py.File(fn, 'r')
    lat = fn['data/table'][:,0]
    lon = fn['data/table'][:,1]
    
    return lon, lat

def plotMap(fn,lonlim=[],latlim=[]):
    if (len(latlim) == 0) or (len(latlim) == 1):
        latlim = [-90,90]
    if (len(lonlim) == 0) or (len(lonlim) == 1):
        lonlim = [-180,180]
    
    gm.plotCartoMap(latlim=latlim,lonlim=lonlim)
    lon, lat = getCoord(fn)
    plt.plot(lon,lat, '.r', ms=3, transform=ccrs.PlateCarree())
    plt.show()
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    
    p.add_argument('hdffile',type=str)
    p.add_argument('-x', '--lonlim', type=str)
    p.add_argument('-y', '--latlim', type=str)
    
    P = p.parse_args()
    yls = P.latlim.split(',')
    xls = P.lonlim.split(',')
    xl = list(map(int,xls))
    yl = list(map(int,yls))
    plotMap(P.hdffile, xl, yl)