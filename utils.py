import numpy
import h5py
import time
import datetime
from scipy import signal
from scipy import interpolate
from scipy.ndimage import gaussian_filter1d
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter
import pandas as pd
import os
import math
import splines

def unwrap_with_nan(array, discont=numpy.pi, axis=None):
    result = numpy.full_like(array, numpy.nan)

    valid_mask = ~numpy.isnan(array)
    result[valid_mask] = numpy.unwrap(array[valid_mask], discont=discont)

    return result
    
def h5_tree(val, pre=''):
    items = len(val)
    #print("items", items)
    for key, val in val.items():
        #print(key,' VAL ',val, 'ITEMS', items)
        items -= 1
        if items == 0:
            # the last item
            if type(val) == h5py._hl.group.Group:
                print(pre + '└── ' + key)
                h5_tree(val, pre+'    ')
            else:
                try:
                    print(pre + '└── ' + key + ' (%d)' % len(val))
                except TypeError:
                    print(pre + '└── ' + key + ' (scalar)')
        else:
            if type(val) == h5py._hl.group.Group:
                print(pre + '├── ' + key)
                h5_tree(val, pre+'│   ')
            else:
                try:
                    print(pre + '├── ' + key + ' (%d)' % len(val))
                    #print(val)
                except TypeError:
                    print(pre + '├── ' + key + ' (scalar)')


def set_bki(year, month, day, hour, minute, second, heightList):
    dt = datetime.datetime(year, month, day, hour, minute, second) # Create a datetime object
    timestamp = dt.timestamp() # Convert to a timestamp
    dt = time.gmtime(timestamp)
    print(dt)
    year= dt.tm_year+(dt.tm_yday-1)/364.0
    print(year)

    dh = heightList[1]-heightList[0]
    MAXNRANGENDT = len(heightList)
    h=numpy.arange(0.0,dh*MAXNRANGENDT,dh,dtype='float32')
    bfm=numpy.zeros(MAXNRANGENDT,dtype='float32')
    bfm=numpy.array(bfm,order='F')
    thb=numpy.zeros(MAXNRANGENDT,dtype='float32')
    thb=numpy.array(thb,order='F')
    bki=numpy.zeros(MAXNRANGENDT,dtype='float32')
    bki = numpy.array(bki, order='F')

    from schainpy.model.proc import mkfact_short_2020_2
    mkfact_short_2020_2.mkfact(year, h, bfm, thb, bki, MAXNRANGENDT)
    return bki
    

def normal(a,b,n,m):
    chmin=1.0e30
    chisq=numpy.zeros(150,'float32')
    temp=numpy.zeros(150,'float32')

    for i in range(2*m-1):
        an=al=be=chisq[i]=0.0
        for j in range(int(n/m)):
            k=int(j+i*n/(2*m))
            if(a[k]>0.0 and b[k]>0.0):
                al+=a[k]*b[k]
                be+=b[k]*b[k]

        if(be>0.0):
            temp[i]=al/be
        else:
            temp[i]=1.0

        for j in range(int(n/m)):
            k=int(j+i*n/(2*m))
            #print("a,b",a[k],b[k])
            if(a[k]>0.0 and b[k]>0.0):
                chisq[i]+=(numpy.log10(b[k]*temp[i]/a[k]))**2
                an=an+1

        if(chisq[i]>0.0):
            chisq[i]/=an

    for i in range(int(2*m-1)):
        #print("xi",chisq[i])
        if(chisq[i]<chmin and chisq[i]>1.0e-6):
            chmin=chisq[i]
            cf=temp[i]
    return cf

def read_hf_file(path):
    hf = h5py.File(path, 'r')
    
    data = hf['Data']
    print("data keys: ", data.keys())
    metadata = hf['Metadata']
    print("metadata keys: ", metadata.keys())
    
    data_spc_group = hf['Data']['data_spc']
    
    channels_data = []
    for channel in data_spc_group.keys():
        channel_data = data_spc_group[channel][:]
        channels_data.append(channel_data)
    spc = numpy.stack(channels_data, axis=0) 

    #spc = hf['Data']['data_spc']['channel00'][:]
    data_cspc_group = hf['Data']['data_cspc']
    pair_data = []
    for pair in data_cspc_group.keys():
        dataset = data_cspc_group[pair][:]
        pair_data.append(dataset)
    try: # 4 pairs
        cspc = numpy.stack(pair_data, axis=0)
        cspc = cspc[0]
        cspc = cspc.transpose(1,0,2,3) # (4, 32, 64, 560)
    except: # for one pair in input
        cspc = numpy.stack(pair_data, axis=0)
        cspc = cspc.transpose(1,0,2)  #(50, 64, 109)
        cspc = numpy.expand_dims(cspc, axis=0) # (1, 50, 64, 109)
        
    #cspc = hf['Data']['data_cspc']['pair00'][:]
    #print(cspc)
        
    utctime = hf['Data']['utctime'][:]
    utctime = numpy.array(utctime)

    heightList = hf['Metadata']['heightList'][:]
    heightList = numpy.array(heightList)
    
    timeZone = hf['Metadata']['timeZone']
    timeZone = numpy.array(timeZone)

    return spc, cspc, heightList, utctime, timeZone
