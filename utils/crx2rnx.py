#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 10:38:16 2018

@author: Sebastijan Mrak <smrak@bu.edu>
"""

import glob
import os
import subprocess
import platform

def unzip(f):
    if platform.system() == 'Linux':
        try:
            print('Decompressing: ', f)
            subprocess.call('./CRX2RNX ' + f, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
            print('Deleting: ', f)
            subprocess.call('rm -r ' + f, shell=True)
        except:
            print('Problems with: ',f)
    elif platform.system() == 'Windows':
        try:
            print('Decompressing: ', f)
            subprocess.call('crx2rnx.exe {}'.format(f), shell=True, timeout=5)
            print('Deleting: ',f)
            subprocess.call('del {}'.format(f), shell=True,timeout=5)
        except:
            print('Problems with: ',f)
        
    return

def crx2rx(folder):
    """
    A function utilizin CRX2RNX script to decompress the RINEX observation 
    files with a *.YYd extension into a *.YYo extension. 
    The script also removes all unnecessary junk from the given directory e.g.,
    .crx and .YYd files.
    The input is a directory, and it automatically finds all files needed to be
    decompressed.
    """
    suffix = ['*.**D', '*.**d']
    for wlstr in suffix:
        filestr = os.path.join(folder,wlstr)
        flist = sorted(glob.glob(filestr))
        for f in flist:
            unzip(f)
    
    suffix.append('*.crx')
    for suffix in suffix:
        filestr = os.path.join(folder,suffix)
        flist = sorted(glob.glob(filestr))
        for f in flist:
            if platform.system() == 'Linux':
                print('Deleting: ', f)
                subprocess.call('rm -r ' + f, shell=True)
            elif platform.system() == 'Windows':
                print('Deleting: ', f)
                subprocess.call('del {}'.format(f), shell=True,timeout=5)

        
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    P = p.parse_args()
    
    crx2rx(P.folder)