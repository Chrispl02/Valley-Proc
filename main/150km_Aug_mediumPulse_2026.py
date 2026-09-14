import os, sys

from schainpy.controller import Project

desc = "150 km Jicamarca January 2022"
filename = "150km_jicamarca.xml"

controllerObj = Project()

controllerObj.setup(id = '191', name='test01', description=desc)

dpath = '/mnt/valley/'
figpath = '/mnt/data10tb/valley/2026_08/medium/'
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
                                            walk=walk,
					    getByBlock=1)
					    
procUnitConfObj0 = controllerObj.addProcUnit(datatype='VoltageProc', inputId=readUnitConfObj.getId())

opObj11 = procUnitConfObj0.addOperation(name='Reshaper', optype='other')
opObj11.addParameter(name='shape', value=[702, 1400], format='list')

opObj11 = procUnitConfObj0.addOperation(name='ProfileSelector', optype='other')
opObj11.addParameter(name='rangeList', value=((42,105),(276,339),(510,573)), format='list')

cc64=[[1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1], [1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1], [1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1], [1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1], [-1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1], [-1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1], [-1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1], [-1, -1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1]]

opObj11 = procUnitConfObj0.addOperation(name='Decoder', optype='other')
opObj11.addParameter(name='code', value=cc64, format='list')
opObj11.addParameter(name='nCode', value='8', format='int')
opObj11.addParameter(name='nBaud', value='64', format='int')

opObj11 = procUnitConfObj0.addOperation(name='deFlip')
opObj11.addParameter(name='channelList', value=[1,3,5,7], format='list')

opObj11 = procUnitConfObj0.addOperation(name='CohInt', optype='other')
#opObj11.addParameter(name='n', value='32', format='int')
opObj11.addParameter(name='n', value='24', format='int')

procUnitConfObj1 = controllerObj.addProcUnit(datatype='SpectraProc', inputId=procUnitConfObj0.getId())
procUnitConfObj1.addParameter(name='nFFTPoints', value='64', format='int')
procUnitConfObj1.addParameter(name='nProfiles', value='64', format='int')
#procUnitConfObj1.addParameter(name='ippFactor', value='3', format='int')
#procUnitConfObj1.addParameter(name='pairsList', value='(3,7),(2,6)', format='pairsList')
#procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6),(2,6),(3,7)], format='list')
procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6)], format='list')
 
opObj11 = procUnitConfObj1.addOperation(name='IncohInt', optype='other')
opObj11.addParameter(name='timeInterval', value='60', format='float')
#opObj11.addParameter(name='timeInterval', value='20', format='float')  # to test rx lines

opObj11 = procUnitConfObj1.addOperation(name='SpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2004', format='int')
opObj11.addParameter(name='wintitle', value='MEDIUM SPC', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='zmin', value='15', format='int')
opObj11.addParameter(name='zmax', value='45', format='int')
opObj11.addParameter(name='showprofile', value='1')
opObj11.addParameter(name='xmin', value='-20', format='int')
opObj11.addParameter(name='xmax', value='20', format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='232', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

opObj11 = procUnitConfObj1.addOperation(name='CrossSpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2006', format='int')
opObj11.addParameter(name='wintitle', value='MEDIUM CROSS-SPC', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='232', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

opObj11 = procUnitConfObj1.addOperation(name='CoherencePlot', optype='other')
opObj11.addParameter(name='id', value='102', format='int')
opObj11.addParameter(name='wintitle', value='MEDIUM CMAP', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='232', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

opObj11 = procUnitConfObj1.addOperation(name='PhasePlot', optype='other')
opObj11.addParameter(name='id', value='102', format='int')
opObj11.addParameter(name='wintitle', value='MEDIUM PMAP', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='232', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')
'''
opObj11 = procUnitConfObj1.addOperation(name='RTIPlot', optype='other')
opObj11.addParameter(name='id', value='3005', format='int')
opObj11.addParameter(name='wintitle', value='MEDIUM RTI', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='float')
opObj11.addParameter(name='xmax', value=t[1], format='float')
opObj11.addParameter(name='zmin', value='15', format='int')
opObj11.addParameter(name='zmax', value='45', format='int')
opObj11.addParameter(name='showprofile', value='0', format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='232', format='int')
opObj11.addParameter(name='server', value='10.10.110.243:4444', format='int')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')
opObj11 = procUnitConfObj1.addOperation(name='NoisePlot', optype='other')
opObj11.addParameter(name='id', value='3006', format='int')
opObj11.addParameter(name='wintitle', value='MEDIUM NOISE', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='float')
opObj11.addParameter(name='xmax', value=t[1], format='float')
opObj11.addParameter(name='zmin', value='15', format='int')
opObj11.addParameter(name='zmax', value='45', format='int')
opObj11.addParameter(name='showprofile', value='0', format='int')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='232', format='int')
opObj11.addParameter(name='server', value='10.10.110.243:4444', format='int')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')
'''
controllerObj.start()
