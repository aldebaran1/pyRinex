#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:23:05 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""

import glob
import os
import subprocess
from threading import Thread
def unzip(f):
    subprocess.call('gzip -d ' + f, shell=True)
    return

def unzipfolder(folder):
    suffix = ['*.gz', '*.Z', '*.zip']
    for wlstr in suffix:
        filestr = os.path.join(folder,wlstr)
        flist = sorted(glob.glob(filestr))
        c = 1
        for file in flist:
            print('Unizipping: ' +str(c) + '/'+str(len(flist)+1))
            thread = Thread(target=unzip, args = (file, ))
            thread.start()
            thread.join(5)
            c+=1

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    P = p.parse_args()
    
    unzipfolder(P.folder)
