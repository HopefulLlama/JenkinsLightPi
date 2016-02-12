#!/usr/bin/python 
import sys, sched, time, wiringpi2, jenkins_poller, config_loader, reporter

def setupPin(name, pinsConfig):
	print ("Using GPIO pin:"  + str(pinsConfig[name]) + " as '" + name + "'.")
	wiringpi2.pinMode(pinsConfig[name], 1)

def pollAndReportOnUrls(sc, config):
	status = jenkins_poller.pollUrls(config["urlPrefix"])
	# Report last completed build color
	reporter.reportBuild(config["jobName"], status["lastResult"], config["pins"])
	# Report building status
	reporter.reportBuilding(config["jobName"], status["building"], config["pins"])
	# Reschedule the same job
	if sc is not None:
		sc.enter(config["frequency"], 1, pollAndReportOnUrls, (sc,))

def main():
	if len(sys.argv) == 2:
		config = config_loader.load(sys.argv[1])
		wiringpi2.wiringPiSetupGpio()
		print ("Configuration loaded for " + config["jobName"] + " job.\n")

		print ("Loading GPIO pins")
		for pin in config["pins"].keys():
			setupPin(pin, config["pins"]);

		print ("\nURLs to test for: ")
		for url in config["urlPrefix"]:
			print ("   " + url)

		print ("\nPolling at frequency of " + str(config["frequency"]) + " seconds.")
		
		print ("\nStarting job...")
		s = sched.scheduler(time.time, time.sleep)
		# Do a poll and report now, and repeat on given frequency
		pollAndReportOnUrls(None, config)
		s.enter(config["frequency"], 1, pollAndReportOnUrls, (s, config))
		s.run()	
	else:
		print ("Please provide configuration file path as parameter.")
		print ("Exiting...")

try:
	main()
except:
	config = config_loader.load(sys.argv[1])
	reporter.reportStatus("Some sort of exception occurred. Turning off all LEDs...", config["pins"], {"success": 0, "failure": 0, "running": 0})