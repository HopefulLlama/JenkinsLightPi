#!/usr/bin/python 
import wiringpi2

def setLEDs(pinConfig, outputDict):
	for key in outputDict.keys():
		wiringpi2.digitalWrite(pinConfig[key], outputDict[key])

def reportStatus(output, pinConfig, pinDict):
	print output
	setLEDs(pinConfig, pinDict)
	
def reportBuild(name, statusList, pinConfig):
	if "FAILURE" in statusList:
			reportStatus(name + " is failing!", pinConfig, {"success": 0, "failure": 1})
	elif "SUCCESS" in statusList:
			reportStatus(name + " is passing!", pinConfig, {"success": 1, "failure": 0})
	else:
			reportStatus("No completion status found for " + name, pinConfig, {"success": 0, "failure": 0})			

def reportBuilding(name, statusList, pinConfig):
	if True in statusList:
			reportStatus(name + " has a running task.", pinConfig, {"running": 1})
	elif False in statusList:
			reportStatus(name + " has no running tasks.", pinConfig, {"running": 0})
	else:
			reportStatus(name + " could not find build status.", pinConfig, {"running": 0})