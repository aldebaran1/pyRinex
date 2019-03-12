#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 16:32:54 2019

@author: smrak
"""

import h5py
import yaml
import os
from numpy import array, logical_and

#fn = '/media/smrak/gnss/obs/2017/147/rxlist..h5'
#ofn = '/media/smrak/gnss/obs/2017/conus147.yaml'
def getData(fn):
    fn = h5py.File(fn, 'r')
    rx = fn['data/rx'].value
    lat = fn['data/table'][:,0]
    lon = fn['data/table'][:,1]
    rxa = [str(l[0].decode('ascii')) for l in rx]
    return lon, lat, array(rxa)

def filterandsave(fn: str = None, ofn: str = None,
                  latlim: list = None,lonlim: list = None):
    """
    """
    latlim = array(latlim).astype(float)
    lonlim = array(lonlim).astype(float)

    assert ofn is not None
    if os.path.isdir(ofn):
        ofn = os.path.splitext(fn)[0] + '.yaml'
    if os.path.splitext(ofn)[1] != 'yaml':
        ofn = os.path.splitext(ofn)[0] + '.yaml'
    #Get data and locations
    x,y,r = getData(fn)
    # filter
    idx = (x >= lonlim[0]) & (x <= lonlim[1])
    idy = (y >= latlim[0]) & (y <= latlim[1])
    ix = logical_and(idx,idy)
    outd = [str(r) for r in r[ix]]
    
    # Dump to yaml
    
    f = open(ofn, 'w')
    yaml.dump({'total': len(outd), 'rx' : outd}, stream=f, default_flow_style=False, allow_unicode=1)
    f.close()
    print ("List successfully saved to ", ofn)
    return

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('rxlist', type = str, help = 'Input data (hdf5)')
    p.add_argument('ofn', type = str, help = 'Name and destination of the output file')
    p.add_argument('lonlim', help = 'Longitude limits', nargs = 2)
    p.add_argument('latlim', help = 'Latitude limits', nargs = 2)
    P = p.parse_args()
    # Get file
    filterandsave(fn = P.rxlist, ofn = P.ofn, latlim=P.latlim, lonlim=P.lonlim)