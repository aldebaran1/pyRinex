#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:19:38 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""

from six.moves.urllib.parse import urlparse
import ftplib
import numpy as np
#from os.path import expanduser
#from time import sleep

def download(F, rx, filename):
    print ('Downloading to: ', filename)
    with open(filename, 'wb') as h:
        F.retrbinary('RETR {}'.format(rx), h.write)

def getStateList(year, day, F, db):
    d = []
    stations = []
    F.retrlines('LIST', d.append)
    if db == 'cddis':
        for line in d:
            arg = line.split()[-1]
            if (arg[-2:] == '.Z') or (arg[-2:] == 'ip') or (arg[-2:] == 'gz'):
                argclober = arg.split('.')
                if (len(argclober[0]) == 8):
                    stations.append(arg)

    elif db == 'cors':
        for line in d:
            arg = line.split()[-1]
            if len(arg) == 4:
                try:
                    rx = arg+str(day)+'0.'+year[-2:]+'o.gz'
                    stations.append(rx)
                except Exception as e:
                    pass
    elif db == 'euref':
        for line in d:
            arg = line.split()[-1]
            if (arg[-2:] == '.Z') or (arg[-2:] == 'ip') or (arg[-2:] == 'gz'):
                argclober = arg.split('.')
                if (len(argclober[0]) == 8):
                    stations.append(arg)

    return np.array(stations)

def getRinexObs(year,day,db,odir):
    """
    year,day: integer
    db: the name of the database
    odif: final directory to save the rinex files
    """
    # Dictionary with complementary FTP url addresses
    urllist = {'cddis': 'ftp://cddis.gsfc.nasa.gov/gnss/data/daily/',
               'cors':  'ftp://geodesy.noaa.gov/cors/rinex/',
               'euref': 'ftp://epncb.oma.be/pub/obs/'}
    url =  urlparse(urllist[db])
    if len(str(day)) == 2:
        day = '0'+str(day)
    elif len(str(day)) == 1:
        day = '00'+str(day)
    elif len(str(day)) == 3:
        day = str(day)
    else: 
        print ('Error - day has to be a string 0-365')
    # Open a connection to the FTP address
    with ftplib.FTP(url[1],'anonymous','guest',timeout=15) as F:
        YY = str(year)[2:]
        # cd to the directory with observation rinex data
        if db == 'cddis':
            rpath = url[2] + '/' + year + '/' + day + '/'+YY+'o/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db)
            print (rxlist)
            # Download the data
            for urlrx in rxlist:
                # urlrx must in in a format "nnnDDD0.YYo.xxx"
                download(F, urlrx, odir+urlrx)
        elif db == 'cors':
            rpath = url[2] + '/' + year + '/' + day + '/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db)
            print (rxlist)
            # Download the data
            for urlrx in rxlist:
                F.cwd(rpath+urlrx[:4]+'/')
                # urlrx must in in a format "nnnDDD0.YYo.xxx"
                download(F, urlrx, odir+urlrx)
        elif db == 'euref':
            rpath = url[2] + '/' + year + '/' + day + '/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db)
            print (rxlist)
            # Download the data
            for urlrx in rxlist:
                # urlrx must in in a format "nnnDDD0.YYo.xxx"
                download(F, urlrx, odir+urlrx)
        else:
            exit()
#        F.cwd(rpath)
##        print (F.dir())
#        rxlist = getStateList(year, day, F, db)
##        print (rxlist)
#        
#        for urlrx in rxlist:
#            # urlrx must in in a format "nnnDDD0.YYo.xxx"
#            download(F, urlrx, odir+urlrx)
#            ofn = odir + rx
#            print ('Downloading from: ', ofn)
#            with open( ofn, 'wb') as h:
#                F.retrbinary('RETR {}'.format(rx), h.write)
#                sleep(1)


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
            
#year = str(2017)
#day = str(233)
#db = 'euref'
#save = 'C:\\Users\\smrak\\Google Drive\\BU\\software\\pyRinex\\utils\\tmp\\'
#getRinexObs(year,day,db,save)
if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('year',type=int)
    p.add_argument('day',type=int)
    p.add_argument('db',type=str, help='database acronym. Supporting: cddis, cors, euref')
    p.add_argument('dir',type=str, help='destination directory')
    P = p.parse_args()
    
    getRinexObs(P.year, P.day, p.db, P.dir)