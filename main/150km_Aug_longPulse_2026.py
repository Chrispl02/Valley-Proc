import os, sys

from schainpy.controller import Project

desc = "150 km Jicamarca January 2015"
filename = "150km_jicamarca.xml"

controllerObj = Project()

controllerObj.setup(id = '191', name='test01', description=desc)

dpath = '/mnt/share/Valley/main_radar/rawdata'
figpath = '/home/david/Documents/DATA-3/Valley/25_28_Aug_26/27_Aug_26'
online=0
delay=30
walk=1
startDate='2026/08/27'
endDate='2026/08/27'
startTime='09:00:00'
endTime='11:59:59'
t=['9','12']

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

opObj11 = procUnitConfObj0.addOperation(name='deFlip')
opObj11.addParameter(name='channelList', value=[1,3,5,7], format='list')

procUnitConfObj1 = controllerObj.addProcUnit(datatype='SpectraProc', inputId=procUnitConfObj0.getId())
procUnitConfObj1.addParameter(name='nFFTPoints', value='64', format='int')
procUnitConfObj1.addParameter(name='nProfiles', value='64', format='int')
#procUnitConfObj1.addParameter(name='pairsList', value='(3,7),(2,6)', format='pairsList')
#procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6),(2,6),(3,7)], format='list')
procUnitConfObj1.addParameter(name='pairsList', value=[(1,0),(3,2),(5,4),(7,6)], format='list')

opObj11 = procUnitConfObj1.addOperation(name='IncohInt', optype='other')
#opObj11.addParameter(name='timeInterval', value='120', format='float')
opObj11.addParameter(name='timeInterval', value='60', format='float')
#opObj11.addParameter(name='timeInterval', value='20', format='float')

'''opObj11 = procUnitConfObj1.addOperation(name='SpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2001', format='int')
opObj11.addParameter(name='wintitle', value='LONG SPC', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='zmin', value='15', format='int')
opObj11.addParameter(name='zmax', value='60', format='int')
opObj11.addParameter(name='showprofile', value='1')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='233', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')'''


'''opObj11 = procUnitConfObj1.addOperation(name='CrossSpectraPlot', optype='other')
opObj11.addParameter(name='id', value='2005', format='int')
opObj11.addParameter(name='wintitle', value='LONG CROSS-SPC', format='str')
opObj11.addParameter(name='xaxis', value='velocity', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='233', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')'''


opObj11 = procUnitConfObj1.addOperation(name='CoherencePlot', optype='other')
opObj11.addParameter(name='id', value='101', format='int')
opObj11.addParameter(name='wintitle', value='LONG CMAP', format='str')
opObj11.addParameter(name='coherence_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
#opObj11.addParameter(name='zmin', value=0.0, format='int')
#opObj11.addParameter(name='zmax', value=1.0, format='int')
opObj11.addParameter(name='showprofile', value='1')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='233', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')


opObj11 = procUnitConfObj1.addOperation(name='PhasePlot', optype='other')
opObj11.addParameter(name='id', value='102', format='int')
opObj11.addParameter(name='wintitle', value='LONG PMAP', format='str')
opObj11.addParameter(name='phase_cmap', value='jet', format='str')
opObj11.addParameter(name='xmin', value=t[0], format='int')
opObj11.addParameter(name='xmax', value=t[1], format='int')
opObj11.addParameter(name='showprofile', value='1')
opObj11.addParameter(name='save', value=figpath, format='str')
opObj11.addParameter(name='exp_code', value='233', format='int')
opObj11.addParameter(name='server', value='10.10.120.138:4444', format='str')
opObj11.addParameter(name='tag', value= 'jicamarca', format='str')

controllerObj.start()
