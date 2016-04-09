#!/usr/bin/python

fileName="datafile.csv"
#<Got lazy on the next two lines... Should have used a dictionary structure to specify rankings; would have needed editing of entire program structure (skipped)>
programTypeNamesList=["24 Hour Residential","Residential Services","CLA (Community Living Arrangement)","Community Living Arrangement","CR-Group Home (Community Residence - Supervised)","Community Residence","Supported Employment","Shared Living"]#,"DS (Day Services)","DH (Day Habilitation Site)"]
programTypeRankings=[1,1,2,2,3,3,4,5]#,6,7]

def swapRows(list2d,row1,row2):
	temp=list2d[row1]
	list2d[row1]=list2d[row2]
	list2d[row2]=temp

def partition(fullArray,columnIndex,indexStart,indexEnd):
	pivotIndex=(indexStart+indexEnd)/2
	pivotValue=fullArray[pivotIndex][columnIndex]
	swapRows(fullArray,pivotIndex,indexEnd)
	storeIndex=indexStart

	for j in range(indexStart,indexEnd):
		if(fullArray[j][columnIndex]<=pivotValue):
			swapRows(fullArray,storeIndex,j)
			storeIndex+=1
	swapRows(fullArray,storeIndex,indexEnd)
	return storeIndex	

def quickSort(masterArray,colIndex,lIndex,rIndex):
	if(lIndex<rIndex):	
		partitionIndex=partition(masterArray,colIndex,lIndex,rIndex)
		quickSort(masterArray,colIndex,lIndex,partitionIndex-1)
		quickSort(masterArray,colIndex,partitionIndex+1,rIndex)

def intConvert(numString):
	if(numString!=""):
		return int(numString)
	return -1

def nonTrivialEqStr(record1,record2,colIndex):
	if((record1[colIndex]!="")and(record2[colIndex]!="")):
		return (record1[colIndex]==record2[colIndex])
	return False

def nonTrivialEqInt(record1,record2,colIndex):
	if((record1[colIndex]!="")and(record2[colIndex]!="")):
		return (intConvert(record1[colIndex])==intConvert(record2[colIndex]))
	return False
		
def matchedPatient(dataSet,i1,i2):
	if( nonTrivialEqStr(dataSet[i1],dataSet[i2],5) and (nonTrivialEqInt(dataSet[i1],dataSet[i2],6) or nonTrivialEqStr(dataSet[i1],dataSet[i2],7) or nonTrivialEqInt(dataSet[i1],dataSet[i2],8)) ):	# Date of Birth (none missing) match and at least one of Patient ID, SSN or Medicaid No. matched
		print "case 1"		
		print str(dataSet[i1])
		print str(dataSet[i2])
		return True
	elif( ((dataSet[i1][5]=="")or(dataSet[i2][5]=="")) and (dataSet[i1][5]!=dataSet[i2][5]) and (nonTrivialEqInt(dataSet[i1],dataSet[i2],6) or nonTrivialEqStr(dataSet[i1],dataSet[i2],7) or nonTrivialEqInt(dataSet[i1],dataSet[i2],8)) ):	# Missing Date of Birth in one or both records and match in at least one of Patient ID, SSN or Medicaid No. 
		print "case 2"
		print str(dataSet[i1])
		print str(dataSet[i2])
		return True
	return False

def singlePovider(records,rptList):
	provider1=records[rptList[0]][1]
	j=1
	while(j<len(rptList)):
		if(records[rptList[j]][1]!=provider1):
			return False
		j+=1
	return True

def selectFromMultipleProviders(record,rptList):
	topPriority=rptList[0]
	topPriorityLevel=max(programTypeRankings)+1
	for p in rptList:
		programTypeName=record[p][11]
		priorityLevel=len(programTypeNamesList)+1
		if(programTypeName==""):
			priorityLevel=max(programTypeRankings)+1
		elif(programTypeName in programTypeNamesList):
			priorityLevel=programTypeRankings[programTypeNamesList.index(programTypeName)]
		else:
			return -1
		if(priorityLevel<topPriorityLevel):
			topPriorityLevel=priorityLevel
			topPriority=p
		elif(priorityLevel==topPriorityLevel):
			numMissingDataOld=0
			numMissingDataNew=0
			for a in [5,6,7,8]:
				if(record[topPriority][a]==""):
					numMissingDataOld+=1
				if(record[p][a]==""):
					numMissingDataNew+=1
			if(numMissingDataNew<numMissingDataOld):
				topPriority=p
	return topPriority

def selectRecord(records,rptListRes,rptListDay):
	if(len(rptListRes)==1):
		return rptListRes[0]
	elif((len(rptListRes)==0)and(len(rptListDay)==1)):	
		return rptListDay[0]
	elif(len(rptListRes)>1):
		if(singlePovider(records,rptListRes)):
			return rptListRes[0]
		return selectFromMultipleProviders(record,rptListRes)
	elif((len(rptListRes)==0)and(len(rptListDay)>1)):
		if(singlePovider(records,rptListDay)):
			return rptListDay[0]
		return selectFromMultipleProviders(record,rptListDay)
	return -1

def writeRecord(dataFile,record): 
	for colIndex in range(len(record)):
		dataFile.write(str(record[colIndex])+",")
	dataFile.write('\n')

def createPlaceholder(records,index):
	records[index][0]="--"
	records[index][1]="--"
	records[index][4]="--"
	records[index][6]="--"
	records[index][7]="--"
	records[index][8]="--"
	records[index][10]="--"
	records[index][11]="--"

print "\n# Python Script for Processing Patient Data for Therap Services LLC"
print "\n# Author: Abdullah Al Rashid, University of Toronto (abdullah.alrashid@utoronto.ca)\n"
print "\n# Date Started: July 21, 2014\n# Last Updated: July 22, 2014"
print "\n# Disclaimer:"
print "#\t1. This software comes with no warranty regarding performance or accuracy of results."
print "#\t2. User assumes liability for legal usage."
print "#\t3. This is free, open-source software, with no restrictions imposed on its copying and re-distribution."
print "# (-C-) 2014 Copyleft Abdullah Al Rashid at the University of Toronto\n"

from csv import reader
patientRecordsFile=open(fileName,"rb")
patientRecordsHeadings=[]
patientRecords=[]
patientData=reader(patientRecordsFile)
rowIndex=0
for record in patientData:
	if(rowIndex>0):
		patientRecords.append(record)
	else:
		patientRecordsHeadings=record
	rowIndex+=1
print "# Step 1 of 6 ... Patient records read from data file"
print str(patientRecords)

# Sorting records by last name
quickSort(patientRecords,2,0,len(patientRecords)-1)
print "# Step 2 of 6 ... Patient records sorted by last name"

# Sorting records by first name, in addition to last name
j=0
while(j<len(patientRecords)):
	jStart=j	
	lastNameKey=patientRecords[j][2]
	while((j+1<len(patientRecords))and(patientRecords[j+1][2]==lastNameKey)):	
		j+=1
	if(j>jStart):
		quickSort(patientRecords,3,jStart,j)
	j+=1
print "# Step 3 of 6 ... Patient records further sorted by first name"
#for ll in range(len(patientRecords)):
#	print str(patientRecords[ll])

# Searching for repeated patients and retaining only the most relevant entry from the repeated entries
unresolvedDataFile=open("unresolved_data.csv",'w')
unresolvedDataHeader=["insert_into_row"]
unresolvedDataHeader.append(patientRecordsHeadings)
writeRecord(unresolvedDataFile,unresolvedDataHeader)
# unresolvedDataFile.write() # Writing header data into unresolvedDataFile
l=0
while(l<len(patientRecords)):
	rptRes=[]
	rptDay=[]
	rptAll=[]
	if(patientRecords[l][9]=="1-Residential"):
		rptRes.append(l)
		rptAll.append(l)
	elif(patientRecords[l][9]=="2-Day"):
		rptDay.append(l)
		rptAll.append(l)
	lRpt=l
	while((lRpt+1<len(patientRecords))and(patientRecords[lRpt+1][2]==patientRecords[l][2])and(patientRecords[lRpt+1][3]==patientRecords[l][3])):
		if((matchedPatient(patientRecords,l,lRpt+1)==True)and(patientRecords[lRpt+1][9]=="1-Residential")):
			rptRes.append(lRpt+1)
			rptAll.append(lRpt+1)
		elif((matchedPatient(patientRecords,l,lRpt+1)==True)and(patientRecords[lRpt+1][9]=="2-Day")):
			rptDay.append(lRpt+1)
			rptAll.append(lRpt+1)
		lRpt+=1
		
	# Deleting any repeated patient records after selecting what to retain
	if(len(rptAll)>1):
		indexRetained=selectRecord(patientRecords,rptRes,rptDay)
		rptAll.pop(0)	# Removing the retained record from the list of records to be deleted
		if(indexRetained!=-1):
			patientRecords[l]=patientRecords[indexRetained]	# Moving record to be retained to the front of the list
		else:	# Writing unclassifiable data into a separate file
			createPlaceholder(patientRecords,l)	# Creaing a placeholder to be filled in manually
			unresolvedDataFile.write("#%.4d," %(l+2))
			for iUnc in rptAll:
				writeRecord(unresolvedDataFile,patientRecords[iUnc])
			unresolvedDataFile.write(",,,,,,,,,,,,\n")
		# Deletion of spurious and unclassified records
		while(len(rptAll)>0):
			patientRecords.pop(rptAll[len(rptAll)-1])
			rptAll.pop(len(rptAll)-1)
				
	l+=1
unresolvedDataFile.close()
print "# Step 4 of 6 ... Spurious and unresolvable patient records purged"
			
# Outputting a pruned/updated record of patient information
updatedDataFile=open("updated_data.csv",'w')
writeRecord(updatedDataFile,patientRecordsHeadings)
for dataIndex in range(len(patientRecords)):
	writeRecord(updatedDataFile,patientRecords[dataIndex])
updatedDataFile.close()
print "# Step 5 of 6 ... Updated data file saved"

# Generating a final report summarizing key information as per the stipulated requirements
quickSort(patientRecords,1,0,len(patientRecords)-1)
reportFile=open("report.csv",'w')
reportFile.write("provider_code,num_residential_patients,num_day_patients,state_of_DE,\n")
m=0
while(m<len(patientRecords)):
	mStart=m
	statusDelaware=bool("Delaware" in patientRecords[mStart][0])
	resCount=0
	dayCount=0
	providerKey=patientRecords[mStart][1]
	if(patientRecords[m][9]=="1-Residential"):
		resCount+=1
	elif(patientRecords[m][9]=="2-Day"):
		dayCount+=1
	while((m+1<len(patientRecords))and(patientRecords[m+1][1]==providerKey)):
		if(patientRecords[m+1][9]=="1-Residential"):
			resCount+=1
		elif(patientRecords[m+1][9]=="2-Day"):
			dayCount+=1
		m+=1
	reportFile.write(str(patientRecords[mStart][1])+","+str(resCount)+","+str(dayCount)+","+str(statusDelaware)+",\n")
	m+=1
reportFile.close()
print "# Step 6 of 6 ... Report file generated"
