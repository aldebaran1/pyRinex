#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 13:25:38 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""
import os
import glob
from time import sleep
from gsit import pyRinex

def convertObs2HDF(folder=None, sufix=None):
    """
    This script converts RINEX 2.11 observation files in a given directory into
    a hdf5 organized data structure, utilizing pyRINEX script. Find the script
    in the main directory.
    """
    if sufix is None:
        wlist = ['*.**o', '*.**O']
    else:
        wlstr = sufix
    for wlstr in wlist:
        filestr = os.path.join(folder,wlstr)
        flist = sorted(glob.glob(filestr))
        for file in flist:
            print (file)
            head, tail = os.path.split(file)
            rx = tail[0:8]
            newfile = head + '/' + rx + '.h5'
            if not os.path.exists(newfile):
                print ('Converting file: ', file)
                try:
                    pyRinex.writeRinexObs2Hdf(file)
                except Exception as e:
                    print (e)
                sleep(1)
                
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    p.add_argument('-s', '--sufix', help='specify a sufix for desired observation files', type=str, default=None)
    P = p.parse_args()
    
    convertObs2HDF(folder = P.folder, sufix=P.sufix)