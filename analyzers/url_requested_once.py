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
logger_info.info( "##******** Analysis #11:###Printing INPUT for url and hosts with only one host requesting this url #####")


per_host_req_url = dict()
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

    logger_info.info(str(y['HOST']) + ": " + r[0] )
    if r[0] in per_host_req_url:
        per_host_req_url[r[0]].append(y['HOST'])
    else:
        per_host_req_url[r[0]] = [y['HOST']]




##Data pre-processing ends here



###Analysis 11: List of urls with only one host requesting it

logger_attack.info( "##******** Analysis #11:###Printing url and hosts with only one host requesting this url #####")

host_unique_url_count = dict()

for x in per_host_req_url:
    if len(per_host_req_url[x]) == 1:
        for y in per_host_req_url[x]:
            if y in host_unique_url_count:
                host_unique_url_count[y] += 1
            else:
                host_unique_url_count[y] = 1

            logger_attack.info( "URL :    "+ x +"\nis hit only by IP: "+ y)

