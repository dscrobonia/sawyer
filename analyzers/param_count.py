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


    req_parameters = dict()

    hostlist = dict()
    req_para_key = []

    #Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]
        
        hostlist[y['HOST']] = 1


        if y['HOST'] in hostlist:
            

            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")

            par_key = str(y['HOST']) + "/" + str(date[0]) + str(date[1])


            reque = y['REQUEST']
            req = reque.split()  
            lst = req[1].split("&")

            if par_key in req_parameters:
                req_parameters[par_key].append(len(lst))
            else :
                req_parameters[par_key] = [len(lst)]
                req_para_key.append(par_key)

        else:
            time = y['TIME']
            hr = time.split(":")
            dt = hr[0]
            date = dt.split("/")
            

            par_key = str(y['HOST']) + "/" + str(date[0]) + str(date[1])

            reque = y['REQUEST']
            req = reque.split()  
            lst = req[1].split("&")

            if par_key in req_parameters:
                req_parameters[par_key].append(len(lst))
            else :
                req_parameters[par_key] = [len(lst)]
                req_para_key.append(par_key)

    ###Analysis 9: List of number of parameters requested by a Host-IP on a given day for urls it requests
    ##Every entry in the list corresponds to number of parameters requested for 1 url

    logger_attack.info( "Analysis #9:\n####****** Printing List of number of parameters requested by a Host-IP on a given day for urls.  *****#####")
    logger_info.info( "Analysis #9:\n####****** Printing List of number of parameters requested by a Host-IP on a given day for urls *****####")
    logger_attack.info("Every entry in the list corresponds to number of parameters requested for 1 url, if the count exceeds 5. \nCheck INFO.log for entries with less number of parameter requests")
    for x in req_para_key:
        for y in req_parameters[x]:
            if y > 5:
                    logger_attack.info( x + ": " + str(y))
            else:
                    logger_info.info( x + ": " + str(y))


    logger_attack.info( "Check INFO.log for more details!")

def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]
