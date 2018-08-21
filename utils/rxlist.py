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
from numpy import nan, zeros
from pymap3d import ecef2geodetic

def getRxList(folder, sufix):
    filestr = os.path.join(folder,sufix)
    flist = sorted(glob.glob(filestr))
    rx = []
    for f in flist:
        head, tail = os.path.split(f)
        rx.append(tail[0:8])
    return rx

def writeRxlist2HDF(obsfolder='/media/smrak/Eclipse2017/Eclipse/cors/all/233/',
                    sufix='*.yaml',listfilename=None):
    """
    Make a list of receivers in a given folder, ordered by their geographical
    location. The list is organized as hdf5 file.
    "obsfolder" is path to the folder with RINEX files, which need to be first
    converted into .yaml cfg file containing their header information. 
    "listfilename" is the wanted filename which will contain converted lat/lon
    information. Itshould contain path/to/file.h5, if you forget .h5 extension,
    it will auto make one for you.
    """
    rxlist = getRxList(obsfolder, sufix)
    head, tail = os.path.split(listfilename)
    print (tail)
    if tail == '':
        print (rxlist[0])
        listfilename+='list' + rxlist[0][4:8] + '.h5'
    if listfilename[-3:] != '.h5':
        listfilename+='.h5'
    print ('NUmber of receivers in the folder: ', len(rxlist))
    print ('Saving as: ', listfilename)
    c = 0
    table = nan*zeros((len(rxlist),2))
    for rx in rxlist:
        try:
            yamlfile = obsfolder+rx+'.yaml'
            stream = yaml.load(open(yamlfile, 'r'))
            rx_xyz = stream.get('APPROX POSITION XYZ')
            rec_lat, rec_lon, rec_alt = ecef2geodetic(rx_xyz[0], rx_xyz[1], rx_xyz[2])
            table[c,:] = [rec_lat, rec_lon]
            c+=1
        except Exception as e:
            print ('Couldnt process: ', rx)
            c+=1
    h5file = h5py.File(listfilename, 'w')
    tab = h5file.create_group('data')
    tab.create_dataset('table', data=table)
    asciiList = [n.encode("ascii", "ignore") for n in rxlist]
    tab.create_dataset('rx', (len(asciiList),1),'S10', asciiList)
    h5file.close()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    p.add_argument('saveto',type=str)
    p.add_argument('-n', '--filename', help='list filename',type=str, default='')
    P = p.parse_args()
    

    if P.filename == '':
        writeRxlist2HDF(obsfolder=P.folder, listfilename=P.saveto)
    else: 
        writeRxlist2HDF(obsfolder=P.folder, listfilename=P.saveto+P.filename)