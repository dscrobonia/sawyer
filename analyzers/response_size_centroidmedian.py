import sys
import json
import re
import urlparse
import logging
from logging.handlers import RotatingFileHandler

import matplotlib.pyplot as plt
import numpy as np

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.preprocessing import StandardScaler
import scipy.cluster.hierarchy as hac


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


    logger_attack.info( "********    Printing Analysis #4: IP-Address and Response Size received: Centroid and Median Hierarchical Clustering  ********\nCheck 'test-centroid-median.png' for more info!")
    #print kmeans.labels_

    ### Analysis 4 (9): ###### CENTROID AND MEDIAN HAC*****#########
    fig, axes23 = plt.subplots(2, 3)

    for method, axes in zip(['centroid','median'], axes23):
        z = hac.linkage(X, method=method)

        # Plotting
        axes[0].plot(range(1, len(z)+1), z[::-1, 2])
        knee = np.diff(z[::-1, 2], 2)
        axes[0].plot(range(2, len(z)), knee)

        num_clust1 = knee.argmax() + 2
        knee[knee.argmax()] = 0
        num_clust2 = knee.argmax() + 2

        axes[0].text(num_clust1, z[::-1, 2][num_clust1-1], 'possible\n<- knee point')

        part1 = hac.fcluster(z, num_clust1, 'maxclust')
        part2 = hac.fcluster(z, num_clust2, 'maxclust')

        clr = ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600' ,'#0099CC' ,
        '#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00' ,'#00CC01' ,'#0055CC']

        for part, ax in zip([part1, part2], axes[1:]):
            for cluster in set(part):
                ax.scatter(X[part == cluster, 0], X[part == cluster, 1], 
                           color=clr[cluster%10])

        m = '\n(method: {})'.format(method)
        plt.setp(axes[0], title='Screeplot{}'.format(m), xlabel='partition',
                 ylabel='{}\ncluster distance'.format(m))
        plt.setp(axes[1], title='{} Clusters'.format(num_clust1))
        plt.setp(axes[2], title='{} Clusters'.format(num_clust2))

    plt.tight_layout()
    ##plt.show()

    plt.savefig('test-centroid-median.png')


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
