# -*- coding: utf-8 -*-
"""
Created on Wed May  9 21:15:14 2018

@author: smrak
"""

import subprocess

def doPreprocessing(year, day, odir, ndir):
    """
    """
    # Correct spelling to unify the length (char) of the day in year (DOY)
    if len(str(day)) == 2:
        day = '0'+str(day)
    elif len(str(day)) == 1:
        day = '00'+str(day)
    elif len(str(day)) == 3:
        day = str(day)
    else: 
        print ('Error - day has to be a string 0-365')
    # Extended paths to files
    obsfolder = odir + year + '/' + day + '/'
    rxfolder = odir + year + '/'
    # Download the data -- Rinex observation
    subprocess.call('python download_rnxo.py {} {} {} {}'.format(
            year,day,'all',odir), shell=True)
    # Download the data -- Rinex Navigation
    subprocess.call('python download_rnxn.py {} {} {}'.format(
            year, day, ndir), shell=True)
    # Unzip & remove
    subprocess.call('python unzip_rm.py {}'.format(obsfolder), shell=True)
    # Decompress the Rinex-obs
    subprocess.call('python crx2rnx.py {}'.format(obsfolder), shell=True)
    # Convert to yaml
    subprocess.call('python rnx2yaml.py {}'.format(obsfolder), shell=True)
    # Make a rxlist-lon/lat file
    subprocess.call('python rxlist.py {} {}'.format(
            obsfolder,rxfolder), shell=True)
    # Convert to HDF5
    subprocess.call('python rnx2hdf.py {}'.format(obsfolder), shell=True)
    
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('year',type=str)
    p.add_argument('day',type=str)
    p.add_argument('odir',type=str, help='rinex observation root directory')
    p.add_argument('ndir',type=str, help='rinex navigation root directory')
    
    P = p.parse_args()
    doPreprocessing(P.year, P.day, P.odir, P.ndir)