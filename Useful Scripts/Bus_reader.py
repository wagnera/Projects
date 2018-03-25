import json
import datetime
import matplotlib.pyplot as plt
import numpy as np

def plotbusses(buses,begin,end):
	#begin = np.array([2003,1991,2008,1986,2013,1994,2002])
	#end =   np.array([2007,2016,2016,2015,2013,1999,2002])
	plt.barh(range(len(begin)),  end-begin, left=begin)

	plt.yticks(range(len(begin)), buses)
	plt.show()

def TSC(unix_time):
	return datetime.datetime.fromtimestamp(unix_time).strftime('%D %H:%M')



#Loads data from json
data =list()
with open('sept28.json') as data_file:
	for line in data_file:
		try:
			data.append(json.loads(line))
		except:
			pass
Routes=list()
buses_ids={}

#Reads in all of the routes
print 'Read in ',len(data),' requests'
for ii in data:
	for jj in ii[0]['buses']:
		Routes.append(jj['route'])
Routes=set(Routes)
Routes=list(Routes)
print "Routes:\n", Routes		

#Reads in all of the buses for each route
busID_temp=list()
all_ids=list()
for i in range(len(Routes)):
	busID_temp.append(list())

for ii in data:
	for jj in ii[0]['buses']:
		for kk in range(len(Routes)):
			if jj['route'] == Routes[kk]:
				busID_temp[kk].append(int(jj['busId']))
				all_ids.append(int(jj['busId']))
for (r,i) in zip(Routes,busID_temp):
	buses_ids[str(r)]=list(set(i))
all_ids=list(set(all_ids))
for Route in Routes:
	print Route," had ",len(buses_ids[Route])," different buses", buses_ids[Route]
print all_ids

#Calcualte when each bus was operating
RouteIDs={} #Dict for each route+busid
for Route in Routes:
	for bus in buses_ids[Route]:
		RouteIDs[Route+','+str(bus)]=[]

for RouteID in RouteIDs:
	[Route,bus]=RouteID.split(',')
	for ii in data:
		for jj in ii[0]['buses']:
			if jj['route'] == Route:
				if jj['busId'] == bus:
					RouteIDs[RouteID].append(jj['timestamp']/1000)					
for RouteID in RouteIDs:
	[Route,bus]=RouteID.split(',')
	ii=RouteIDs[RouteID]
	temp=[ii[len(ii)-1]-ii[0],ii[0],ii[len(ii)-1]]	
	RouteIDs[RouteID]=temp


plotbegin=list()
plotend=list()
plotlabels=list()
for Route in Routes:
	for rid in RouteIDs:
		[r,bus]=rid.split(',')
		if Route == r:
			temp=RouteIDs[rid]
			plotlabels.append(rid)
			plotbegin.append(temp[1])
			plotend.append(temp[2])
			print Route,":",bus," Duration: ", temp[0]/3600,"From: ",TSC(temp[1])," until ",TSC(temp[2])
#plotbusses(plotlabels,np.asarray(plotbegin),np.asarray(plotend))

#init=0
#for ii in data:
#	for jj in ii[0]['buses']:
#		if jj['route'] == 'HWB' and jj['busId']=='6012' and jj['lastStopCode'] == '1206':
#			print(TSC(jj['timestamp']/1000))
