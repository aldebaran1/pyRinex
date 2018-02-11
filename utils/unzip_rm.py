#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 12:23:05 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""

import glob
import os
import subprocess
from time import sleep

#folder = '/home/smrak/sharedrive/cors/al/184/'
def unzipfolder(folder):
    suffix = ['*.gz', '*.Z']
    for wlstr in suffix:
#    wlstr ='*.gz'
        filestr = os.path.join(folder,wlstr)
        flist = glob.glob(filestr)
        for file in flist:
            print('Unizipping: ', file)
            subprocess.call('gzip -d ' + file, shell=True)
            sleep(5)
#for file in flist:
#    print('Deleting: ', file)
#    subprocess.call('rm -r ' + file, shell=True)
#    sleep(3)

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('folder',type=str)
    P = p.parse_args()
    
    unzipfolder(P.folder)
