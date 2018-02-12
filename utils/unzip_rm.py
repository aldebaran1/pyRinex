#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:23:05 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""

import glob
import os
import subprocess
import multiprocessing
#from time import sleep

def unzip(f):
    print('Unizipping: ', f)
    subprocess.call('gzip -d ' + f, shell=True)

def unzipfolder(folder):
    suffix = ['*.gz', '*.Z', '*.zip']
    for wlstr in suffix:
        filestr = os.path.join(folder,wlstr)
        flist = sorted(glob.glob(filestr))
        for file in flist:
            p = multiprocessing.Process(target=unzip, args=(file,))
            p.start()
            p.join(2)


if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    P = p.parse_args()
    
    unzipfolder(P.folder)
