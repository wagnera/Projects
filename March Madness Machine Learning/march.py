#Machine learning for NCAA Basketball Tournament
#Created by Anthony Wagner 2017
#Uses Data from Kaggle NCAA Machine Learning Challenge https://www.kaggle.com/c/march-machine-learning-mania-2017
#Gets Team Stats from http://www.sports-reference.com/cbb/seasons/2017-school-stats.html each year is downloaded as csv to ppg_[year].csv
#Input Teams 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn import svm
import numpy as np
import csv
import math
import random
import matplotlib.pyplot as plt

###################
#Input for Play in Games
#Teams entered as pair (ie first two teams play each other)
Round0=list()
Round0.extend(['North Carolina Central','UC-Davis','Providence','Southern California',"Mount St. Mary's",'New Orleans','Kansas State','Wake Forest']) #For 2017 NCAA Play In Games
Round0INDEXs=[16,11,16,11] #Index is the seed of the teams playing in each game for play in games
#########################

#Enter Teams for round of 64 in order from 1 seed to 16 seed in the order of division Mid-West, West, East, South
#Order= M W E S
Round1=list()
Round1.extend(['North Carolina', 'Kentucky', 'Houston', 'Kansas', 'Auburn', 'Iowa State', 'Wofford', 'Utah State', 'Washington', 'Seton Hall', 'Ohio State', 'New Mexico State', 'Northeastern', 'Georgia State', 'Abilene Christian', 'Iona', 'Gonzaga', 'Michigan', 'Texas Tech', 'Florida State', 'Marquette', 'Buffalo', 'Nevada', 'Syracuse', 'Baylor', 'Florida', 'Arizona State', 'Murray State', 'Vermont', 'Northern Kentucky', 'Montana', 'Fairleigh Dickinson', 'Duke', 'Michigan State', 'Louisiana State', 'Virginia Tech', 'Mississippi State', 'Maryland', 'Louisville', 'Virginia Commonwealth', 'Central Florida', 'Minnesota', 'Belmont', 'Liberty', 'Saint Louis', 'Yale', 'Bradley', 'North Dakota State', 'Virginia', 'Tennessee', 'Purdue', 'Kansas State', 'Wisconsin', 'Villanova', 'Cincinnati', 'Mississippi', 'Oklahoma', 'Iowa', "Saint Mary's (CA)", 'Oregon', 'UC-Irvine', 'Old Dominion', 'Colgate', 'Gardner-Webb'])#['Virginia','Michigan State','Utah','Iowa State','Purdue','Seton Hall','Dayton','Texas Tech','Butler','Syracuse','Gonzaga','Arkansas-Little Rock','Iona','Fresno State','Middle Tennessee','Hampton','Oregon','Oklahoma','Texas A&M','Duke','Baylor','Texas','Oregon State',"Saint Joseph's",'Cincinnati','Virginia Commonwealth','Northern Iowa','Yale','North Carolina-Wilmington','Green Bay','Cal State Bakersfield','Southern','North Carolina','Xavier','West Virginia','Kentucky','Indiana','Notre Dame','Wisconsin','Southern California','Providence','Pittsburgh','Michigan','Chattanooga','Stony Brook','Stephen F. Austin','Weber State','Fairleigh Dickinson','Kansas','Villanova','Miami (FL)','University of California','Maryland','Arizona','Iowa','Colorado','Connecticut','Temple','Vanderbilt','South Dakota State','Hawaii','Buffalo','North Carolina-Asheville','Austin Peay'])

teams=list() #Initialize list for teams found in data from http://www.sports-reference.com/cbb/seasons/2017-school-stats.html
ppg=list() #intialize lists
opp=list()
SRS=list()
SOS=list()
raw=list()

##########################
#Begin Reading in stats  #
##########################
NYearsData=0;
print("Found the following CSV files:")
try:
	while 1:
		fileNAME='ppg_'+str(2019-NYearsData)+'.csv' #create filename for next csv
		print(fileNAME) 
		with open(fileNAME, 'r') as PPG: #open file
			PPG_read = csv.reader(PPG, delimiter=',')
			ppgTemp=list()
			oppTemp=list()
			teamsTemp=list()
			SRSTemp=list()
			SOSTemp=list()
			count=0
			for row in PPG_read:
				if count > 1:
					if '*' in row[1]:
						teamsTemp.append(row[1].replace(" *","")) #Add teams while removing * denoting NCAA tournament team
						ppgTemp.append(int(row[14])) #Get points per game
						oppTemp.append(int(row[15])) #Get oppnent points
						SRSTemp.append(float(row[6])) #Get SRS
						SOSTemp.append(float(row[7])) #Get strength of Schedule
						
					else:
						teamsTemp.append(row[1])
						ppgTemp.append(int(row[14]))
						oppTemp.append(int(row[15]))
						SRSTemp.append(float(row[6]))
						SOSTemp.append(float(row[7]))
				else:
					count=count+1
		
		SOS.append(SOSTemp) #Append years worth of stats to 3D list 
		SRS.append(SRSTemp)
		teams.append(teamsTemp)
		ppg.append(ppgTemp)
		opp.append(oppTemp)
		NYearsData=NYearsData+1 #Increment counter for years of data
except: #once we run out of CSV files
	pass

print("Number of years Data Found:",NYearsData)	

##########################################
#Read in Auilary data from Kaggle Sources#
##########################################
FoundTeams=list() #List of teams from Kaggle Data
MissingTeams=list() #Initialize list for teams not found
TeamsIndex=list() #List of indexs 
TEAMS_REA=list()
with open('teams.csv', 'r') as TEAMS:
	TEAMS_read = csv.reader(TEAMS, delimiter=',')
	for row in TEAMS_read:
		TEAMS_REA.append(row)
print([el[1] for el in TEAMS_REA][2])		
for year in range(NYearsData):
	FoundTeamsTemp=list()
	TeamsIndexTemp=list()
	for row in teams[year]:
		if row in [el[1] for el in TEAMS_REA]:
			ind=[el[1] for el in TEAMS_REA].index(row)
			FoundTeamsTemp.append([el[1] for el in TEAMS_REA][ind])#row[1]
			TeamsIndexTemp.append([el[0] for el in TEAMS_REA][ind])#row[0]
	FoundTeams.append(FoundTeamsTemp)
	TeamsIndex.append(TeamsIndexTemp)

for year in range(NYearsData):
	MissingTeamsTemp=list()
	for row in teams[year]: #find misssing teams
		if row not in FoundTeams[year]:
			MissingTeamsTemp.append(row)
	MissingTeams.append(MissingTeamsTemp)
print("Teams not found ", MissingTeams)
	

for year in range(NYearsData):
	for row in MissingTeams[year]: #remove missing teams
		INDEX=teams[year].index(row)
		teams[year].remove(row)
		del opp[year][INDEX]
		del ppg[year][INDEX]
		del SRS[year][INDEX]
		del SOS[year][INDEX]
	
############################################################


count3=0
DATAin=list()
winner=list()
Datatemp=list()
missingTcount=0
'''
with open('regular_season_detailed_results.csv', 'r') as RESULTS:
	RESULTS_read = csv.reader(RESULTS, delimiter=',')
	for row in RESULTS_read:
		try:	
			Datatemp=list()
			T1=random.choice([2,4])
			#T1=4
			if T1 is 2:
				T2=4
				#winner.append(1)
			if T1 is 4:
				T2=2
				#winner.append(0) 
			#print(row[T1], " ", row[T2])
			T1ind=TeamsIndex.index(row[T1])
			T2ind=TeamsIndex.index(row[T2])
			T1ppg=ppg[T1ind]
			T2ppg=ppg[T2ind]
			T1opp=opp[T1ind]
			T2opp=opp[T2ind]
			T1SRS=SRS[T1ind]
			T2SRS=SRS[T2ind]
			T1SOS=SOS[T1ind]
			T2SOS=SOS[T2ind]
			Datatemp=raw[T1ind]+raw[T2ind]
			#Datatemp.extend([T1ppg-T2ppg,T1opp-T2opp,T1SOS-T2SOS,T1SRS-T1SOS])
			DATAin.append(Datatemp)
			#print(Datatemp)
			#print(DATAin[len(DATAin)-1])
			#print(ppg[T1ind])
			if T1 is 2:
				winner.append(1)
			if T1 is 4:
				winner.append(0) 	
		except:
			missingTcount=missingTcount+1
			pass

'''
seed=list()
TSeedind=list()
for i in range(NYearsData):
	seed.append([])
	TSeedind.append([])

with open('NCAATourneySeeds.csv', 'r') as RESULTS:
	RESULTS_read = csv.reader(RESULTS, delimiter=',')
	for row in RESULTS_read:
		year=2019-int(row[0])
		if year < NYearsData:
			TSeedind[year].append(row[2])
			seed[year].append(int(row[1][1:3]))
		
#print(seed,'\n',TSeedind)
#print(teams[2])
#print(SOS[2][teams[2].index('Duke')])
#print(TeamsIndex[2],'\n',teams[2],'\n',SOS[2],'\n',TeamsIndex[2].index('1463'),SOS[2][TeamsIndex[2].index('1463')],SOS[2].index(-5.18),len(teams[2]),len(TeamsIndex[2]))
with open('NCAATourneyCompactResults.csv', 'r') as RESULTS:
	RESULTS_read = csv.reader(RESULTS, delimiter=',')
	for row in RESULTS_read:
		try:	
			Datatemp=list()
			T1=random.choice([2,4])
			#T1=4
			if T1 is 2:
				T2=4
				#winner.append(1)
			if T1 is 4:
				T2=2
				#winner.append(0) 
			#print(row[T1], " ", row[T2])
			year=2019-int(row[0])
			if year < NYearsData:
				T1ind=TSeedind[year].index(row[T1])
				T2ind=TSeedind[year].index(row[T2])
				T1seed=seed[year][T1ind]
				T2seed=seed[year][T2ind]
				T1ind=TeamsIndex[year].index(row[T1])
				T2ind=TeamsIndex[year].index(row[T2])
				T1ppg=ppg[year][T1ind]
				T2ppg=ppg[year][T2ind]
				T1opp=opp[year][T1ind]
				T2opp=opp[year][T2ind]
				T1SRS=SRS[year][T1ind]
				T2SRS=SRS[year][T2ind]
				T1SOS=SOS[year][T1ind]
				T2SOS=SOS[year][T2ind]
				#Datatemp=raw[T1ind]+raw[T2ind]
				Datatemp.extend([T1seed-T2seed,T1ppg-T2ppg,T1opp-T2opp,T1SOS-T2SOS,T1SRS-T2SRS])
				DATAin.append(Datatemp)
				#Datatemp=list()
				#Datatemp.extend([T2seed-T1seed,T2ppg-T1ppg,T2opp-T1opp,T2SOS-T1SOS,T2SRS-T1SOS])
				#DATAin.append(Datatemp)
				#print(Datatemp)
				#print(DATAin[len(DATAin)-1])
				#print(ppg[T1ind])
				if T1 is 2:
					winner.append(1)
					#winner.append(0)
				if T1 is 4:
					winner.append(0)
					#winner.append(1)					
		except:
			print("Missing Game is: ", row)	
			missingTcount=missingTcount+1
			pass



#print(DATAin)			
DATAin=np.array(DATAin).astype(np.float)						
print("OPP " ,len(opp))
print("PPG " ,len(ppg))
print("Teams " ,len(teams))
#print("#raw ", len(raw))
print("tea index ", len(TeamsIndex))
print("#of Winners ", len(winner))
print("#of Datasets ", len(DATAin))
print("Number of Missing Games: ", missingTcount)
#print(winner)
#print(DATAin)
if len(teams) is not len(ppg):
	print('Error number of teams does not match')

teamst=list()
oppt=list()
ppgt=list()
SOSt=list()
SRSt=list()
'''
with open('opp_14.csv', 'r') as OPPt:
	OPPt_read = csv.reader(OPPt, delimiter=',')
	for row in OPPt_read:
		if '*' in row[1]:
			teamst.append(row[1].replace(" *",""))
			oppt.append(int(row[15]))
			count=count+1
			
count1 = 0
with open('ppg_14.csv', 'r') as PPGt:
	PPGt_read = csv.reader(PPGt, delimiter=',')
	for row in PPGt_read:
		if '*' in row[1]:
			ppgt.append(int(row[15]))
			SRSt.append(float(row[6]))
			SOSt.append(float(row[7]))
'''

X_train, X_test, y_train, y_test = train_test_split(DATAin,winner, test_size=0.000001, random_state=0)
print('Training SVC: ')
clf=svm.SVC()
clf.fit(X_train,y_train)
print("SVC Accuracy Test: ",clf.score(X_test,y_test))
########################
print('Training GNB: ')
gnb = GaussianNB()
gnb.fit(X_train,y_train)
print("GNB Accuracy Test: ",gnb.score(X_test,y_test))
print(gnb.predict_proba(X_test[0].reshape(1, -1)))
########################
print('Training BNB: ')
bnb = BernoulliNB()
bnb.fit(X_train,y_train)
print("BNB Accuracy Test: ",bnb.score(X_test,y_test))
#######################
'''
print('Training kNN: ')
test_result=list()
for jj in range (1,200,20):
	neigh = KNeighborsClassifier(n_neighbors=jj,p=1)
	neigh.fit(X_train,y_train)
	print("kNN Accuracy Test for",jj," neighbors: ",neigh.score(X_test,y_test))
	test_result.append(neigh.score(X_test,y_test))

plt.plot(test_result)
plt.ylabel('some numbers')
plt.show()'''

'''
T2t='Kentucky'
T1t='Hampton'			
T1tind=teamst.index(T1t)
T2tind=teamst.index(T2t)
testData=list()
#testData.extend([ppgt[T1tind],ppgt[T2tind],oppt[T1tind],oppt[T2tind],SRSt[T1tind],SRSt[T2tind],SOSt[T1tind],SOSt[T2tind]])	
#testData=raw[T1tind]+raw[T2tind]	

print(testData)	
print('Teting kNN: ')
print(neigh.predict([testData]))		
print(neigh.predict_proba([testData]))
print('Teting GNB: ')
#print(.predict_proba([testData]))
'''
print(Round0)
FoundTourneyTeams0=list()
TeamsTourneyIndex0=list()
TourneyData0=list()
year=0
for iii in range(8):#Round0:
	if Round0[iii] in teams[year]:#row in teams[1]:
		print(Round0[iii])
		FoundTourneyTeams0.append(Round0[iii])
		TeamsTourneyIndex0.append(Round0[iii])
		Tind=teams[year].index(Round0[iii])
		print(type(year),type(Tind))
		TourneyData0.append([Round0INDEXs[int(math.floor(iii/2))],ppg[year][Tind],opp[year][Tind],SRS[year][Tind],SOS[year][Tind]])
	else:
		print("Team Not found: ",Round0[iii])

print(FoundTourneyTeams0,TourneyData0)
GameData=list()
for i in range(0,7,2):
	#print(i)
	GameData=[TourneyData0[i][0]-TourneyData0[i+1][0],TourneyData0[i][1]-TourneyData0[i+1][1],TourneyData0[i][2]-TourneyData0[i+1][2],TourneyData0[i][3]-TourneyData0[i+1][3],TourneyData0[i][4]-TourneyData0[i+1][4]]
	print(GameData)
	GameData=np.array(GameData).astype(np.float)	
	WL=gnb.predict([GameData])
	print(WL[0])
	if WL[0] == 1:
		print("Winner is: ",FoundTourneyTeams0[i])
	else:
		print("Winner is: ",FoundTourneyTeams0[i+1])
########################
print(len(Round1))
print(Round1)
FoundTourneyTeams1=list()
TeamsTourneyIndex1=list()
TourneyData1=list()
year=1
seedd=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
for iii in range(64):#Round0:
	if Round1[iii] in teams[year]:#row in teams[1]:
		print(Round1[iii])
		FoundTourneyTeams1.append(Round1[iii])
		TeamsTourneyIndex1.append(Round1[iii])
		Tind=teams[year].index(Round1[iii])
		TourneyData1.append([seedd[iii],ppg[year][Tind],opp[year][Tind],SRS[year][Tind],SOS[year][Tind]])
	else: 
		print("Team not found: ",Round1[iii])
print(FoundTourneyTeams1,TourneyData1,'\n',len(FoundTourneyTeams1),len(TourneyData1))
T2List=[15,14,13,12,11,10,9,8,31,30,29,28,27,26,25,24,47,46,45,44,43,42,41,40,63,62,61,60,59,58,57,56]
T1List=[0,1,2,3,4,5,6,7,16,17,18,19,20,21,22,23,32,33,34,35,36,37,38,39,48,49,50,51,52,53,54,55]
print(len(T1List),len(T2List))
GameData=list()
R1Win=list()
for i in range(0,32,1):
	T1=T1List[i]
	T2=T2List[i]
	print(T1," " ,T2)
	GameData=[TourneyData1[T1][0]-TourneyData1[T2][0],TourneyData1[T1][1]-TourneyData1[T2][1],TourneyData1[T1][2]-TourneyData1[T2][2],TourneyData1[T1][3]-TourneyData1[T2][3],TourneyData1[T1][4]-TourneyData1[T2][4]]
	#print(GameData)
	GameData=np.array(GameData).astype(np.float)	
	WL=gnb.predict([GameData])
	print("Match up of: ",FoundTourneyTeams1[T1],"  ",FoundTourneyTeams1[T2])
	if WL[0] == 1:
		print("Winner is: ",FoundTourneyTeams1[T1])
		R1Win.append([FoundTourneyTeams1[T1],TourneyData1[T1]])
	else:
		print("Winner is: ",FoundTourneyTeams1[T2])
		R1Win.append([FoundTourneyTeams1[T2],TourneyData1[T2]])
print(R1Win)
##################################
T2List=[7,6,5,4,15,14,13,12,23,22,21,20,31,30,29,28]
T1List=[0,1,2,3,8,9,10,11,16,17,18,19,24,25,26,27]
print(len(T1List),len(T2List))
R2Win=list()
GameData=list()
for i in range(0,16,1):
	T1=T1List[i]
	T2=T2List[i]
	GameData=[R1Win[T1][1][0]-R1Win[T2][1][0],R1Win[T1][1][1]-R1Win[T2][1][1],R1Win[T1][1][2]-R1Win[T2][1][2],R1Win[T1][1][3]-R1Win[T2][1][3],R1Win[T1][1][4]-R1Win[T2][1][4]]
	GameData=np.array(GameData).astype(np.float)	
	WL=gnb.predict([GameData])
	print("Match up of: ",R1Win[T1][0],"  ",R1Win[T2][0])
	if WL[0] == 1:
		print("Winner is: ",R1Win[T1][0])
		R2Win.append(R1Win[T1])
	else:
		print("Winner is: ",R1Win[T2][0])
		R2Win.append(R1Win[T2])
print(R2Win)
########################
T2List=[3,2,7,6,11,10,15,14]
T1List=[0,1,4,5,8,9,12,13]
print(len(T1List),len(T2List))
R3Win=list()
GameData=list()
for i in range(0,8,1):
	T1=T1List[i]
	T2=T2List[i]
	GameData=[R2Win[T1][1][0]-R2Win[T2][1][0],R2Win[T1][1][1]-R2Win[T2][1][1],R2Win[T1][1][2]-R2Win[T2][1][2],R2Win[T1][1][3]-R2Win[T2][1][3],R2Win[T1][1][4]-R2Win[T2][1][4]]
	GameData=np.array(GameData).astype(np.float)	
	WL=gnb.predict([GameData])
	print("Match up of: ",R2Win[T1][0],"  ",R2Win[T2][0])
	if WL[0] == 1:
		print("Winner is: ",R2Win[T1][0])
		R3Win.append(R2Win[T1])
	else:
		print("Winner is: ",R2Win[T2][0])
		R3Win.append(R2Win[T2])
print(R3Win)
########################
T2List=[1,3,5,7]
T1List=[0,2,4,6]
print(len(T1List),len(T2List))
R4Win=list()
GameData=list()
for i in range(0,4,1):
	T1=T1List[i]
	T2=T2List[i]
	GameData=[R3Win[T1][1][0]-R3Win[T2][1][0],R3Win[T1][1][1]-R3Win[T2][1][1],R3Win[T1][1][2]-R3Win[T2][1][2],R3Win[T1][1][3]-R3Win[T2][1][3],R3Win[T1][1][4]-R3Win[T2][1][4]]
	GameData=np.array(GameData).astype(np.float)	
	WL=gnb.predict([GameData])
	print("Match up of: ",R3Win[T1][0],"  ",R3Win[T2][0])
	if WL[0] == 1:
		print("Winner is: ",R3Win[T1][0])
		R4Win.append(R3Win[T1])
	else:
		print("Winner is: ",R3Win[T2][0])
		R4Win.append(R3Win[T2])
print(R4Win)
########################
T2List=[0,1]
T1List=[3,2]
print(len(T1List),len(T2List))
R5Win=list()
GameData=list()
for i in range(0,2,1):
	T1=T1List[i]
	T2=T2List[i]
	GameData=[R4Win[T1][1][0]-R4Win[T2][1][0],R4Win[T1][1][1]-R4Win[T2][1][1],R4Win[T1][1][2]-R4Win[T2][1][2],R4Win[T1][1][3]-R4Win[T2][1][3],R4Win[T1][1][4]-R4Win[T2][1][4]]
	GameData=np.array(GameData).astype(np.float)	
	WL=gnb.predict([GameData])
	print("Match up of: ",R4Win[T1][0],"  ",R4Win[T2][0])
	if WL[0] == 1:
		print("Winner is: ",R4Win[T1][0])
		R5Win.append(R4Win[T1])
	else:
		print("Winner is: ",R4Win[T2][0])
		R5Win.append(R4Win[T2])
print(R5Win)
########################
T1=0
T2=1
GameData=[R5Win[T1][1][0]-R5Win[T2][1][0],R5Win[T1][1][1]-R5Win[T2][1][1],R5Win[T1][1][2]-R5Win[T2][1][2],R5Win[T1][1][3]-R5Win[T2][1][3],R5Win[T1][1][4]-R5Win[T2][1][4]]
GameData=np.array(GameData).astype(np.float)	
WL=gnb.predict([GameData])
print("Match up of: ",R5Win[T1][0],"  ",R5Win[T2][0])
if WL[0] == 1:
	print("Overall Winner is: ",R5Win[T1][0])
	WINNER=R5Win[T1][0]
else:
	print("Overall Winner is: ",R5Win[T2][0])
	WINNER=R5Win[T2][0]
'''
print(len(Round1))
if len(Round1) is 64:
	for i in range(64):
		print(Round1.pop(15-i))
		T1tind=teamst.index(Round1.pop(i))
		T2tind=teamst.index(Round1.pop(15-i))
		testData=raw[T1tind]+raw[T2tind]	
		print(testData)	
		print(neigh.predict([testData]))		
		print(neigh.predict_proba([testData]))	
else:
	print("Number of teams is not 64")
'''


'''
forest = ExtraTreesClassifier(n_estimators=250,random_state=0)

forest.fit(DATAin, winner)
importances = forest.feature_importances_
std = np.std([tree.feature_importances_ for tree in forest.estimators_],axis=0)
indices = np.argsort(importances)[::-1]

#Print the feature ranking
print("Feature ranking:")

for f in range(1,100):
    print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
'''






















