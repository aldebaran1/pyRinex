#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 12:08:38 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""
import h5py
import yaml
import os
import glob
import numpy as np
import subprocess
from pymap3d.coordconv3d import ecef2geodetic
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

def getRxList(folder, sufix):
    filestr = os.path.join(folder,sufix)
    flist = sorted(glob.glob(filestr))
    rx = []
    for f in flist:
        head, tail = os.path.split(f)
        rx.append(tail[0:8])
    return rx

def plotRxMap(latlim=[30,65],lonlim=[-20,50],parallels=[],meridians=[],rxlist=''):
    """
    """
    if rxlist != '':
        (fig,ax) = plt.subplots(1,1,figsize=(16,12),facecolor='w')
        m = Basemap(projection='merc',resolution='i',
        llcrnrlat=latlim[0],urcrnrlat=latlim[1],llcrnrlon=lonlim[0],urcrnrlon=lonlim[1])
        m.drawcoastlines()
#        m.drawstates()
        m.drawcountries()
        m.drawparallels(parallels, labels=[1,0,0,0], linewidth=0.25)
        m.drawmeridians(meridians, labels=[0,0,0,1], linewidth=0.25)
    
    fn = h5py.File(rxlist, 'r')
    lat = fn['data/table'][:,0]
    lon = fn['data/table'][:,1]
    x,y = m(lon,lat)
    m.scatter(x,y,s=15,color='r')
    

def writeRxlist2HDF(rxfolder='/media/smrak/Eclipse2017/Eclipse/cors/all/233/',
                    sufix='*.yaml',listfn=None):
    """
    """
    if listfn is not None:
        rxlist = getRxList(rxfolder, sufix)
        c = 0
        table = np.nan*np.zeros((len(rxlist),2))
        for rx in rxlist:
            try:
                yamlfile = rxfolder+rx+'.yaml'
                stream = yaml.load(open(yamlfile, 'r'))
                rx_xyz = stream.get('APPROX POSITION XYZ')
                rec_lat, rec_lon, rec_alt = ecef2geodetic(rx_xyz[0], rx_xyz[1], rx_xyz[2])
                table[c,:] = [rec_lat, rec_lon]
                c+=1
            except Exception as e:
                print (rx)
                c+=1
        h5file = h5py.File(listfn, 'w')
        tab = h5file.create_group('data')
        tab.create_dataset('table', data=table)
        asciiList = [n.encode("ascii", "ignore") for n in rxlist]
        tab.create_dataset('rx', (len(asciiList),1),'S10', asciiList)
        h5file.close()
        
#fn = '/media/smrak/Eclipse2017/Eclipse/2017/233/'
#listfn = '/media/smrak/Eclipse2017/Eclipse/2017/rx'
#
#writeRxlist2HDF(rxfolder=fn, listfn=listfn)
#l = plotRxMap(rxlist=listfn+'.h5')

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    p.add_argument('saveto',type=str)
    P = p.parse_args()
    
    if os.path.exists(P.saveto):
        print('the file exists. Deleting and replacing: ', P.saveto)
        subprocess.call('rm -r ' + P.saveto, shell=True)
    if P.saveto[-3:] == '.h5':
        writeRxlist2HDF(rxfolder=P.folder, listfn=P.saveto)
    else: 
        writeRxlist2HDF(rxfolder=P.folder, listfn=P.saveto+'.h5')