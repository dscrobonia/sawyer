import sys
from AccessLog import *
import json




#Call toJson function from AccessLog.py to convert the log file "partial-log-july.txt" to
#json format

import sys
data = toJson(sys.argv[1])


#Convert this to python data for us to be able to run ML algorithms
json_to_python = json.loads(data)


##For logging to INFO.log and DEBUG.log:
import logging
from logging.handlers import RotatingFileHandler

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


# Import re and urlparse for pre-processing
import re
import urlparse


def countnonoverlappingrematches(pattern, thestring):
    return re.subn(pattern, '', thestring)[1]


net_req_hr = dict() 

hostlist = dict()

net_req_hr_key = [] # keeps track of keys of type hr+date+month. for finding requests received per hour 



#Data pre-processing here:
for i in json_to_python:

    y = json_to_python[i]
    
    hostlist[y['HOST']] = 1

    if y['HOST'] in hostlist:
        time = y['TIME']
        hr = time.split(":")
        dt = hr[0]
        date = dt.split("/")


        net_key = str(hr[1]) + '/' + str(date[0]) + str(date[1])
        if net_key in net_req_hr_key:
            net_req_hr[net_key] += 1
        else :
            net_req_hr[net_key] = 1
            net_req_hr_key.append(net_key)


    else:
        time = y['TIME']
        hr = time.split(":")
        dt = hr[0]
        date = dt.split("/")
        

        net_key = str(hr[1]) + '/' + str(date[0]) + str(date[1])
        if net_key in net_req_hr_key:
            net_req_hr[net_key] += 1
        else :
            net_req_hr[net_key] = 1
            net_req_hr_key.append(net_key)



###Analysis 8: Per-hour requests for a particular hour and day: key of type: hr+date

logger_attack.info( "Analysis #8: \n####****** Printing net requests per hour stats at the Server with Key: Hour/DATE Value: Number of requests ******###########")
logger_attack.info("** Note that this shows data if number of requests exceed 500. For detailed info, check INFO.log")
for x in net_req_hr_key:
    if net_req_hr[x] > 500:
        logger_attack.info( x + " received :" + str(net_req_hr[x]) + " requests!!")
        if net_req_hr[x] > 750:
            logger_attack.info("ALERT! Abnormal behaviour!")
    else:
        logger_info.info(x + " received :" + str(net_req_hr[x]) + " requests!!")
    
