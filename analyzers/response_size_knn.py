import json
import logging

import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors.kde import KernelDensity

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

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

    log.debug("*** Printing Input to analysis - 4 (1): K-means on IP and average response size ****")

    #####*****SIZE******####
    #### Analysis #4 (1): IP address - Size of response received feature
    X = np.array([[0.00, 0.00]])

    for x in hostlist:

        avg_size = mean(per_size[x])
        log.debug(x + ": " + str(avg_size))
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

        # log.debug( str(float(float(ip)/1000)) + ": " + str(avg_size))
        le = [float(float(ip) / 1000), avg_size]

        X = np.vstack([X, le])

    log.info(
        "********    Printing Analysis #4 (2): IP-Address and Response Size received:  K-Nearest Neighbours ********")
    # print kmeans.labels_

    #################################################
    ##Analysis: 4 (2): K-Nearest Neighbours######
    nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
    distances, indices = nbrs.kneighbors(X)

    log.info("Graph and neighbours:")
    # log.info( nbrs.kneighbors_graph(X))

    log.info(nbrs.kneighbors_graph(X).toarray())

    kde = KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
    log.info("Printing KDE:")
    log.info(kde.score_samples(X))


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
