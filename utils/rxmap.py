#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:09:46 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""
import h5py
import yaml
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


def plotRxMap(latlim=[30,65],lonlim=[-20,50],parallels=[],meridians=[],
              projection='merc', res='i', ms=15, c='r', rxlist=''):
    """
    """
    if rxlist != '':
        (fig,ax) = plt.subplots(1,1,figsize=(16,12),facecolor='w')
        m = Basemap(projection=projection,resolution=res,
                    lat_0 = latlim[1]/2, lon_0=lonlim[1]/2,
                    llcrnrlat=latlim[0],urcrnrlat=latlim[1],
                    llcrnrlon=lonlim[0],urcrnrlon=lonlim[1])
        m.drawcoastlines()
#        m.drawstates()
        m.drawcountries()
        m.drawparallels(parallels, labels=[1,0,0,0], linewidth=0.25)
        m.drawmeridians(meridians, labels=[0,0,0,1], linewidth=0.25)

    fn = h5py.File(rxlist, 'r')
    lat = fn['data/table'][:,0]
    lon = fn['data/table'][:,1]
    x,y = m(lon,lat)
    m.scatter(x,y,s=ms,color=c)
    plt.show()
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('hdffile',type=str)
    p.add_argument('-c', '--cfg', help='yaml configuration file')
    P = p.parse_args()
    
    cfg_file = P.cfg
    rxlist = P.hdffile
    # YAML: map configs
    stream = yaml.load(open(cfg_file, 'r'))
    lonlim = stream.get('lonlim')
    latlim = stream.get('latlim')
    projection = stream.get('projection')
    resolution = stream.get('resolution')
    ms = stream.get('marker_size')
    c = stream.get('marker_color')
    parallels = stream.get('parallels')
    meridians = stream.get('meridians')
    
    plotRxMap(latlim=latlim, lonlim=lonlim, parallels=parallels, meridians=meridians,
              projection=projection, res=resolution, ms=ms, rxlist=rxlist)
    