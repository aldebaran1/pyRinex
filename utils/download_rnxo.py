#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:19:38 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""

from six.moves.urllib.parse import urlparse
import ftplib
from os.path import expanduser
from time import sleep

def getStateList(year, day, F):
#    url =  urlparse(url+year+'/'+day+'/')# 'ftp://geodesy.noaa.gov'
#    lib = ftplib.FTP(url[1],'anonymous','guest',timeout=15)
#    lib.cwd(url[2])
    d = []
    stations = []
    F.retrlines('LIST', d.append)
    for line in d:
        stations.append(line[:4])
    
    return np.array(stations)

def getRinexObs(year,day,db,odir):
    """
    year,month,day: integer
    hour, minute:  start,stop integer len == 2
    """
    
    urllist = {'cddis': 'ftp://cddis.gsfc.nasa.gov/gnss/data/daily/',
               'cors':  'ftp://geodesy.noaa.gov/cors/rinex/',
               'euref': 'ftp://www.epncb.oma.be/ftp/obs/'}
    url =  urlparse(urllist[db])
    if len(str(day)) == 2:
        day = '0'+str(day)
    elif len(str(day)) == 1:
        day = '00'+str(day)
    elif len(str(day)) == 3:
        day = str(day)
    else: 
        print ('Error - day has to be a string 0-365')

#%% get available files for this day
    with ftplib.FTP(url[1],'anonymous','guest',timeout=15) as F:
        YY = str(year)[2:]
        if db == 'cddis':
            rpath = url[2] + '/' + year + '/' + day + '/'+YY+'o/'
        F.cwd(rpath)
        
        rxlist = getStateList(year, day, F)
        for rx in rxlist:
            filename = rx + day + '0.' + YY + 'o.Z'
            #download observation file
            ofn = odir + filename
            print ('Downloading from: ', ofn)
            with open( ofn, 'wb') as h:
                F.retrbinary('RETR {}'.format(filename), h.write)
                sleep(1)
        #download navigation file
#        elif ftype == 'nav':
#            fn_year = str(year)[2:]
#            rpath2 = url[2] + '/' + str(year) + '/' + day + '/'
#            F.cwd(rpath2)
#            navfilename = 'brdc' + day + '0.' + fn_year + 'n.gz'
#            ofn = odir + navfilename
#            print ('Downloading: ', ofn)
#            with open(ofn, 'wb') as h:
#                F.retrbinary('RETR {}'.format(navfilename), h.write)
#                sleep(1)
        else: 
            print ('Wrong file format -t')
            
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('year',type=int)
    p.add_argument('day',type=int)
    p.add_argument('db',type=str, help='database acronym. Supporting: cddis, cors, euref')
    p.add_argument('dir',type=str, help='destination directory')
    P = p.parse_args()
    
    getRinexObs(P.year, P.day, p.db, P.dir)