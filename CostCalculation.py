#!/usr/bin/python
import json
import urllib2
from pprint import pprint
import locale

def CostCalulation(hoursRunning,costPerHour):
    runningCost = (hoursRunning * float(costPerHour))
    return runningCost
  
#def main ():
#  CostCalulation(4198,0.091)
##   getCostPerHour("us-east","linux","m1.large")
#if __name__ == "__main__":
#    main()
