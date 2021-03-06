# pyRinex: Python framework for RINEX 2.11 acquisition, file manipulation and preprocesing for Researchers and Scientists 

The pyRinex framework is a comprehansive software package for most fundamental RINEX 2.11 manupulation and 
data pre-pronessing.

The pyrinex framework was written in python 3.5, it was not yet tested on python 2! Please report bugs and suggestions to
smrak[at]bu.edu. The software is a work in progress.

Install the package as follows:
```
$ git clone https://github.com/aldebaran1/pyRinex.git
$ cd pyRinex
$ python setup.py develop
```
This will install the main `pyRinex.py` script to the chosen python workspace

The main `pyRinex.py` script includes basic pre-processing routines to make your life easier. RINEX is a compact format
but it is not practical to work with. For this purpose, we split the RINEX observation file into 2 separate files: heder into 
YAML dictionary and Observations into HDF5 archive.

The HDF5 is structured as follows:
- Observations are ordered by observation time/epoch @ major axis,
- Observations are ordered by satellite vehicle @ minor axis. GPS 1-32, GLONASS 33-60, GALILLEO 60-
- For each epoch/sv: obsrvations are in array as number of observables x 3. Where each observable has observation and eather 
phase or signal indicator/flag: 'data', 'lli', 'ssi'
- Arrays are structured ad pandas.panel4D array

Access the data as follows:
```python
data = pandas.read_hdf('path/to/file.h5')
obstimes = np.array((data.major_axis))
L1 = np.array(data['L1', satellite_vehicle, :, 'data'])
```

Header contains informations about the obervations, usually the only data you are gonna need is receiver position. 
Access the data as follows:
```python
import yaml
stream = yaml.load(open('/path/to/configurationheaderfile.yaml', 'r'))
rx_xyz = stream.get('APPROX POSITION XYZ') # ECEF coordinate system
```

Besides main file, there are util scripts for RINEX acquisition and file manipulation. Go to
```
$ cd utils/
```
### DOWNLOAD RINEX files from publicly available databases
So far, there we support CORS, CDDIS and EUREF databases. First make a directory you want to download data to than:
``` 
$ pytohn download_rnxo.py year day database /path/to/data/
```
### Unzipping
All databases provide you compressed data with .Z, .gz, or .zip extensions. Use:
```
$ python unzip_rm.py /path/to/data/
```
to extract all files in the directory. The scripts get rid of all .Z files for you.
### Decompress RINEX: .YYD extension
If the data is older than 3 months, all databases compress rinex observation files into .xxD format. To decompress the
such files, there is a CRX2RNX executable script in the /utils folder.
An automatic python script takes care of a whole folder of compressed observation files. Decompress the folder of downloaded data
as follows:
```
$ python crx2rnx.py /path/to/data/
```
### Convert Observation headers into configuration (yaml) files
Each rinex observation file starts with a header with system variables and receiver configuration. The most importnat 
informatio we always need is a receiver position in ECEF coordinate system.

An automated script converts a whole folder of rinex observation files in .xxO format into yaml files with the same name. The yaml
configuration file is a python dictionary-like txt file, with a header information in it.
Call the automated conversion script:
```
$ python rnx2yaml.py /path/to/observation/data/
```
### Convert RINEX Observation file into HDF5 database-like format
RINEX files are in an awkward format for data parsing purposes. Therefore, we convert RINEX files into a HDF5 files once, and then 
do all the processing from the HDF5 files.
Call the automated conversion script:
```
$ python rnx2hdf.py /path/to/observation/data/
```
