#!/usr/bin/python 
def isPassing(statusList):
	if "FAILURE" in statusList:
		return False
	elif "SUCCESS" in statusList:
		return True
	else:
		return None

def isBuilding(statusList):
	if True in statusList:
		return True
	elif False in statusList:
		return False
	else:
		return None