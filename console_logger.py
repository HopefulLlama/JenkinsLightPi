#!/usr/bin/python 
def logPassing(jobName, passing):
	if passing:
		print(jobName + " is passing!")
	elif not passing:
		print(jobName + " is failing!")
	else:
		print(jobName + " has no completion status.")

def logBuilding(jobName, building):
	if building:
		print(jobName + " has a building task!")
	elif not building:
		print(jobName + " has no building tasks.")
	else:
		print("Job's building status could not be found for " + jobName + ".")