#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 10:38:16 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""

import glob
import os
import subprocess


def crx2rx(folder):
    """
    """
    suffix = ['*.**D', '*.**d']
    for wlstr in suffix:
        filestr = os.path.join(folder,wlstr)
        flist = sorted(glob.glob(filestr))
        for f in flist:
            print('Decompressing: ', f)
            subprocess.call('./CRX2RNX ' + f, shell=True)
            print('Deleting: ', f)
            subprocess.call('rm -r ' + f, shell=True)
    suffix = '*.crx'
    filestr = os.path.join(folder,suffix)
    flist = sorted(glob.glob(filestr))
    for f in flist:
        print('Deleting: ', f)
        subprocess.call('rm -r ' + f, shell=True)

        
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    P = p.parse_args()
    
    crx2rx(P.folder)