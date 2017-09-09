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

    rep_host_url_paramnamecnt = dict()
    url_req = []
    hostlist = dict()

    #Data pre-processing here:
    for i in json_to_python:

        y = json_to_python[i]
     
        hostlist[y['HOST']] = 1

        requee = y['REQUEST']
        requ = requee.split()  
        url = requ[1]
        parsed = urlparse.urlparse(url)
        params = urlparse.parse_qsl(parsed.query)
        count = 0
        r = url.split('?')
        r[0] ####this is the url before query parameters


        key_for_par_count = y['HOST'] + " : " + r[0]
        #key_for_par_count = y['TIME'] + y['HOST'] + " : " + r[0]


        for x,y in params:

            ##Important functionality
            if key_for_par_count in rep_host_url_paramnamecnt:
                random = rep_host_url_paramnamecnt[key_for_par_count]
                if x in random:
                    random[x] +=1
                else:
                    random[x] = 1
                rep_host_url_paramnamecnt[key_for_par_count] = random

            else:
                random = dict()
                random[x] = 1
                rep_host_url_paramnamecnt[key_for_par_count] = random



    logger_info.info( "##Analysis #13:#######**** Printing count and name of parameters for host+url combination: Find missing and extra params with this: ***######## ")
    logger_attack.info("Analysis #13:#######**** Printing missing/extra parameters *******#########")


    for y in rep_host_url_paramnamecnt:
        logger_info.info( y + "--")
        tem = rep_host_url_paramnamecnt[y]
        verify = 1
        flag = 0
        for random in rep_host_url_paramnamecnt[y]:
            flag += 1
            logger_info.info(random + ": " + str(tem[random]))
            if flag == 1:
                verify = tem[random]
            if flag > 1 :
                if verify > tem[random]:
                    logger_attack.info( "Missing parameter: " + random + " for key : "+ y)
                if verify < tem[random]:
                    logger_attack.info( "Extra parameter: " + random + " for key : "+ y)