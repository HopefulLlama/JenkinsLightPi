#!/usr/bin/python 
import json

def load(path):
	configFile = open(path, 'r')
	config = json.load(configFile)
	configFile.close()
	
	return config