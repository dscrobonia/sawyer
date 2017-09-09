import sys
import json
import re
import urlparse
import logging
from logging.handlers import RotatingFileHandler

import matplotlib.pyplot as plt
import numpy as np

def analyze(data):
    #Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    logger_info = logging.getLogger('info_logger')
    logger_info.setLevel(logging.INFO)
    handler_info = RotatingFileHandler('INFO.log', mode = 'w',   backupCount=0)
    logger_info.addHandler(handler_info)

    logger_debug = logging.getLogger('debug_logger')
    logger_debug.setLevel(logging.INFO)
    handler_debug = RotatingFileHandler('DEBUG.log', mode = 'w',  backupCount=0)
    logger_debug.addHandler(handler_debug)

    logger_attack = logging.getLogger('results_logger')
    logger_attack.setLevel(logging.INFO)
    handler_attack = RotatingFileHandler('ATTACK.log', mode = 'w',  backupCount=0)
    logger_attack.addHandler(handler_attack)

    hostlist = dict()
    req_per_hr_key_list = []  #keeps track of keys of the type ip+hour+date+month
    per_hr_req = dict() #IP-req-per-hour


    #Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]

        hostlist[y['HOST']] = 1

        if y['HOST'] in hostlist:
            

            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            comp_key = str(y['HOST']) + '/' + str(hr[1]) + '/' + str(date[0]) + str(date[1])
            if comp_key in per_hr_req:  
                per_hr_req[comp_key] += 1
            else:
                per_hr_req[comp_key] = 1
                req_per_hr_key_list.append(comp_key)


        else:
            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")
            
            comp_key = str(y['HOST']) + '/' + str(hr[1]) + '/' + str(date[0]) + str(date[1])

            per_hr_req[comp_key] = 1
            req_per_hr_key_list.append(comp_key)


    ###########################****NON-ML Analysis here******################
    ###Analysis 7: Per-hour requests for a host at a particular hour and day: key of type: host+hr+date
    logger_attack.info( "Analysis #7: ####****** Printing per hour request stats for a given combination of : HOST/HOUR/DATE: ******###########")
    logger_attack.info( "** Detects only in case th host makes more than 250 requests in 1 hour. For more detailed info, see INFO.log")

    logger_info.info( "Analysis #7: ####****** Printing per hour request stats for a given combination of : HOST/HOUR/DATE: ******###########")

    for x in req_per_hr_key_list:
        if per_hr_req[x] > 250:
            logger_attack.info( x + ": " + str(per_hr_req[x]))
        else:
            logger_info.info( x + ": " + str(per_hr_req[x]))





