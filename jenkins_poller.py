#!/usr/bin/python 
import requests

def pollUrls(urlPrefix):
	status = {"building": [], "lastResult": []}
	for url in urlPrefix:
		buildingResponse = requests.get(url + "/lastBuild/api/json").json()
		status["building"].append(buildingResponse["building"])

		resultResponse = requests.get(url + "/lastCompletedBuild/api/json").json()
		status["lastResult"].append(resultResponse["result"])
	return status;