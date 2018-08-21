#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  3 13:19:38 2017

@author: Sebastijan Mrak <smrak@gmail.com>
"""

from six.moves.urllib.parse import urlparse
import ftplib
import numpy as np
import yaml
import os
import subprocess
import platform

def download(F, rx, filename):
    path, tail = os.path.split(filename)
    if not os.path.exists(path):
        try:
            subprocess.call('mkdir ' + path, shell=True)
        except:
            print ('Cant make the directory')
    if not os.path.exists(filename[:-5]):
        print ('Downloading file: {}'.format(tail))
        try:
            with open(filename, 'wb') as h:
                F.retrbinary('RETR {}'.format(rx), h.write)
        except:
            pass
    else:
        print ('{} File already exists'.format(tail))
def getSingleRxUrl(year, day, F, db, rxn):
    d = []
    F.retrlines('LIST', d.append)
    # Find the files
    # CDDIS db
    if db == 'cddis':
        if isinstance(rxn, str):
            match = rxn + day + '0.' + year[-2:] + 'o.Z'
        elif isinstance(rxn, list):
            match = [r + day + '0.'+year[-2:]+'o.Z' for r in rxn]
            match = np.array(match)
        ds = [line.split()[-1] for line in d]
        ds = np.array(ds)
        idrx = np.where(np.isin(ds,match))[0]
        if idrx.shape[0] > 0:
            stations = ds[idrx]
        
    # CORS db
    elif db == 'cors':
        match = rxn
        ds = [line.split()[-1] for line in d]
        ds = np.array(ds)
        idrx = np.where(np.isin(ds,match))[0]
        if idrx.shape[0] > 0:
            suffix = day+'0.'+year[-2:]+'d.Z'
            stations = [st+suffix for st in ds[idrx]]
            stations = np.array(stations)
    # EUREF db
    elif db == 'euref':
        if isinstance(rxn, str):
            match = rxn.upper() + day + '0.'+year[-2:]+'D.Z'
        elif isinstance(rxn, list):
            match = [r.upper() + day + '0.' + year[-2:] + 'D.Z' for r in rxn]
            match = np.array(match)
        ds = [line.split()[-1] for line in d]
        ds = np.array(ds)
        idrx = np.where(np.isin(ds,match))[0]
        if idrx.shape[0] > 0:
            stations = ds[idrx]
    # UNAVCO db
    elif db == 'unavco':
        if isinstance(rxn, str):
            match =rxn + day + '0.'+year[-2:]+'d.Z'
        elif isinstance(rxn, list):
            match = [r + day + '0.'+year[-2:]+'d.Z' for r in rxn]
            match = np.array(match)
        ds = [line.split()[-1] for line in d]
        ds = np.array(ds)
        idrx = np.where(np.isin(ds,match))[0]
        if idrx.shape[0] > 0:
            stations = ds[idrx]
        
    # Return
    return stations
def getStateList(year, day, F, db, rxn=None):
    if isinstance(rxn, str):
        stations = getSingleRxUrl(year,day,F,db,rxn=rxn)
    elif isinstance(rxn, list):
        stations = getSingleRxUrl(year,day,F,db,rxn=rxn)
        print (stations)
    else:
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
                if (len(arg) == 4):
                    try:
                        rx = arg+str(day)+'0.'+year[-2:]+'d.Z'
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
                        
        elif db == 'unavco':
            for line in d:
                arg = line.split()[-1]
                if (arg[-3:] == 'd.Z'):
                    stations.append(arg)
    
    return stations

def getRinexObs(year,day,db,odir,rx=None, dllist=None):
    """
    year,day: integer
    db: the name of the database
    odif: final directory to save the rinex files
    """
    # Designator
    if platform.system() == 'Linux':
        des = '/'
    elif platform.system() == 'Windows':
        des = '\\'
    # Dictionary with complementary FTP url addresses
    urllist = {'cddis': 'ftp://cddis.gsfc.nasa.gov/gnss/data/daily/',
               'cors':  'ftp://geodesy.noaa.gov/cors/rinex/',
               'euref': 'ftp://epncb.oma.be/pub/obs/',
               'unavco': 'ftp://data-out.unavco.org/pub/rinex/obs/',
               'ring': 'ftp://bancadati2.gm.ingv.it:2121/OUTGOING/RINEX30/RING/'}
    url =  urlparse(urllist[db])
    # Correct spelling to unify the length (char) of the day in year (DOY)
    if len(str(day)) == 2:
        day = '0'+str(day)
    elif len(str(day)) == 1:
        day = '00'+str(day)
    elif len(str(day)) == 3:
        day = str(day)
    else: 
        print ('Error - day has to be a string 0-365')
        
    # Complete the save directory path
    odir += year + des
    if not os.path.exists(odir):
        try:
            subprocess.call('mkdir ' + odir, shell=True)
        except:
            print ('Cant make the directory')
    odir += day + des
    if not os.path.exists(odir):
        try:
            subprocess.call('mkdir ' + odir, shell=True)
        except:
            print ('Cant make the directory')
    # Reasign dllist from yaml into rx [list]
    if dllist is not None and isinstance(dllist,str):
        if dllist[-5:] == '.yaml':
            stream = yaml.load(open(dllist, 'r'))
            rx = stream.get('dllist')
        else:
            exit()
            
    # Open a connection to the FTP address
    with ftplib.FTP(url[1],'anonymous','guest',timeout=15) as F:
        YY = str(year)[2:]
        
        # cd to the directory with observation rinex data
        if db == 'cddis':
            rpath = url[2] + '/' + year + '/' + day + '/'+YY+'o/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db, rxn=rx)
            print (rxlist)
            # Download the data
            print ('Downloading to: ', odir)
            for urlrx in rxlist:
                # urlrx must in in a format "nnnDDD0.YYo.xxx"
                download(F, urlrx, odir+urlrx)
        elif db == 'cors':
            rpath = url[2] + '/' + year + '/' + day + '/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db, rxn=rx)
            print (rxlist)
            # Download the data
            print ('Downloading to: ', odir)
            for urlrx in rxlist:
                try:
                    F.cwd(rpath+urlrx[:4]+'/')
                    # urlrx must in in a format "nnnDDD0.YYo.xxx"
                    download(F, urlrx, odir+urlrx)
                except:
                    pass
        elif db == 'euref':
            rpath = url[2] + '/' + year + '/' + day + '/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db, rxn=rx)
            print (rxlist)
            # Download the data
            print ('Downloading to: ', odir)
            for urlrx in rxlist:
                # urlrx must in in a format "nnnDDD0.YYo.xxx"
                download(F, urlrx, odir+urlrx)
        elif db == 'unavco':
            rpath = url[2] + '/' + year + '/' + day + '/'
            F.cwd(rpath)
            # Get the name of all avaliable receivers in the direcotry
            rxlist = getStateList(year, day, F, db, rxn=rx)
            print (rxlist)
            # Download the data
            print ('Downloading to: ', odir)
            for urlrx in rxlist:
                # urlrx must in in a format "nnnDDD0.YYo.xxx"
                download(F, urlrx, odir+urlrx)
        else:
            exit()

if __name__ == '__main__':
    from argparse import ArgumentParser
    p = ArgumentParser()
    p.add_argument('year',type=str)
    p.add_argument('day',type=str)
    p.add_argument('db',type=str, help='database acronym. Supporting: cddis, \
                   cors, euref')
    p.add_argument('dir',type=str, help='destination directory')
    p.add_argument('-r', '--rx', type=str, help='download a single file for a \
                   given receiver (4 letters)', default=None)
    p.add_argument('-l', '--dllist', type=str, help='A list of receiver names to \
                   be downloaded in yaml cfg format. Look at the example file \
                   dl_list.yaml', default=None)
    P = p.parse_args()
    if P.db == 'all':
        a = ['cors', 'cddis', 'euref', 'unavco']
        for db in a:
            getRinexObs(P.year, P.day, db, P.dir, rx=P.rx, dllist=P.dllist)
            
    else:
        getRinexObs(P.year, P.day, P.db, P.dir, rx=P.rx, dllist=P.dllist)
            