import json
import os
import datetime
import numpy
import madrigal.cedar
from schainpy.utils import log


def load_json(obj):
    '''
    Parse json as string instead of unicode
    '''

    if isinstance(obj, str):
        iterable = json.loads(obj)
    else:
        iterable = obj

    if isinstance(iterable, dict):
        #return {str(k): load_json(v) if isinstance(v, dict) else str(v) if isinstance(v, basestring) else v
        #    for k, v in list(iterable.items())}
        return {str(k): load_json(v) if isinstance(v, dict) else str(v) if isinstance(v, str) else v
                for k, v in iterable.items()}
    elif isinstance(iterable, (list, tuple)):
        #return [str(v) if isinstance(v, basestring) else v for v in iterable]
        return [str(v) if isinstance(v, str) else v for v in iterable]

    return iterable


def setFile():
    '''
    Create new cedar file object
    '''

    mnemonic = MNEMONICS[kinst]   #TODO get mnemonic from madrigal
    date = datetime.datetime.utcfromtimestamp(utctime)
    #if dataOut.input_dat_type:
        #date=datetime.datetime.fromtimestamp(dataOut.TimeBlockSeconds_for_dp_power)
    #print("date",date)

    filename = '{}{}{}'.format(mnemonic,
                                date.strftime('%Y%m%d_%H%M%S'),
                                ext)

    fullname = os.path.join(path, filename)

    if os.path.isfile(fullname) :
        log.warning(
            'Destination file {} already exists, previous file deleted.'.format(
                fullname),
            'MADWriter')
        os.remove(fullname)

    try:
        log.success(
            'Creating file: {}'.format(fullname),
            'MADWriter')
        if not os.path.exists(path):
            os.makedirs(path)
        fp = madrigal.cedar.MadrigalCedarFile(fullname, True)


    except ValueError as e:
        log.error(
            'Impossible to create a cedar object with "madrigal.cedar.MadrigalCedarFile"',
            'MADWriter')
        return

    return fp, fullname

def writeBlock(fp,utctime, extra_args):
    '''
    Add data records to cedar file taking data from oneDDict and twoDDict
    attributes.
    Allowed parameters in: parcodes.tab
    '''
    #dataOut.paramInterval=2
    startTime = datetime.datetime.utcfromtimestamp(utctime)

    endTime = startTime + datetime.timedelta(seconds=paramInterval)

    heights = heightList

    '''if ext == '.dat':
        for key, value in list(twoDDict.items()):
            if isinstance(value, str):
                data = getattr(dataOut, value)
                invalid = numpy.isnan(value)
                data[invalid] = missing
            elif isinstance(value, (tuple, list)):
                attr, key = value
                data = getattr(dataOut, attr)
                invalid = numpy.isnan(data)
                data[invalid] = missing'''

    '''if ext == '.hdf5':
        for key, value in list(twoDDict.items()):
            if isinstance(value, str):
                data = globals()[value][0]
                invalid = numpy.isnan(value)
                data[invalid] = missing
            elif isinstance(value, (tuple, list)):
                attr, key = value
                data = globals()[attr][0]
                invalid = numpy.isnan(data)
                data[invalid] = missing'''

    out = {}
    for key, value in list(twoDDict.items()):
        key = key.lower()
        if isinstance(value, str):
            tmp = globals()[value]
            out[key] = tmp.flatten()[:len(heights)]
        elif isinstance(value, (tuple, list)):
            attr, x = value
            data = globals()[attr]
            out[key] = data[int(x)][:len(heights)]

    a = numpy.array([out[k] for k in keys])
    #print(a)
    nrows = numpy.array([numpy.isnan(a[:, x]).all() for x in range(len(heights))])
    index = numpy.where(nrows == False)[0]

    #print(startTime.minute)
    rec = madrigal.cedar.MadrigalDataRecord(
        kinst,
        kindat,
        startTime.year,
        startTime.month,
        startTime.day,
        startTime.hour,
        startTime.minute,
        startTime.second,
        startTime.microsecond/10000,
        endTime.year,
        endTime.month,
        endTime.day,
        endTime.hour,
        endTime.minute,
        endTime.second,
        endTime.microsecond/10000,
        list(oneDDict.keys()),
        list(twoDDict.keys()),
        len(index),
        **extra_args
    )
    #print("rec",rec)
    # Setting 1d values
    for key in oneDDict:
        rec.set1D(key, globals()[oneDDict[key]])

    # Setting 2d values
    nrec = 0
    for n in index:
        for key in out:
            rec.set2D(key, nrec, out[key][n])
        nrec += 1

    fp.append(rec)
    if ext == '.hdf5' and counter %2 == 0 and counter > 0:
        #print("here")
        fp.dump()
    if counter % 20 == 0 and counter > 0:
        #fp.write()
        log.log(
            'Writing {} records'.format(
                counter),
            'MADWriter')
    return fp

def setHeader(fp, fullname):
    '''
    Create an add catalog and header to cedar file
    '''

    log.success('Closing file {}'.format(fullname), 'MADWriter')

    if ext == '.dat':
        fp.write()
    else:
        fp.dump()
        fp.close()

    header = madrigal.cedar.CatalogHeaderCreator(fullname)
    header.createCatalog(**catalog)
    header.createHeader(**_header)
    header.write()

'''def timeFlag(self):
    currentTime = dataOut.utctime
    timeTuple = time.localtime(currentTime)
    dataDay = timeTuple.tm_yday

    if currentDay is None:
        currentDay = dataDay
        return False

    #Si el dia es diferente
    if dataDay != currentDay:
        currentDay = dataDay
        return True

    else:
        return False'''

def putData(fp, counter, utctime, extra_args):


    #if dataOut.flagDiscontinuousBlock or counter == blocks or timeFlag():
    #    if counter > 0:
    #        setHeader()
    #    counter = 0

    

    fp = writeBlock(fp,utctime, extra_args)
    counter += 1
    return fp, counter, fullname 

def close(fp,fullname):

    if counter > 0:
        setHeader(fp,fullname)



def write_routine(den, time, height, figpath='/media/cportilla/HDD/Valley/HDF5/'):
    global basestring
    global counter
    global lat, lon, paramInterval, DensityFinal, ind2DList, oneDDict, twoDDict, metadata
    global MNEMONICS, kinst, utctime, ext, path, kindat, keys, heightList, catalog, _header
    global fullname
    global missing
    missing = -32767 # see if we can change by nan without breaking MadrigalData

    utctime = time
    heightList = height
    DEF_CATALOG = {
        'principleInvestigator': 'Marco Milla',
        'expPurpose': '',
        'cycleTime': '',
        'correlativeExp': '',
        'sciRemarks': '',
        'instRemarks': ''
        }
    DEF_HEADER = {
        'kindatDesc': '',
        'analyst': 'Jicamarca User',
        'comments': '',
        'history': ''
        }
    MNEMONICS = {
        10: 'jro',
        12: 'jmp',
        11: 'jbr',
        14: 'jmp', #Added by R. Flores
        840: 'jul',
        13: 'jas',
        1000: 'pbr',
        1001: 'hbr',
        1002: 'obr',
        400: 'clr'

        }

    basestring = str
    figpath_server=figpath
    format = 'hdf5'


    _utctime = utctime
    lat=-11.95
    lon=-76.87
    paramInterval= 0 #nIncohInt*2*2
    counter = 0
    blocks = 10600# kwargs.get('blocks', None)

    for idx, utctime in enumerate(_utctime):
        one = {'gdlatr': 'lat', 'gdlonr': 'lon', 'inttms': 'paramInterval'} #reader gdlatr-->lat only 1D

        two = {
            'gdalt': 'heightList',   #<----- nmonics
            'NE': ('DensityFinal', 0),
            } #writer
        f=open('/media/cportilla/HDD/Valley/moder_test.txt','r')
        file_contents=f.read()
        ind = ['gdalt']
        meta = {
            'kinst': 10, #instrument code
            'kindat': 1800, #type of data
            'catalog': {
                'principleInvestigator': 'Danny Scipión',
                'expPurpose': 'Electron Density',
                'sciRemarks': file_contents
                },
            'header': {
                'analyst': 'C. Portilla'
            }
        }
        f.close()

        __attrs__ = ['path', 'oneDDict', 'ind2DList', 'twoDDict','metadata', 'format', 'blocks']
        missing = -32767
        currentDay = None

        ind2DList = ind
        oneDDict = one
        twoDDict = two
        metadata = meta

        DensityFinal = [den[idx]]
        #DensityFinal[numpy.isnan(DensityFinal)] = missing
        DensityFinal = numpy.array(DensityFinal, dtype=float)
        DensityFinal[numpy.isnan(DensityFinal)] = missing

        print("DensityFinal", numpy.shape(DensityFinal))

        path = figpath
        oneDDict = load_json(one)
        twoDDict = load_json(two)
        ind2DList = load_json(ind)
        meta = load_json(meta)
        kinst = meta.get('kinst')
        kindat = meta.get('kindat')
        catalog = meta.get('catalog', DEF_CATALOG)
        _header = meta.get('header', DEF_HEADER)
        if format == 'cedar':
            ext = '.dat'
            extra_args = {}
        elif format == 'hdf5':
            ext = '.hdf5'
            extra_args = {'ind2DList': ind2DList}

        keys = [k.lower() for k in twoDDict]
        if 'range' in keys:
            keys.remove('range')
        if 'gdalt' in keys:
            keys.remove('gdalt')

        if counter == 0:
            fp,fullname = setFile()

        fp, counter, fullname = putData(fp, counter, utctime, extra_args)
    close(fp,fullname)
