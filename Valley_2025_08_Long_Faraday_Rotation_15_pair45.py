import os, sys

from schainpy.controller import Project

desc = "150 km Jicamarca January 2015"
filename = "150km_jicamarca.xml"

controllerObj = Project()

controllerObj.setup(id = '191', name='test01', description=desc)

dpath = '/home/cportilla/Minotaur/2025_08/Valley/main_radar/rawdata'
figpath = '/home/cportilla/PC_DATA/Valley/08_15_pair45'
online=0
delay=30
walk=1
startDate='2025/08/15'
endDate='2025/08/15'
#startTime='08:30:00' #May28
startTime='00:00:00'
endTime='23:59:59'

t=['0','24']
valley_pairs = '4,5'

readUnitConfObj = controllerObj.addReadUnit(datatype='VoltageReader',
                                            path=dpath,
                                            startDate=startDate,
                                            endDate=endDate,
                                            startTime=startTime,
                                            endTime=endTime,
                                            online=online,
                                            delay=delay,
                                            walk=walk)
#											getblock=1)#added

procUnitConfObj0 = controllerObj.addProcUnit(datatype='VoltageProc', inputId=readUnitConfObj.getId())


opObj11 = procUnitConfObj0.addOperation(name='ProfileSelector', optype='other')
opObj11.addParameter(name='rangeList', value=((53,116),(170,233),(287,350)), format='list')

opObj11 = procUnitConfObj0.addOperation(name='filterByHeights')
opObj11.addParameter(name='window', value='5', format='int')

code = [[1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1], [1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1], [-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1], [-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1]]
opObj11 = procUnitConfObj0.addOperation(name='Decoder', optype='other')
opObj11.addParameter(name='code', value=code, format='list')
opObj11.addParameter(name='nCode', value='4', format='int')
opObj11.addParameter(name='nBaud', value='28', format='int')

opObj11 = procUnitConfObj0.addOperation(name='filterByHeights')
opObj11.addParameter(name='window', value='4', format='int')

opObj11 = procUnitConfObj0.addOperation(name='deFlip')
opObj11.addParameter(name='channelList', value=[1,3,5,7], format='list')

op1 = procUnitConfObj0.addOperation(name='selectChannels')
op1.addParameter(name='channelList', value=valley_pairs)

op4 = procUnitConfObj0.addOperation(name='selectHeights')
op4.addParameter(name='minHei', value='70')
op4.addParameter(name='maxHei', value='400')


procUnitConfObj1 = controllerObj.addProcUnit(datatype='SpectraProc', inputId=procUnitConfObj0.getId())
procUnitConfObj1.addParameter(name='nFFTPoints', value='64', format='int')
procUnitConfObj1.addParameter(name='nProfiles', value='64', format='int')
procUnitConfObj1.addParameter(name='pairsList', value=[(1,0)], format='list')
#procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6),(2,6),(3,7)], format='list')
#procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6)], format='list')



#opObj11 = procUnitConfObj1.addOperation(name='IncohInt', optype='other')
opObj11 = procUnitConfObj1.addOperation(name='IntegrationFaradaySpectraNoLags')
#opObj11.addParameter(name='timeInterval', value='120', format='float')
opObj11.addParameter(name='n', value='900', format='float')
#opObj11.addParameter(name='timeInterval', value='20', format='float')

#opObj11 = procUnitConfObj1.addOperation(name='CoherenceRads')


opObj11 = procUnitConfObj1.addOperation(name='SpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2001', format='int')
opObj11.addParameter(name='wintitle', value='LONG SPC', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='zmin', value='15', format='int')
opObj11.addParameter(name='zmax', value='45', format='int')
opObj11.addParameter(name='save', value=figpath, format='str')

opObj11 = procUnitConfObj1.addOperation(name='CrossSpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2005', format='int')
opObj11.addParameter(name='wintitle', value='LONG CROSS-SPC', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='save', value=figpath, format='str')

opObj11 = procUnitConfObj1.addOperation(name='CoherencePlot', optype='other')
opObj11.addParameter(name='id', value='101', format='int')
opObj11.addParameter(name='wintitle', value='LONG CMAP', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='throttle', value='20')
opObj11.addParameter(name='save', value=figpath, format='str')

opObj11 = procUnitConfObj1.addOperation(name='PhasePlot', optype='other')
opObj11.addParameter(name='id', value='102', format='int')
opObj11.addParameter(name='wintitle', value='LONG PMAP', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='throttle', value='20')
opObj11.addParameter(name='save', value=figpath, format='str')

#dataList=['Coherence',
dataList=['data_spc','data_cspc',
        'utctime']
metadataList=['heightList','timeZone']

op221 = procUnitConfObj1.addOperation(name='HDFWriter', optype='external')
op221.addParameter(name='path', value=figpath)
op221.addParameter(name='dataList', value=dataList)
op221.addParameter(name='uniqueChannel', value='False')
op221.addParameter(name='metadataList', value=metadataList)
#op221.addParameter(name='blocksPerFile', value=500)
op221.addParameter(name='blocksPerFile', value=50)



controllerObj.start()
