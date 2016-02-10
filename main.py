#!/usr/bin/python 

import requests, sys, json, sched, time, wiringpi2
from time import sleep

try:
	if len(sys.argv) == 2:
		configFile = open(sys.argv[1], 'r')
		config = json.load(configFile)

		wiringpi2.wiringPiSetupGpio()
		print ("Configuration loaded for " + config.get("jobName") + " job.")
		print ("")

		print ("Loading GPIO pins")
		pins = config.get("pins")
		print ("Using GPIO pin: " + str(pins.get("success")) + " as 'success'.")
		wiringpi2.pinMode(pins.get("success"), 1)
		print ("Using GPIO pin: " + str(pins.get("running")) + " as 'running'.")
		wiringpi2.pinMode(pins.get("running"), 1)
		print ("Using GPIO pin: " + str(pins.get("failure")) + " as 'failure'.")
		wiringpi2.pinMode(pins.get("failure"), 1)

		print ("URLs to test for: ")

		for url in config.get("urlPrefix"):
			print ("   " + url)

		print ("")
		print ("Polling at frequency of " + str(config.get("frequency")) + " seconds.")

		print ("Starting job...")

		s = sched.scheduler(time.time, time.sleep)
		def pollAndReportOnUrls(sc):
			lastBuildsBuilding = []
			lastCompletedBuildsStatus = []
			for url in config.get("urlPrefix"):
				lastBuildsResponse = requests.get(url + "/lastBuild/api/json").json()
				lastBuildsBuilding.append(lastBuildsResponse.get("building"))

				lastCompletedBuildsResponse = requests.get(url + "/lastCompletedBuild/api/json").json()
				lastCompletedBuildsStatus.append(lastCompletedBuildsResponse.get("result"))

			# Get last completed build color
			if "FAILURE" in lastCompletedBuildsStatus:
				print (config.get("jobName") + " is failing!")
				wiringpi2.digitalWrite(pins.get("failure"), 1)
				wiringpi2.digitalWrite(pins.get("success"), 0)
			elif "SUCCESS" in lastCompletedBuildsStatus:
				print (config.get("jobName") + " is passing!")
                	        wiringpi2.digitalWrite(pins.get("failure"), 0)
                        	wiringpi2.digitalWrite(pins.get("success"), 1)
			else:
				print("No completion status found for " + config.get("jobName"))
				wiringpi2.digitalWrite(pins.get("failure"), 0)
				wiringpi2.digitalWrite(pins.get("success"), 0)

			# Get building status
			if True in lastBuildsBuilding: 
				print (config.get("jobName") + " has a running task.")
				wiringpi2.digitalWrite(pins.get("running"), 1)
			elif False in lastBuildsBuilding:
				print (config.get("jobName") + " has no running tasks.")
				wiringpi2.digitalWrite(pins.get("running"), 0)
			else:
				print (config.get("jobName") + " could not find build status.")
				wiringpi2.digitalWrite(pins.get("running"), 0)

			# Reschedule the same job
			if sc is not None:
				sc.enter(config.get("frequency"), 1, pollAndReportOnUrls, (sc,))

		pollAndReportOnUrls(None)
		s.enter(config.get("frequency"), 1, pollAndReportOnUrls, (s,))
		s.run()	
	else:
		print ("Please provide configuration file path as parameter.")
		print ("Exiting...")
except:
	print ("Some sort of exception occurred.")
	wiringpi2.digitalWrite(pins.get("running"), 0)
	wiringpi2.digitalWrite(pins.get("failure"), 0)
	wiringpi2.digitalWrite(pins.get("success"), 0)
