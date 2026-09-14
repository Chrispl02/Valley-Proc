import os, sys

from schainpy.controller import Project

desc = "150 km Jicamarca January 2022"
filename = "150km_jicamarca.xml"

controllerObj = Project()

controllerObj.setup(id = '191', name='test01', description=desc)

dpath = '/mnt/valley/'
figpath = '/mnt/data10tb/valley/2026_08/short/'
online=1
delay=30
walk=1
startDate='2026/08/24'
endDate='2026/08/30'
startTime='00:00:00'
endTime='23:59:59'

t=['0','24']

readUnitConfObj = controllerObj.addReadUnit(datatype='VoltageReader',
                                            path=dpath,
                                            startDate=startDate,
                                            endDate=endDate,
                                            startTime=startTime,
                                            endTime=endTime,
                                            online=online,
                                            delay=delay,
                                            getByBlock=1,
                                            walk=walk)

#opObj11 = readUnitConfObj.addOperation(name='printNumberOfBlock')

procUnitConfObj0 = controllerObj.addProcUnit(datatype='VoltageProc', inputId=readUnitConfObj.getId())

opObj11 = procUnitConfObj0.addOperation(name='Reshaper', optype='other')
#opObj11.addParameter(name='nTxs', value=4.0, format='float')  # not recommended this way
opObj11.addParameter(name='shape', value=[1404, 700], format='list')

opObj11 = procUnitConfObj0.addOperation(name='ProfileSelector', optype='other')
#opObj11.addParameter(name='rangeList', value=((0,79),(468,547),(936,1015)), format='list')
opObj11.addParameter(name='rangeList', value=((0,79)), format='list')
     
cod7barker=[[1.0,1,1,-1,-1,1,-1],[1,1,1,-1,-1,1,-1],[-1,-1,-1,1,1,-1,1],[-1,-1,-1,1,1,-1,1]]
opObj11 = procUnitConfObj0.addOperation(name='Decoder')
opObj11.addParameter(name='code', value=cod7barker, format='list')
opObj11.addParameter(name='nCode', value=4, format='int')
opObj11.addParameter(name='nBaud', value=7, format='int')

opObj11 = procUnitConfObj0.addOperation(name='deFlip')
opObj11.addParameter(name='channelList', value=[1,3,5,7], format='list')

procUnitConfObj1 = controllerObj.addProcUnit(datatype='SpectraProc', inputId=procUnitConfObj0.getId())
procUnitConfObj1.addParameter(name='nFFTPoints', value='80', format='int')
procUnitConfObj1.addParameter(name='nProfiles', value='80', format='int')
procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6)], format='list')

opObj11 = procUnitConfObj1.addOperation(name='IncohInt', optype='other')
opObj11.addParameter(name='timeInterval', value='60', format='float')
#opObj11.addParameter(name='timeInterval', value='20', format='float')

opObj11 = procUnitConfObj1.addOperation(name='SpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2004', format='int')
opObj11.addParameter(name='wintitle', value='SHORT SPC', format='str')
opObj11.addParameter(name='zmin', value='15', format='int')
opObj11.addParameter(name='zmax', value='45', format='int')
opObj11.addParameter(name='showprofile', value='1')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='231', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

opObj11 = procUnitConfObj1.addOperation(name='CrossSpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2006', format='int')
opObj11.addParameter(name='wintitle', value='SHORT CROSS-SPC', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='231', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

opObj11 = procUnitConfObj1.addOperation(name='CoherencePlot', optype='other')
opObj11.addParameter(name='id', value='102', format='int')
opObj11.addParameter(name='wintitle', value='SHORT CMAP', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='231', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

opObj11 = procUnitConfObj1.addOperation(name='PhasePlot', optype='other')
opObj11.addParameter(name='id', value='1002', format='int')
opObj11.addParameter(name='wintitle', value='SHORT PMAP', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='231', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

controllerObj.start()

