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
    logger_info.info('Hello to info logger!')

    logger_debug = logging.getLogger('debug_logger')
    logger_debug.setLevel(logging.INFO)
    handler_debug = RotatingFileHandler('DEBUG.log', mode = 'w',  backupCount=0)
    logger_debug.addHandler(handler_debug)
    logger_debug.info('Hello to debug logger!')

    logger_attack = logging.getLogger('results_logger')
    logger_attack.setLevel(logging.INFO)
    handler_attack = RotatingFileHandler('ATTACK.log', mode = 'w',  backupCount=0)
    logger_attack.addHandler(handler_attack)
    logger_attack.info('Hello to attack logger!')

    per_400_500 = dict() #IP-responses with 4XX/5XX
    per_200_300 = dict() #IP-responses with 2XX/3XX

    hostlist = dict()

    counter = 0

    #Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]
        


        if y['HOST'] in hostlist:
            hostlist[y['HOST']] = 1
        else:
            hostlist[y['HOST']] = 1


        #Track responses starting with 4XX and 5XX for a host-IP. Similarly with 2XX and 3XX
        if y['STATUS'].startswith('4') or y['STATUS'].startswith('5'):

            if y['HOST'] in per_400_500:
                per_400_500[y['HOST']] += 1
            else:
                per_400_500[y['HOST']] = 1


        if y['STATUS'].startswith('2') or y['STATUS'].startswith('3'):

            if y['HOST'] in per_200_300:
                per_200_300[y['HOST']] += 1
            else:
                per_200_300[y['HOST']] = 1

    ## Analysis 2: (Non-ML): Ratio and number of successful and failure response codes for an IP:
    logger_info.info("Printing Analysis #2: Number of 2XX_3XX and 4XX_5XX responses per host IP:")
    for x in hostlist:
        logger_info.info( x + ":" )
        if x in per_200_300:
            logger_info.info("200_300 total: " + str(per_200_300[x]))
        if x in per_400_500:
            logger_info.info("400_500 total: " + str(per_400_500[x])) 
        if x in per_400_500 and x in per_200_300:
            logger_info.info("ratio: "+ str(float(per_200_300[x])/float(per_400_500[x])))
            if float(per_200_300[x])/float(per_400_500[x]) < 0.0099:
                logger_attack.info("May be an attack by "+ x + " as it has "+ str(per_400_500[x]) + " failed attempts but only "+ str(per_200_300[x]) +" successful attempts!")
                

        if x in per_400_500 and not x in per_200_300:
            logger_debug.info(x + " has only failed attempts!!   :" + str(per_400_500[x]))
            if per_400_500[x] > 50 : 
                logger_attack.info("May be an attack by "+ x + " as it has "+ str(per_400_500[x]) + " failed attempts.")

        if x in per_200_300 and not x in per_400_500:
            logger_debug.info(x + " has all successful attempts!!    :" + str(per_200_300[x]) )