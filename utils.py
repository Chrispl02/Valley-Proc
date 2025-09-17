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

    #from schainpy.model.proc import mkfact_short_2020_2
    import mkfact_short_2020_2
    print("mkfact location", mkfact_short_2020_2)
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



### get noise utils

def hildebrand_sekhon(data, navg):
    """
    This method is for the objective determination of the noise level in Doppler spectra. This
    implementation technique is based on the fact that the standard deviation of the spectral
    densities is equal to the mean spectral density for white Gaussian noise

    Inputs:
        Data    :    heights
        navg    :    numbers of averages

    Return:
        mean    :    noise's level
    """

    sortdata = numpy.sort(data, axis=None)
    #print(numpy.shape(data))
    #exit()
    
    lenOfData = len(sortdata)
    nums_min = lenOfData*0.2

    if nums_min <= 5:

        nums_min = 5

    sump = 0.
    sumq = 0.

    j = 0
    cont = 1

    while((cont == 1)and(j < lenOfData)):

        sump += sortdata[j]
        sumq += sortdata[j]**2

        if j > nums_min:
            rtest = float(j)/(j-1) + 1.0/navg
            if ((sumq*j) > (rtest*sump**2)):
                j = j - 1
                sump = sump - sortdata[j]
                sumq = sumq - sortdata[j]**2
                cont = 0

        j += 1

    lnoise = sump / j
    
    return lnoise


def getNoisebyHildebrand(data_spc, xmin_index=None, xmax_index=None, ymin_index=None, ymax_index=None):
    """
    Determino el nivel de ruido usando el metodo Hildebrand-Sekhon

    Return:
        noiselevel
    """
    nChannels = 2
    noise = numpy.zeros(nChannels)

    for channel in range(nChannels):
        #print(self.data_spc[0])
        #exit(1)
        daux = data_spc[channel,xmin_index:xmax_index, ymin_index:ymax_index]
        #print("daux",daux)
        noise[channel] = hildebrand_sekhon(daux, 1) # nIncohInt

    return noise

def getNoise(data_spc, xmin_index=None, xmax_index=None, ymin_index=None, ymax_index=None):
        noise = getNoisebyHildebrand(data_spc, xmin_index, xmax_index, ymin_index, ymax_index)
        return noise

def getPower(data_spc, normFactor):
    z = (data_spc.astype(numpy.float32, copy=False) / normFactor)
    z[~numpy.isfinite(z)] = numpy.nan
    avg = numpy.nanmean(z, axis=1)
    return 10 * numpy.log10(avg, where=(avg>0), out=numpy.full_like(avg, numpy.nan))

def getVelRange(Vmax, nFFTPoints, ippFactor, extrapoints=0):

    deltav = Vmax / (nFFTPoints * ippFactor)
    velrange = deltav * (numpy.arange(nFFTPoints + extrapoints) - nFFTPoints / 2.)

    return velrange