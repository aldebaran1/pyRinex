#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:24:03 2018

@author: smrak
"""

from six.moves.urllib.parse import urlparse
import ftplib
import subprocess


def unzip(f):
    subprocess.call('gzip -d ' + f, shell=True)
    return

def download(F, rx, filename):
    print ('Downloading to: ', filename)
    try:
        with open(filename, 'wb') as h:
            F.retrbinary('RETR {}'.format(rx), h.write)
    except:
        pass

def getRinexNav(year,day,odir,const='gps'):
    """
    year,day: integer
    db: the name of the database
    odif: final directory to save the rinex files
    """
    # Parse cors url address
    url =  urlparse('ftp://geodesy.noaa.gov/cors/rinex/')
    # Correct spelling to unify the length (char) of the day in year (DOY)
    if len(str(day)) == 2:
        day = '0'+str(day)
    elif len(str(day)) == 1:
        day = '00'+str(day)
    elif len(str(day)) == 3:
        day = str(day)
    else: 
        print ('Error - day has to be a string 0-365')
    
    # Constellation navigation file variable
    sct = {'gps' : 'n',
           'glonass' : 'g',
           'gallileo' : 'e'}
    # Open a connection to the FTP address
    with ftplib.FTP(url[1],'anonymous','guest',timeout=15) as F:
        rpath = url[2] + '/' + year + '/' + day + '/'
        F.cwd(rpath)
        urlrx = 'brdc' +day + '0.' + year[-2:]+sct[const]+'.gz'
        print (urlrx)
        try:
            # urlrx must in in a format "nnnDDD0.YYo.xxx"
            download(F, urlrx, odir+urlrx)
        except Exception as e:
            print (e)
            
    unzip(odir+urlrx)
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('year',type=str)
    p.add_argument('day',type=str)
    p.add_argument('dir',type=str, help='destination directory')
    p.add_argument('-t', '--sct',type=str, help='constellation type',default='gps')
    
    P = p.parse_args()
    # Get file
    getRinexNav(P.year, P.day, P.dir, const=P.sct)
