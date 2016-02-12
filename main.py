#!/usr/bin/python 
import sys, sched, time, jenkins_poller, config_loader, status_checker, console_logger, pin_handler

def pollAndReportOnUrls(sc, config):
	status = jenkins_poller.pollUrls(config["urlPrefix"])
	
	# Report last completed build color
	passing = status_checker.isPassing(status["lastResult"])
	console_logger.logPassing(config["jobName"], passing)
	pin_handler.illuminatePassing(passing, config["pins"])
	
	# Report building status
	building = status_checker.isBuilding(status["building"])
	console_logger.logBuilding(config["jobName"], building)
	pin_handler.illuminateBuilding(building, config["pins"])

	# Reschedule the same job
	if sc is not None:
		sc.enter(config["frequency"], 1, pollAndReportOnUrls, (sc,))

def main():
	if len(sys.argv) == 2:
		config = config_loader.load(sys.argv[1])
		print ("Configuration loaded for " + config["jobName"] + " job.\n")
		
		pin_handler.setUpAllPins(config["pins"])

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
	print("Some sort of exception occurred. Turning off all LEDs...")
	pin_handler.setLEDs(config["pins"], {"success": 0, "failure": 0, "building": 0})