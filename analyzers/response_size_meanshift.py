import sys
from AccessLog import *
import json

import numpy as np


from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin

from sklearn.preprocessing import StandardScaler




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


per_size = dict() #IP-Response size
hostlist = dict()


#Data pre-processing here:
for i in json_to_python:

    y = json_to_python[i] 
    hostlist[y['HOST']] = 1

    if y['HOST'] in per_size:
        
        per_size[y['HOST']].append(int(y['SIZE']))

    else:
        
        per_size[y['HOST']] = [int(y['SIZE'])]

 
##Data pre-processing ends here

logger_debug.info("*** Printing Input to analysis - 4 (1): K-means on IP and average response size ****")


#####*****SIZE******####
#### Analysis #4 (1): IP address - Size of response received feature
X = np.array([[0.00,0.00]]) 


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

for x in hostlist:
    
    avg_size = mean(per_size[x])
    logger_debug.info( x + ": " + str(avg_size))
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


    #logger_debug.info( str(float(float(ip)/1000)) + ": " + str(avg_size))
    le = [float(float(ip)/1000),avg_size]

    X = np.vstack([X,le])


logger_attack.info( "********    Printing Analysis #4: IP-Address and Response Size received: MEAN SHIFT algorithm   ********")
logger_attack.info("Please check the graph at test-mean-shift.png for more info!")
#print kmeans.labels_


## Analysis 4 (6): MEAN SHIFT algorithm: (IP-response size) #########
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

# #############################################################################
# Generate sample data
X1 = X

import urlparse
centers = X1

X, _ = make_blobs(n_samples=10000, centers=centers, cluster_std=0.6)

# #############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

logger_attack.info("number of estimated clusters : %d" % n_clusters_)

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
##plt.show()
plt.savefig('test-mean-shift.png')








