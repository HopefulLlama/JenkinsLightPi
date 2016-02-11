#!/usr/bin/python 

import requests, sys, json, sched, time, wiringpi2
from time import sleep

try:
	if len(sys.argv) == 2:
		configFile = open(sys.argv[1], 'r')
		config = json.load(configFile)

		wiringpi2.wiringPiSetupGpio()
		print ("Configuration loaded for " + config["jobName"] + " job.")
		print ("")

		print ("Loading GPIO pins")
		pins = config["pins"]

		def setupPin(name, pinsConfig):
			print ("Using GPIO pin:"  + str(pinsConfig[name]) + " as '" + name + "'.")
			wiringpi2.pinMode(pinsConfig[name], 1)

		for pin in pins.keys():
			setupPin(pin, pins);

		print ("")
		print ("URLs to test for: ")

		for url in config["urlPrefix"]:
			print ("   " + url)

		print ("")
		print ("Polling at frequency of " + str(config["frequency"]) + " seconds.")
		print ("")
		print ("Starting job...")

		def setLEDs(pinConfig, outputDict):
			for key in outputDict.keys():
				wiringpi2.digitalWrite(pinConfig[key], outputDict[key])

		def reportStatus(output, pinConfig, pinDict):
			print output
			setLEDs(pinConfig, pinDict)

		def pollUrls(urlPrefix):
			status = {"building": [], "lastResult": []}
			for url in urlPrefix:
				buildingResponse = requests.get(url + "/lastBuild/api/json").json()
				status["building"].append(buildingResponse["building"])

				resultResponse = requests.get(url + "/lastCompletedBuild/api/json").json()
				status["lastResult"].append(resultResponse["result"])
			return status;
			
		def reportBuild(status):
                        if "FAILURE" in status:
                                reportStatus(config["jobName"] + " is failing!", pins, {"success": 0, "failure": 1})
                        elif "SUCCESS" in status:
                                reportStatus(config["jobName"] + " is passing!", pins, {"success": 1, "failure": 0})
                        else:
                                reportStatus("No completion status found for " + config["jobName"], pins, {"success": 0, "failure": 0})			

		def reportBuilding(status):
                        if True in status:
                                reportStatus(config["jobName"] + " has a running task.", pins, {"running": 1})
                        elif False in status:
                                reportStatus(config["jobName"] + " has no running tasks.", pins, {"running": 0})
                        else:
                                reportStatus(config["jobName"] + " could not find build status.", pins, {"running": 0})


		s = sched.scheduler(time.time, time.sleep)
		def pollAndReportOnUrls(sc):
			status = pollUrls(config["urlPrefix"])
			# Report last completed build color
			reportBuild(status["lastResult"])
			# Report building status
			reportBuilding(status["building"])
			# Reschedule the same job
			if sc is not None:
				sc.enter(config["frequency"], 1, pollAndReportOnUrls, (sc,))

		# Do a poll and report now, and repeat on given frequency
		pollAndReportOnUrls(None)
		s.enter(config["frequency"], 1, pollAndReportOnUrls, (s,))
		s.run()	
	else:
		print ("Please provide configuration file path as parameter.")
		print ("Exiting...")
except:
	reportStatus("Some sort of exception occurred. Turning off all LEDs...", pins, {"success": 0, "failure": 0, "running": 0})
