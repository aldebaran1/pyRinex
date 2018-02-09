#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:09:46 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""
import h5py
import yaml
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import os

def filterRxstations(rxlist='', latlim=[-90,90],lonlim=[-180,180]):
    """
    Count the total number of recivers withing lat/lon boundary. Return a 
    number. INput variable/arg "rxlist" is a hdf5 archive containtg a pool of 
    all possible receivers. Boundaries are given as lists!
    """
    fn = h5py.File(rxlist, 'r')
    lat = fn['data/table'][:,0]
    lon = fn['data/table'][:,1]
    lat = lat[~np.isnan(lat)]
    lon = lon[~np.isnan(lon)]
    idx = np.where((lat>=latlim[0]) & (lat<=latlim[1]) & \
                   (lon>=lonlim[0]) & (lon<=lonlim[1]))[0]
    return lat[idx].shape[0]

def plotRxMap(latlim=[30,65],lonlim=[-20,50],parallels=[],meridians=[],
              projection='merc', res='i', ms=15, c='r', rxlist='',save=False):
    """
    The function plots receivers' locations on a global map with a set of comp-
    limentary parameters. The parameters must be specified in adjacent .yaml
    file. The function utilizes Basemap library, and the positions are rendered
    as a scatter plot with adjustable color and marker size. 
    If you want to save a plot, use an optioanl argument "save" and set it to 
    True. The script will save the map as a PNG image in the same directory as
    the rxlist.h5 is located. If you choose this option, than the figure won't
    render in a separate figure viewer.
    """
    if rxlist != '':
        (fig,ax) = plt.subplots(1,1,figsize=(16,12),facecolor='w')
        m = Basemap(projection=projection,resolution=res,
                    lat_0 = int(np.mean(latlim)), lon_0=int(np.mean(lonlim)),
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
    
    if save:
        head, tail = os.path.split(rxlist)
        plt.savefig(head+'/rxmap_' +str(lonlim[0])+str(lonlim[1])+'_'+
                                   str(latlim[0])+str(latlim[1])+'_'+
                                   projection+'.png', dpi=300)
        plt.close()
        return
    else:
        plt.show()
        return
        
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('hdffile',type=str)
    p.add_argument('-c', '--cfg', help='yaml configuration file')
    p.add_argument('-s', '--save', help='save the plot? T/F', default=0, type=bool)
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
    
    rxnr = filterRxstations(rxlist=rxlist, latlim=latlim, lonlim=lonlim)
    # Print the number of recevers in a given lat-lon boundaries
    print (rxnr)
    # Plot the receiver positions
    plotRxMap(latlim=latlim, lonlim=lonlim, parallels=parallels, meridians=meridians,
              projection=projection, res=resolution, ms=ms, rxlist=rxlist, save=P.save)
    