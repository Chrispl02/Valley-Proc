from doctest import ELLIPSIS_MARKER
from this import d
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

from utils import unwrap_with_nan, h5_tree, set_bki, normal, read_hf_file, getNoise, getPower, getVelRange
from write_utils import write_routine
#plt.show = lambda: None  # Override plt.show to do nothing


#####################################################################
#
#
#
global heightList
dirr = '/media/cportilla/HDD/Valley/FaradayInt/d2024278/'
#dirr = '/media/cportilla/HDD/Valley/FaradayInt/1min/d2024276/'
#irr = '/media/cportilla/HDD/Valley/2024_05/spc/FaradayInt/d2024150/'
dirr = '/media/cportilla/HDD/Data/Valley/08_13_pair23/d2025225/'
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
    
    utctime = numpy.concatenate((utctime, utctime_temp))
    if spc_aux is None:
        spc_aux, cspc_aux = spc_aux_temp, cspc_aux_temp
        continue

    # Concatenate the current arrays with the existing ones
    spc_aux = numpy.concatenate((spc_aux, spc_aux_temp),axis=1)
    cspc_aux = numpy.concatenate((cspc_aux, cspc_aux_temp),axis=1)
    

    print(utctime.shape,spc_aux.shape)

    

#--- Manage Data

#spc = spc_aux.transpose(1,0,2,3)
#cspc = cspc_aux.transpose(1,0,2,3)

spc = spc_aux
cspc = cspc_aux


# Spectra arranged in the order of: Channel, DataTime, FFTPoint, Heigh 



#--- Integragion ---
'''
# -- In Time
n_t = 1#n_t = 18 #n_t = 15
j = 0
data_spc_time = []; data_cspc_time = []
buffer = []; buffer_cspc = []
buffer = numpy.array(buffer) 
buffer_cspc = numpy.array(buffer_cspc)

while j < numpy.shape(spc)[1]:
    buffer = spc[:,j:j+n_t,:,:]
    buffer_cspc = cspc[:, j:j + n_t,:,:]
    j += n_t
    data_spc_time.append(numpy.nansum(buffer,axis=1))
    data_cspc_time.append(numpy.nansum(buffer_cspc, axis=1))

data_spc_time = numpy.array(data_spc_time)
data_cspc_time = numpy.array(data_cspc_time)
# Time correction
buffer = []
for i in range(int(-(-len(utctime)//n_t))):
    buffer.append(utctime[int(i*n_t)])
utctime = numpy.array(buffer)

# -- In Heigh
n_h = 1
j = 0
data_spc = []; data_cspc = []
buffer = [];   buffer_cspc = []
buffer = numpy.array(buffer) 
buffer_cspc = numpy.array(buffer_cspc)

#while j < numpy.shape(data_spc_time)[3]:
#    buffer = data_spc_time[:,:,:,j:j+n_h]
#    buffer_cspc = data_cspc_time[:,:,:,j:j + n_h]
#    j += n_h
#    data_spc.append(numpy.nanmean(buffer,axis=3))
#    data_cspc.append(numpy.nanmean(buffer_cspc, axis=3))

window = n_h
shape = numpy.shape(data_spc_time)
shape = numpy.array(shape)
deltaHeight = heightList[1] - heightList[0]
newdelta = deltaHeight * window
r = shape[3]  % window
newheights = (shape[3] -r)/window


buffer = data_spc_time[:, :,:, 0:int(shape[3] -r)]
buffer = buffer.reshape(shape[0], shape[1,],shape[2],int(shape[3] /window), window)
buffer = numpy.sum(buffer, 4)
data_spc = buffer
del buffer

shape = numpy.shape(data_cspc_time)
shape = numpy.array(shape)
buffer = data_cspc_time[:, :,:, 0:int(shape[3] -r)]
buffer = buffer.reshape(shape[0], shape[1,],shape[2],int(shape[3] /window), window)
buffer = numpy.sum(buffer, 4)
data_cspc = buffer

heightList = heightList[0] + numpy.arange( newheights )*newdelta



# Heigh correction
#buffer = []
#for i in range(int(-(-len(heightList)//n_h))):
#    buffer.append(heightList[int(i*n_h)])
#heightList = numpy.array(buffer)
'''

#-- Manage data
data_spc = numpy.array(spc)
data_cspc = numpy.array(cspc)

# Reordering due to integration method
##data_spc = data_spc.transpose(2,1,3,0)
##data_cspc = data_cspc.transpose(2,1,3,0)
#data_spc = data_spc.transpose(1,0,2,3)
#data_cspc = data_cspc.transpose(1,0,2,3)
print(data_spc.shape)
print(data_cspc.shape)
spc = data_spc
cspc = data_cspc

'''# Eliminate high power frequency 16 48 by median around
spc[:, :, 16, :] = numpy.median(spc[:, :, [15, 17], :], axis=2)
cspc[:, :, 16, :] = numpy.median(cspc[:, :, [15, 17], :], axis=2)
spc[:, :, 48, :] = numpy.median(spc[:, :, [47, 49], :], axis=2)
cspc[:, :, 48, :] = numpy.median(cspc[:, :, [47, 49], :], axis=2)'''

# Eliminate high power frequency 16 48 by mean in all
spc[:, :, 16, :]  = numpy.mean(numpy.delete(spc, [16, 48], axis=2), axis=2)
cspc[:, :, 16, :] = numpy.mean(numpy.delete(cspc, [16, 48], axis=2), axis=2)
spc[:, :, 48, :]  = numpy.mean(numpy.delete(spc, [16, 48], axis=2), axis=2)
cspc[:, :, 48, :] = numpy.mean(numpy.delete(cspc, [16, 48], axis=2), axis=2)

# Spectra arranged in the order of: Channel, DataTime, FFTPoint, Heigh 
#--- Spectra Plot  # [0,20] -> channel 0 time index 20
normFactor = 900 * 64 # nInt * nProfiles
global nFFTPoints, ippFactor, Vmax
nFFTPoints = 64
Va = lambda IPP, nCohInt: 6 / (4*nCohInt*(2*IPP*1e+3)/3e+8)
Vmax = 2*Va(420, 1)
ippFactor = 1
xrange = getVelRange(Vmax, nFFTPoints, ippFactor, 0) # numpy.arange(0, spc.shape[2], 1)

'''for i in range(120,140):
    idx = (0, i)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(5, 4), gridspec_kw={'width_ratios': [4, 1]}, sharey=True)

    RTI = ax1.pcolormesh( xrange, heightList, spc[idx].T,
        vmin=0.9*numpy.median(spc[idx]),
        vmax=1.1*numpy.median(spc[idx]),cmap='jet')
    plt.colorbar(RTI, ax=ax1)

    ax1.set_title(time.ctime(utctime[idx[1]]))
    ax1.set_xlabel("Velocity (m/s)")
    ax1.set_ylabel("Height")
    # Power Profile

    profile = getPower(spc[idx[0]], normFactor)[idx[1]]  #numpy.mean(spc[idx], axis=0) 
    noise = 10*numpy.log10(getNoise(numpy.array(spc)[:,idx[1],:,:], ymin_index=50) /normFactor)[idx[0]]

    ax2.plot(profile, heightList, 'r-')
    ax2.axvline(x = noise, color="black", linestyle="--")
    ax2.set_xlim([0.95*numpy.min(profile),1.02*numpy.median(profile)])
    ax2.grid()

    plt.tight_layout()
    plt.savefig(f'frame_{i}.png')
    plt.show()'''


_power = numpy.array( [getPower(spc[0], normFactor) , getPower(spc[1], normFactor)]  )[:]
_noise = numpy.array([
    10 * numpy.log10(getNoise(spc[:, i, :, :], ymin_index=55) / normFactor)
    for i in range(len(utctime))
]).T

### 
cspc_ch0 = cspc[0] #'First Pair'
print("cspc_ch0.shape", cspc_ch0.shape)
#print(heightList[220])

#-- Limit heigh
h_id_min = 41 #41
h_id_min = 0 #200
h_id_max = heightList.shape[0]

#--- Remove low coherence mode ---
LOW_COH_LIM = 4e-3 #1.8e-3 #4e-3
HIGH_SNR_LIM = 2e-3
RATE = 1.8978873*1e-6
DH = heightList[1]-heightList[0]

if 1: # dont necessary
    ccf = numpy.mean(cspc_ch0[:,:,h_id_min:h_id_max],axis=-2)
    ccf.real = signal.medfilt2d(ccf.real) # Reducing Noise
    ccf.imag = signal.medfilt2d(ccf.imag)
    powa = numpy.mean(spc[0,:,:,h_id_min:h_id_max],axis=-2)
    powb = numpy.mean(spc[1,:,:,h_id_min:h_id_max],axis=-2)
    avgcoherenceComplex = ccf / numpy.sqrt(powa * powb)

    phase_all = numpy.arctan2(avgcoherenceComplex.imag,avgcoherenceComplex.real)
    coh_all = numpy.abs(avgcoherenceComplex)
    phase_all.shape

remove_low_coh = 1

if remove_low_coh:
    ccfAux = numpy.mean(cspc_ch0,axis=-2)
    ccfAux.real = signal.medfilt2d(ccfAux.real)
    ccfAux.imag = signal.medfilt2d(ccfAux.imag)
    #ccf.real = ccf.real
    #ccf.imag = ccf.imag
    powaAux = numpy.mean(spc[0],axis=-2)
    powbAux = numpy.mean(spc[1],axis=-2)
    avgcoherenceComplexAux = ccfAux / numpy.sqrt(powaAux * powbAux)

    phase_allAux = numpy.arctan2(avgcoherenceComplexAux.imag,avgcoherenceComplexAux.real)
    coh_allAux = numpy.abs(avgcoherenceComplexAux)
    phase_allAux.shape

if remove_low_coh:
    Boolean_low_coh = numpy.array(numpy.where(coh_allAux[:,h_id_min:h_id_max]<.0025,1,0))
    print(Boolean_low_coh)
    #plt.figure()
    #RTI = plt.pcolormesh(range(12),heightList,coh_allAux.T,vmin=.0025,vmax=.08,cmap='jet')
    #RTI = plt.pcolormesh(range(len(utctime)),heightList,Boolean_low_coh.T,cmap='jet')
    #plt.title('Red: Remove data (low coherence)')
    #plt.colorbar(RTI)

#--- Calculate Data from spectra. Power coherence phase

ccf = numpy.mean(cspc_ch0,axis=-2)
if 0:
    ccf = numpy.where(coh_allAux<LOW_COH_LIM,numpy.nan,ccf) # Filtering of low coherence echoes
    
ccf = signal.medfilt2d(ccf.real,kernel_size=5) + 1j * signal.medfilt2d(ccf.imag,kernel_size=5)

powa = numpy.mean(spc[0],axis=-2)
powb = numpy.mean(spc[1],axis=-2)
avgcoherenceComplex = ccf / numpy.sqrt(powa * powb)

#phase_all = numpy.arctan2(avgcoherenceComplex.imag,avgcoherenceComplex.real)
phase_all = numpy.angle(avgcoherenceComplex)
coh_all = numpy.abs(avgcoherenceComplex)


for t_id in range(coh_all.shape[0]):
#for t_id in range(67,68):
    for h_id in range(1,coh_all.shape[1]-1):
        if numpy.isnan(coh_all[t_id,h_id]) and ~numpy.isnan(coh_all[t_id,h_id-1]) and ~numpy.isnan(coh_all[t_id,h_id+1]):
            coh_all[t_id,h_id] = (coh_all[t_id,h_id-1]+coh_all[t_id,h_id+1])/2 #?
            phase_all[t_id,h_id] = (phase_all[t_id,h_id-1]+phase_all[t_id,h_id+1])/2
            #print(time.localtime(utctime[t_id]),heightList[h_id])

print("phase_all.shape", phase_all.shape)

#--- Limit data
phase_all = phase_all[:,h_id_min:h_id_max]
coh_all = coh_all[:,h_id_min:h_id_max]
heightList = heightList[h_id_min:h_id_max]
powa =  powa[:,h_id_min:h_id_max]
powb =  powb[:,h_id_min:h_id_max]

power = powa + powb
#--
if 0:
    phase_all_mean = (numpy.roll(phase_all,1)+numpy.roll(phase_all,-1))/2
    #phase_all = phase_all_mean
    #phase_all = numpy.where(coh_all<.002,phase_all_mean,phase_all)
    #coh_all = numpy.where(coh_all<.002,numpy.nan,coh_all)


# Spectra arranged in the order of: Channel, DataTime, FFTPoint, Heigh 


utctime_all = utctime[:]

#--- Set bki parameter for day ---

year = datetime.datetime.fromtimestamp(utctime[0]).year
month = datetime.datetime.fromtimestamp(utctime[0]).month
day = datetime.datetime.fromtimestamp(utctime[0]).day
hour = 0; minute = 0; second = 0

bki = set_bki(year, month, day, hour, minute, second, heightList)
#print("Bki: ", bki)
xlim = len(utctime)


#--- SpectraDatatoFaraday

#self.dataLag_spc=(dataOut.dataLag_spc.sum(axis=1))*(dataOut.rnint2[0]/dataOut.nProfiles)
#self.dataLag_cspc=(dataOut.dataLag_cspc.sum(axis=1))*(dataOut.rnint2[0]/dataOut.nProfiles)
tmpx_a2 = spc[0].sum(axis=1).real
tmpx_5 = None
tmpx_b2 = spc[1].sum(axis=1).real
tmpx_7 = None
pa_2=numpy.abs(tmpx_a2) # +tmpx_5
pb_2=numpy.abs(tmpx_b2) # +tmpx_7
pas_2 = []
pbs_2 = []
# obtained power power2 = pa_2 + pb_2  is the same that usual power with mean

for i in range(len(utctime)):
    noise = 10*numpy.log10(getNoise(numpy.array(spc)[:,i,:,:], ymin_index=50) /normFactor)
    pas_2.append(noise[0]*numpy.ones(numpy.shape(pa_2[1])[0]))
    pbs_2.append(noise[1]*numpy.ones(numpy.shape(pa_2[1])[0]))

power2 = pa_2 + pb_2 #- pas_2 - pbs_2 # - noises
# dataOut.tnoise = dataOut.noise_lag/float(dataOut.nProfiles*dataOut.nIncohInt)
###########################
#--- Valley Processing ---#
###########################
discont = numpy.pi*1
from scipy.ndimage import gaussian_filter1d

dphi = numpy.ones((phase_all.shape[0],phase_all.shape[1]))*numpy.nan
den = numpy.ones((phase_all.shape[0],phase_all.shape[1]))*numpy.nan
phase_spline = numpy.ones((phase_all.shape[0],phase_all.shape[1]))*numpy.nan

#for idx in [55,60,65,68,70,80,85,90,95,100,105]:
'''for idx in [200,220,221,222]:
    plt.figure(figsize=(5,6))
    test = phase_all[idx,:]
    phase_t_un = numpy.unwrap(test, discont=discont)  #unwrap_with_nan(test)
    tck_s = interpolate.splrep(heightList, phase_t_un, s=2*360, k=4) ##
    phase_spline_un = interpolate.splev(heightList, tck_s) ##
    plt.plot(test,heightList,'b')
    plt.plot(phase_t_un,heightList,'g')
    phase_t_un_smooth = gaussian_filter1d(phase_t_un,sigma = 10)
    plt.plot(phase_t_un_smooth ,heightList,'y') # yellow -> used , trasnlated to loop since indexes
    plt.plot(phase_spline_un ,heightList,'m') # magenta
    plt.axvline(numpy.pi, color='k', linestyle='--', label='+π')
    plt.axvline(-numpy.pi, color='k', linestyle='--', label='-π')
    plt.title('{0} {1}'.format(time.ctime(utctime_all[idx]), idx))'''
#
plt.show()
den_power = numpy.copy(power)
den_power2 = numpy.copy(power2)
id_h_lower, id_h_upper = None, None
for idx, phase_t_aux in enumerate(phase_all):
    phase_t = numpy.copy(phase_t_aux)

    ### find index sequences that overcomes the Coherence tresshold
    arr = coh_all[idx,:]<LOW_COH_LIM 
    false_sequences = numpy.where(numpy.diff(numpy.concatenate(([False], arr == False, [False]))))[0].reshape(-1, 2)
    if arr.all():
        den[idx,:] = None
        dphi[idx] = None
        phase_spline[idx,id_h_lower:id_h_upper] = None
        continue
    
    else:
        try:
            false_indices = numpy.where(arr == False)[0]
            id_h_lower, id_h_upper = false_indices[0],false_indices[-1]
        except:
            longest_false_seq = max(false_sequences, key=lambda x: x[1] - x[0])
            id_h_lower, id_h_upper = longest_false_seq
    #
    print("idx:", idx, " range: ", id_h_lower, id_h_upper)
    '''if time.gmtime(utctime[idx]).tm_hour < 12 or time.gmtime(utctime[idx]).tm_hour > 22:
        longest_false_seq = max(false_sequences, key=lambda x: x[1] - x[0])
        id_h_lower, id_h_upper = longest_false_seq
    id_h_upper,id_h_lower = heightList.shape[0],0'''
    
    #if heightList[id_h_lower] < 100: id_h_lower = numpy.abs(heightList - 100).argmin()
    
    #Always smoothing after the unwrapping 
    ## High-Order interpolation
    #tck_s = interpolate.splrep(heightList[id_h_lower:id_h_upper], numpy.unwrap(phase_t[id_h_lower:id_h_upper]), s=2*360, k=4) ##
    #phase_spline[idx,id_h_lower:id_h_upper] = interpolate.splev(heightList[id_h_lower:id_h_upper], tck_s)
    
    # Gaussian Filter
    phase_spline[idx,id_h_lower:id_h_upper] = gaussian_filter1d(numpy.unwrap(phase_t[id_h_lower:id_h_upper], discont = discont), sigma=5) ## 15
    dev = numpy.gradient(phase_spline[idx])
    mask = numpy.where(numpy.array(dev) > 0)[0]
    print(len(mask))
    if len(mask) != 0 and (time.gmtime(utctime[idx]).tm_hour < 11 or time.gmtime(utctime[idx]).tm_hour > 22):
        print("entered")
        id_h_lower = mask[0]
        if heightList[id_h_lower] < 200: id_h_lower = numpy.abs(heightList - 200).argmin()
    phase_spline[idx,:id_h_lower] = None
    #phase_spline[idx,id_h_upper:] = None

    phase_spline[idx,id_h_lower:id_h_upper] = gaussian_filter1d(numpy.unwrap(phase_t[id_h_lower:id_h_upper], discont = discont), sigma=5) ## 15

    
    #tck_s = interpolate.splrep(heightList[id_h_lower:id_h_upper], numpy.unwrap(phase_t[id_h_lower:id_h_upper]), s=2*360, k=4) ##
    #phase_spline[idx,id_h_lower:id_h_upper] = interpolate.splev(heightList[id_h_lower:id_h_upper], tck_s)

    #spline = csaps.CubicSmoothingSpline(heightList[id_h_lower:id_h_upper], phase_t[id_h_lower:id_h_upper], smooth=0.8)

    


    #'''
    #dphi[idx] = interpolate.splev(heightList, tck_s, der=1)

    #if idx in [200,220,221,222]:
    if  idx > 200 and idx < 250 or idx == 133 or idx == 120:
        plt.figure(figsize=(5,6))
        test = phase_t
        phase_t_un = numpy.unwrap(test, discont=discont)  #unwrap_with_nan(test)
        plt.plot(test,heightList,'b')
        plt.plot(phase_t_un,heightList,'g')
        plt.plot(phase_spline[idx] ,heightList,'y') # yellow -> used , trasnlated to loop since indexes

        plt.axvline(numpy.pi, color='k', linestyle='--', label='+π')
        plt.axvline(-numpy.pi, color='k', linestyle='--', label='-π')
        plt.axhline(heightList[mask[0]], color='gray', linestyle='--')
        plt.axhline(heightList[mask[-1]], color='gray', linestyle='--')
        plt.title('{0} {1}'.format(time.ctime(utctime_all[idx]), idx))
        plt.savefig(f'{idx}_interpol.png')
        plt.close()




    for i in range(2,phase_all.shape[1]-2): # idx time i heigh
        fact=(-0.5/(RATE*DH))*bki[i]

        dphi[idx,i]=((phase_spline[idx][i+1]-phase_spline[idx][i-1])+(2.0*(phase_spline[idx][i+2]-phase_spline[idx][i-2])))/10.0 #Better results

        den[idx,i]=dphi[idx,i]*abs(fact) 
        #'''

### Cleaning Masks
""" Cleaning by Coherence filtering LOW_COH_LIM and by 
snr tresshold HIGH_SNR_LIM (optional, only for coherent echoes in ISR)"""
snr_thr = True

coh_all_aux = signal.medfilt2d(coh_all,kernel_size=9) #coh_all.copy()
coh_all_aux = signal.medfilt2d(coh_all_aux,kernel_size=7) 
coh_all_aux = numpy.where(coh_all_aux < LOW_COH_LIM ,numpy.nan,coh_all_aux) # .0025
coh_all_aux_filled = numpy.copy(coh_all_aux[:xlim].T)

snr_all = (_power[0, :xlim, :] - _noise[0, :xlim][:, numpy.newaxis])/_noise[0, :xlim][:, numpy.newaxis]
snr_all_aux = signal.medfilt2d(snr_all,kernel_size=9)
snr_all_aux = numpy.where(snr_all_aux > HIGH_SNR_LIM ,numpy.nan,snr_all_aux)
snr_all_aux_filled = numpy.copy(snr_all_aux[:xlim].T)

for t_id in range(coh_all_aux_filled.shape[1]):
    for h_id in range(1,coh_all_aux_filled.shape[0]-1):

        if numpy.isnan(coh_all_aux_filled[h_id,t_id]) and ~numpy.isnan(coh_all_aux_filled[h_id-1,t_id]) and ~numpy.isnan(coh_all_aux_filled[h_id+1,t_id]):
            coh_all_aux_filled[h_id,t_id] = (coh_all_aux_filled[h_id-1,t_id]+coh_all_aux_filled[h_id+1,t_id])/2

        if numpy.isnan(snr_all_aux_filled[h_id,t_id]) and ~numpy.isnan(snr_all_aux_filled[h_id-1,t_id]) and ~numpy.isnan(snr_all_aux_filled[h_id+1,t_id]):
            snr_all_aux_filled[h_id,t_id] = (snr_all_aux_filled[h_id-1,t_id]+snr_all_aux_filled[h_id+1,t_id])/2

mask = numpy.isnan(coh_all_aux_filled.T)
#mask[50:54,200:350] = True # Oct 1
#mask[56:58,80:200] = True # Oct 1
#mask[78:86,:] = True # Oct 3
#mask[78:,:150] = True # Oct 3

mask_snr = numpy.isnan(snr_all_aux_filled.T)
#snr_all_aux = numpy.where(snr_all_aux > HIGH_SNR_LIM ,numpy.nan,snr_all_aux)
#mask_snr = numpy.isnan(snr_all_aux)

den = numpy.where(mask ,numpy.nan,den)
den = numpy.where(mask_snr ,numpy.nan,den)
den[den < 0] = numpy.nan
dphi = numpy.where(mask,numpy.nan,dphi)
phase_spline = numpy.where(mask ,numpy.nan,phase_spline)

# Normalize Power
'''for idx,utime in enumerate(utctime_all):
    #if (utime>=11.5 and utime<23): # 6 30am to 6pm
    if True:
        i2=(390.-heightList[0])/DH
        i1=(250.-heightList[0])/DH

    try:
        heightList[i2]
    except:
        i2 -= 1


    i1=int(i1);i2=int(i2)
    print("Bounds 1: ", heightList[i1],heightList[i2])

    try:
        cf= normal(den[idx,i1:i2], den_power[idx,i1:i2], i2-i1, 1)
    except Exception as e:
        print(f"Exception occurred: {e}")
        print("except: chi factor not achieved in normalization")
        cf = numpy.nan
    
    try:
        cf2= normal(den[idx,i1:i2], den_power2[idx,i1:i2], i2-i1, 1)
    except Exception as e:
        print(f"Exception occurred: {e}")
        print("except: chi factor not achieved in normalization")
        cf2 = numpy.nan
    
    #print("power[utime,:]",power[id,:])
    den_power[idx,:] *= cf
    den_power2[idx,:] *= cf2
    print("cf",cf, idx, i2-i1, i1 , i2)'''



# only to plot a sample - Power profiles
'''idx_list = [60,70,80,100,150,200]
for idx in idx_list:
    fig = plt.figure(figsize=(5,8))
    ax = fig.add_subplot(111)
    #ax.plot((phase_t[id_h_lower:id_h_upper]),heightList[id_h_lower:id_h_upper])
    ax.plot(den[idx,id_h_lower:id_h_upper],heightList[id_h_lower:id_h_upper],'--')
    print( "###")
    print(den_power, den_power.shape)
    print(den_power2, den_power2.shape)
    ax.plot(den_power[idx,id_h_lower:id_h_upper],heightList[id_h_lower:id_h_upper])
    ax.plot(den_power2[idx,id_h_lower:id_h_upper],heightList[id_h_lower:id_h_upper],'--')
    ax.legend(['Faraday','Power', 'Power2'])
    plt.title('{0} {1}'.format(time.ctime(utctime_all[idx]), idx))
plt.show()'''


################
### PLOTTING ###
################

#-- Phase plot 
'''xlim = len(utctime)
fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')

RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,phase_spline[:xlim].T,cmap='RdBu_r',vmin=-numpy.pi,vmax=4*numpy.pi)
#RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,signal.medfilt2d(phase_spline[:xlim],kernel_size=9).T,cmap='RdBu_r',vmin=-3,vmax=3)

date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)
#ax.set_ylim(200,350)
plt.title('Smoothed Phase RTI')
#plt.show()'''



#--- Coherence Plot
fig = plt.figure(figsize=(15,5))
ax = fig.add_subplot(221)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')
RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,coh_all[:xlim].T,cmap='jet',vmin=0,vmax=.01) # 700 when bad normalizing
date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)

ax2 = fig.add_subplot(222)
RTI_aux = ax2.pcolormesh(df_x['Dates'][:xlim],heightList,coh_all_aux[:xlim].T,cmap='jet',vmin=0,vmax=.01)
fig.colorbar(RTI_aux)
ax2.xaxis.set_major_formatter(date_format)

ax3 = fig.add_subplot(224)
RTI_aux_3 = ax3.pcolormesh(df_x['Dates'][:xlim],heightList,coh_all_aux_filled,cmap='jet',vmin=0,vmax=.01)
fig.colorbar(RTI_aux_3)
ax3.xaxis.set_major_formatter(date_format)
plt.title("Coherence RTI")
plt.tight_layout()
plt.show()




#--- Power Plot
'''fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')
#RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,phase_spline[:xlim].T,cmap='RdBu_r',vmin=-numpy.pi,vmax=4*numpy.pi)

#val = 10*numpy.log10(powa[:xlim,h_id_min:h_id_max])
#RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,val.T,cmap='jet',vmin=0.99*numpy.median(val),vmax=1.01*numpy.median(val))
val = 10*numpy.log10(power)
RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,val[:xlim].T,cmap='jet',vmin=0.99*numpy.median(val),vmax=1.01*numpy.median(val))

date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)
plt.title("Power RTI")
plt.show()'''

#--- RTI Plot

fig, ax = plt.subplots(2, 1, figsize=(9, 3.5), sharex=True)

df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')

for i in [0, 1]:
    RTI = ax[i].pcolormesh(
        df_x['Dates'][:xlim],
        heightList,
        _power[i, :xlim, :].T,  # ensure this is (len(heightList), len(time))
        cmap='jet',vmin=0.95*numpy.median( _noise[i] ),vmax=48
    )

    date_format = mdates.DateFormatter('%H:%M')
    ax[i].xaxis.set_major_formatter(date_format)
    fig.colorbar(RTI, ax=ax[i])

ax[0].set_title("RTI")
plt.show()

#--- SNR Plot

fig, ax = plt.subplots(2, 1, figsize=(9, 3.5), sharex=True)

df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')

for i in [0, 1]:
    val = (_power[i, :xlim, :] - _noise[i, :xlim][:, numpy.newaxis])/_noise[i, :xlim][:, numpy.newaxis]
    RTI = ax[i].pcolormesh(
        df_x['Dates'][:xlim],
        heightList,
        val.T,  # ensure this is (len(heightList), len(time))
        cmap='jet',vmin=0 , vmax=0.002 #0.004
    )

    date_format = mdates.DateFormatter('%H:%M')
    ax[i].xaxis.set_major_formatter(date_format)
    fig.colorbar(RTI, ax=ax[i])

ax[0].set_title("RTI")
plt.show()


#--- Gradient Plot
'''fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')

RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,numpy.gradient(numpy.gradient(phase_spline[:xlim].T,heightList,axis=0),axis=0),cmap='jet',vmin=-.001,vmax=.001)
date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)
plt.title("Gradient RTI")'''
#ax.set_ylim(200,350)
#plt.show()

#--- dphi plot
fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')

RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,dphi[:xlim].T,cmap='plasma',vmin=-0.04,vmax=.05)
#RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,signal.medfilt2d(dphi[:xlim].T),cmap='Blues',vmin=0,vmax=.04)

date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)
plt.title("Dphi RTI")
#ax.set_ylim(200,350)
#plt.show()


limit_date = df_x['Dates'][:xlim][0::6]
heights_VIPIR = [536.6,505,456,313,328,338,339,313,336,numpy.nan,282,337,280,290,numpy.nan,312,350,185,numpy.nan,330,numpy.nan,434,447,numpy.nan]
heights_VIPIR = heights_VIPIR[:19]
heights_VIPIR = numpy.array([285.3,296.7,309.5,294.1,330.9,292.8,291.1,326.2,311.9,285.3,294.3,298.6,290.2,287.2,282.6,338.8,271.3,294.7,305.4,289.8,322.8,297.0,273.3,310.1,300.5,321.0,297.2,304.8,321.0,293.4,285.0,303.2,289.6,320.6,291.7,312.2,299.7,332.6,297.4,308.4,312.7,319.7,338.6,322.5,334.8,347.2,340.7,362.2,356.0,353.4,358.1,377.0,376.7,372.6,365.1,378.2,386.9,377.5,375.7,387.4,380.4,383.0,396.1,404.1,389.7,401.7,397.2,390.0,388.9,392.4,374.1,405.4,384.5,388.5,390.4,405.5,423.6,419.0,416.6,414.9,387.7,410.0,400.0,395.5,369.3,347.6,338.2,351.5,389.2,336.8,332.1,366.2,354.9,351.7])

#--- Density Plot
#plt.style.use('dark_background')
fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')


RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,den[:xlim].T,cmap='jet',norm=colors.LogNorm(vmin=1e4,vmax=5e6))

date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)
plt.title("Density RTI: "+str(day)+"/"+str(month)+"/"+str(year))




# Compute the result
result = numpy.array([
    numpy.nan if numpy.all(numpy.isnan(row)) else numpy.nanargmax(row)
    for row in den[:xlim, 2:-2]
], dtype=float)


# Convert result to heightList, preserving NaN
heightList_result = numpy.array([
    numpy.nan if numpy.isnan(index) else heightList[int(index)]
    for index in result
], dtype=float)




#ax.set_ylim(200,350)
#ax.plot(df_x['Dates'][:xlim],heights_VIPIR,'^',color='r',label='VIPIR')
#ax.plot(_,heights_VIPIR,'^',color='r',label='VIPIR')
#ax.plot(limit_date,heights_VIPIR[:19],'^',color='g',label='VIPIR')
#plt.legend(loc='lower right')
#plt.show()


#-- Total Phase
xlim = -1
fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')

RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,phase_all[:xlim].T,cmap='RdBu_r',vmin=-1*numpy.pi,vmax=1*numpy.pi)
#RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,signal.medfilt2d(phase_all[:xlim],kernel_size=9).T,cmap='RdBu_r',vmin=-3,vmax=3)

date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
ax.set_title("Total Phase", fontsize=14)
fig.colorbar(RTI)
plt.show()#

#-- Density & magnetometer
import numpy as np

LISN_dir = '/media/cportilla/HDD/Valley/LISN_magnetometer/' + 'jica_250813.sec'

# Inicializar listas vacías
from datetime import datetime, timedelta, timezone
times = []
channel_H = []
channel_D = []
channel_Z = []

with open(LISN_dir, "r") as f:
    lines = f.readlines()

# Saltar encabezados (primeras 2 líneas)
for line in lines[2:]:
    if not line.strip():
        continue  # saltar líneas vacías si hay
    parts = line.split()
    if len(parts) < 6:
        continue  # línea malformada

    hh, mm, ss = map(int, parts[0:3])
    h_val = parts[3]
    d_val = parts[4]
    z_val = parts[5]

    times.append(f"{hh:02}:{mm:02}:{ss:02}")
    channel_H.append(h_val)
    channel_D.append(d_val)
    channel_Z.append(z_val)

# Convertir a arrays si lo necesitas
channel_H = np.array(channel_H)
channel_D = np.array(channel_D)
channel_Z = np.array(channel_Z)
# Scaling
channel_H = channel_H.astype(float)
channel_D = channel_D.astype(float)
channel_Z = channel_Z.astype(float)
H = (channel_H-np.min(channel_H)) *0.000055   #/ np.positive(np.mean(channel_H)) *1.5e2
D = (channel_D-np.min(channel_D[0])) *0.0005
Z = (channel_Z-np.min(channel_Z[0])) *0.000055

# Timezone definitions
UTC = timezone.utc
GMT_minus_5 = timezone(timedelta(hours=-5))

# Create datetime objects in UTC and convert to GMT-5
datetime_array = [
    datetime.strptime(t, "%H:%M:%S").replace(
        year=2025, month=8, day=13, tzinfo=UTC
    )
    for t in times
]
#datetime_array = [ts - timedelta(hours=5) for ts in datetime_array]
LTime2 = [datetime.fromtimestamp(ts, timezone.utc) - timedelta(hours=5) for ts in utctime]
LTime2 = [t.astimezone(GMT_minus_5)for t in LTime2]
# Example: print the output
'''for dt in datetime_array:
    print(dt)'''
# Slice the range first
time_slice = datetime_array[50000:80000]
H_slice = H[50000:80000]

# Then keep every 3rd item (i.e., every 3 seconds)
time_reduced = time_slice[::3]
H_reduced = H_slice[::3]


# RTI plot
fig = plt.figure(figsize=(9,3.5))
ax = fig.add_subplot(111)
df_x = pd.DataFrame(data=utctime_all[:], columns=["Dates"])
df_x['Dates'] = pd.to_datetime(df_x['Dates'], unit='s', errors='coerce')


RTI = ax.pcolormesh(df_x['Dates'][:xlim],heightList,den[:xlim].T,cmap='jet',norm=colors.LogNorm(vmin=1e4,vmax=5e6))

date_format = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(date_format)
fig.colorbar(RTI)
plt.title("Density RTI: "+str(day)+"/"+str(month)+"/"+str(year))

H_norm = (H_reduced - np.min(H_reduced)) / (np.max(H_reduced) - np.min(H_reduced))

# Rescale to 110–114
H_scaled = H_norm * (380 - 108) + 108

# Plot H line on top (adjust y-range if needed to be visible)
plt.plot(time_reduced, H_scaled, color='black', linewidth=2, label='H (nT)')

#plt.ylim([105, 115])  # This limits visibility of H unless it falls in this range
plt.xlabel('Time')
plt.tight_layout()
plt.legend()
#plt.savefig("Overlay_SameAxis.png")
plt.show()







exit(1)
#-- Data contrast with VIPIR


file_path = "/media/cportilla/HDD/PPP_code/scaled_2024_10_1.npz"
data = numpy.load(file_path, allow_pickle=True)

# Access individual arrays
DEN = data['DEN']
H = data['H']
TIME = data['TIME']


isr_id = 50
vipir_id = 191
'''
for isr_id in range(len(utctime)):

    vipir_id = numpy.argmin(numpy.abs((TIME - numpy.array(utctime[isr_id]))))
    print("isr range time: ", time.ctime(min(utctime)), " ", time.ctime(max(utctime)))
    print("vipir range time: ", time.ctime(min(TIME)), " ", time.ctime(max(TIME)))
    print("ISR TIME:", time.ctime(utctime[isr_id]),"\n VIPIR TIME:", time.ctime(TIME[vipir_id]))
    plt.plot(den[isr_id,:].T,heightList)
    plt.plot(DEN[vipir_id],H[vipir_id])
    plt.xlim([5e4,5e6])
    plt.ylim([150,400])
    plt.xscale('log')
    plt.title("ISR TIME:"+ time.ctime(utctime[isr_id])+"\n VIPIR TIME:"+ time.ctime(TIME[vipir_id]))
    print(time.ctime(min(TIME)),time.ctime(max(TIME)))
    plt.legend(['ISR','VIPIR'])
    plt.savefig(str(isr_id)+'.png',dpi = 100)
    plt.close()

'''
########################
##### SAVE DATA ########
########################

#write_routine(den, utctime, heightList, figpath='/media/cportilla/HDD/Valley/HDF5/')