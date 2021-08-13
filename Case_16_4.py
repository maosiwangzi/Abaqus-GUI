# -*- coding: mbcs -*-
import os, os.path, sys
from odbAccess import *
from abaqus import *
from abaqusConstants import *
from caeModules import *
def ODBDataExtraction (OdbPath,ElementNumber):
	o = openOdb(path=OdbPath, readOnly=False)
	elementL = ElementNumber
	instanceL = 'PART-2-1'
	times, stress = [], []
	inst = o.rootAssembly.instances[instanceL]
	ele = inst.getElementFromLabel(label=elementL)
	frames = o.steps['myStep1'].frames
	for frame in frames:
		times.append(frame.frameValue)
		fopS = frame.fieldOutputs['S']
		fopSFromEle = fopS.getSubset(region=ele)
		stress.append(fopSFromEle.values[0].mises)
	
	o.close()
	print('Learn Good')
	stressData = zip(times,stress)
	plotData =  session.XYData(data=stressData,name='Stress at element '+ str(ElementNumber),xValuesLabel='时间 s',yValuesLabel='Stress Mpa')
	stressCurve = session.Curve(xyData=plotData)
	stressPlot = session.XYPlot(name='Stress Plot '+ str(ElementNumber))
	stressPlot.title.setValues(text='Stress at element '+ str(ElementNumber))
	chartName = stressPlot.charts.keys()[0]
	chart = stressPlot.charts[chartName]
	chart.setValues(curvesToPlot=(stressCurve,), )
	chart.gridArea.style.setValues(color='White')
	chart.legend.area.style.setValues(color='Gray')
	myViewport = session.Viewport(name='myViewport',border=OFF,
	    titleBar=OFF,titleStyle=CUSTOM)
	myViewport.setValues(width=120,height=100,origin=(0,-20))
	myViewport.setValues(displayedObject=stressPlot)
	session.viewports['myViewport'].maximize()
	session.printToFile(fileName='stressPlot '+ str(ElementNumber), format=PNG, canvasObjects=(
	     myViewport, ))

