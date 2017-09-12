import json
import logging
from logging.handlers import RotatingFileHandler

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors.kde import KernelDensity


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    logger_info = logging.getLogger('info_logger')
    logger_info.setLevel(logging.INFO)
    handler_info = RotatingFileHandler('INFO.log', mode='w', backupCount=0)
    logger_info.addHandler(handler_info)

    logger_debug = logging.getLogger('debug_logger')
    logger_debug.setLevel(logging.INFO)
    handler_debug = RotatingFileHandler('DEBUG.log', mode='w', backupCount=0)
    logger_debug.addHandler(handler_debug)

    logger_attack = logging.getLogger('results_logger')
    logger_attack.setLevel(logging.INFO)
    handler_attack = RotatingFileHandler('ATTACK.log', mode='w', backupCount=0)
    logger_attack.addHandler(handler_attack)

    per_size = dict()  # IP-Response size
    hostlist = dict()

    # Data pre-processing here:
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
    X = np.array([[0.00, 0.00]])

    for x in hostlist:

        avg_size = mean(per_size[x])
        logger_debug.info(x + ": " + str(avg_size))
        y = x.split(".")
        ip = ""
        for z in range(4):
            l = len(y[z])
            l = 3 - l
            if (l > 0):
                zero = ""
                for t in range(3 - len(y[z])):
                    zero = zero + "0"
                y[z] = zero + y[z]

            ip = ip + y[z]

        # logger_debug.info( str(float(float(ip)/1000)) + ": " + str(avg_size))
        le = [float(float(ip) / 1000), avg_size]

        X = np.vstack([X, le])

    logger_attack.info(
        "********    Printing Analysis #4 (2): IP-Address and Response Size received:  K-Nearest Neighbours ********")
    # print kmeans.labels_

    #################################################
    ##Analysis: 4 (2): K-Nearest Neighbours######
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)

    logger_info.info("Graph and neighbours:")
    # logger_info.info( nbrs.kneighbors_graph(X))

    logger_info.info(nbrs.kneighbors_graph(X).toarray())

    kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
    logger_attack.info("Printing KDE:")
    logger_attack.info(kde.score_samples(X))


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
