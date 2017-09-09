import sys
from AccessLog import *
import json

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


#Call toJson function from AccessLog.py to convert the log file "partial-log-july.txt" to
#json format

import sys
data = toJson(sys.argv[1])


#Convert this to python data for us to be able to run ML algorithms
json_to_python = json.loads(data)



# Import re and urlparse for pre-processing
import re


per_user = dict() #IP-Status

hostlist = dict()




#Data pre-processing here:
for i in json_to_python:

    y = json_to_python[i]

    hostlist[y['HOST']] = 1

    
    if y['HOST'] in per_user:    
        per_user[y['HOST']].append(y['STATUS'])
 
    else:
        per_user[y['HOST']] = [y['STATUS']]






logger_debug.info("***  Printing input contents to the algorithm: ***")

###Analysis 1 : (ML): Run K-prototypes algorithm on IP-Response_status feature-set here:
import numpy as np
X = np.array([[0.00,'0']]) 

for x in hostlist:
    word_counter = {}
    for word in per_user[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    max_status = popular_words[0]
    #print x + ": " + max_status
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]
    logger_debug.info(str(float(float(ip)/1000)) + ": " + max_status)
    le = [float(float(ip)/1000),max_status]
    X = np.vstack([X,le])



#print X
logger_attack.info( "######******* Analysis #1: K-prototype for IP address-Response status: ******#######")

##For k-proto analysis:
from kmodes import kmodes
from kmodes import kprototypes


##Adjust number of clusters here
kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

result = kproto.fit_predict(X, categorical= 1)

#print result
#cluster by status


num_clust = dict()
clust_content = dict()


X_index = 0
for x in result:
    if x in num_clust:
        num_clust[x] += 1
        clust_content[x].append(X_index)
    else:
        num_clust[x] = 1
        clust_content[x] = [X_index]
    X_index += 1




min_index = min(num_clust, key=num_clust.get)

max_index = max(num_clust, key=num_clust.get)

logger_attack.info("Cluster no. " +str(min_index) + " has the least elements: "+ str(num_clust[min_index]))
logger_attack.info("Check INFO.log to view its contents!")


content_arr = clust_content[min_index]

logger_info.info("****  Contents of the cluster with minimum number of elements!  *****")

#Prints contents of min cluster
input_index = 0
for y in X:
    if input_index in content_arr:
        logger_info.info(y)
    input_index += 1


logger_attack.info("Cluster no. "+ str(max_index) + " has the maximum elements: "+ str(num_clust[max_index]))
logger_attack.info("Check INFO.log to view its contents!")
logger_attack.info("Check DEBUG.log to view contents of all clusters along with the main input X!")


content_arr = clust_content[max_index]

logger_info.info("***** Contents of the cluster with maximum number of elements! *****")
#Prints contents of max cluster
input_index = 0
for y in X:
    if input_index in content_arr:
        logger_info.info(y)
    input_index += 1






logger_debug.info("***** Contents of all clusters! *****")
#Prints contents of all clusters


for k in clust_content:
    content_arr = clust_content[k]
    logger_debug.info("***** Contents of cluster #"+ str(k) +":  *****")
    logger_debug.info("***** This cluster has "+ str(num_clust[k]) +" elements!  *****")


    input_index = 0
    for y in X:
        if input_index in content_arr:
            logger_debug.info(y)
        input_index += 1


