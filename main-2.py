from doctest import ELLIPSIS_MARKER
#from this import d
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy
import h5py
import time
from scipy import signal
import matplotlib.dates as mdates
import matplotlib as mpl
from scipy import interpolate
import os
import splines
import math
import csaps
import sys
import datetime
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter
from scipy.ndimage import gaussian_filter1d
mpl.rcParams['timezone'] = 'America/Lima'
matplotlib.use("Agg")
script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
os.chdir(script_dir)

from utils import set_bki, normal, read_hf_file, getNoise, getPower, getVelRange, fill_nan_linear
from write_utils import write_routine


global heightList

dirr = '/home/david/Documents/DATA-2/Valley/25_28_Aug_26/28_Aug_26/d2026240/'
output_dir = '/home/david/Documents/DATA-3/Valley/25_28_Aug_26/28_Aug_26/main-2'
os.makedirs(output_dir, exist_ok=True)


#--- Read Data
utctime_all = []
all_files=os.listdir(dirr) #Get the list of all files in directory
files = [ fname for fname in all_files if fname.endswith('.hdf5')]
files=sorted(files) #Sort the files in ascending numerical order
print("files: ", files)

# Initialize empty NumPy arrays for all variables
spc_aux = None
cspc_aux = None
utctime = numpy.array([])

for file in files[:]: #files[3:4]
    print("file: ", file)
    #spc_aux, cspc_aux, heightList, utctime, timeZone = read_hf_file(dirr + file)

     # Read the data from the file (this line remains unchanged)
    spc_aux_temp, cspc_aux_temp, heightList, utctime_temp, timeZone = read_hf_file(dirr + file)
    #print(utctime_temp.shape)
    
    utctime = numpy.concatenate((utctime, utctime_temp))
    print(utctime.shape)
    if spc_aux is None:
        spc_aux, cspc_aux = spc_aux_temp, cspc_aux_temp
        continue

    # Concatenate the current arrays with the existing ones
    spc_aux = numpy.concatenate((spc_aux, spc_aux_temp),axis=1)
    cspc_aux = numpy.concatenate((cspc_aux, cspc_aux_temp),axis=1)
    

    print(utctime.shape,spc_aux.shape,cspc_aux.shape)

print(utctime[0])
print(datetime.datetime.fromtimestamp(utctime[0], tz=datetime.timezone.utc))

#--- Manage Data

#spc = spc_aux.transpose(1,0,2,3)
#cspc = cspc_aux.transpose(1,0,2,3)

spc = spc_aux
cspc = cspc_aux
# Spectra arranged in the order of: Channel, DataTime, FFTPoint, Heigh 

#-- Manage data
data_spc = numpy.array(spc)
data_cspc = numpy.array(cspc)

print("data_spc.shape ", data_spc.shape)
print("data_cspc.shape ", data_cspc.shape)
spc = data_spc
cspc = data_cspc


print("spc.shape ", data_spc.shape)
print("cspc.shape ", data_cspc.shape)