#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:21:58 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""

import os
import glob
from time import sleep
from gsit import pyRinex

def convertObs2HDF(folder=None, sufix=None):
    """
    This script converts headers from the RINEX 2.11 observation files in a 
    YAML configuration file, organized as a dictionary, utilizing pyRINEX 
    script. Find the script in the main directory.
    """
    if sufix is None:
        wlist = ['*.**o', '*.**O']
    for wlstr in wlist:
        filestr = os.path.join(folder,wlstr)
        flist = sorted(glob.glob(filestr))
        for file in flist:
            head, tail = os.path.split(file)
            rx = tail[0:8]
            newfile = head + '/' + rx + '.yaml'
            if not os.path.exists(newfile):
                print ('Converting file: ', file)
                try:
                    pyRinex.writeRinexObsHeader2yaml(file)
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