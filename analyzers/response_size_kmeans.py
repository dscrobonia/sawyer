import json
import logging

import numpy as np
from sklearn.cluster import KMeans

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    per_size = dict()  # IP-Response size
    hostlist = dict()

    # Data pre-processing here:
    for y in json_to_python:

        hostlist[y['HOST']] = 1

        if y['HOST'] in per_size:

            per_size[y['HOST']].append(int(y['SIZE']))

        else:

            per_size[y['HOST']] = [int(y['SIZE'])]

    ##Data pre-processing ends here

    log.debug(
        "*** Printing Input to analysis - 4 (1): K-means on IP and average response size ****"
    )

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

    # Print result for size
    kmeans = KMeans(n_clusters=24, random_state=0).fit(X)

    # print "Printing result of Analysis #4: IP-address and Response size: KMeans "
    # print kmeans.labels_

    log.info(
        "********    Printing Analysis #4: IP-Address and Response Size received: KMeans   ********"
    )
    # print kmeans.labels_
    num_clust = dict()
    clust_content = dict()

    X_index = 0
    for x in kmeans.labels_:
        if x in num_clust:
            num_clust[x] += 1
            clust_content[x].append(X_index)
        else:
            num_clust[x] = 1
            clust_content[x] = [X_index]
        X_index += 1

    min_index = min(num_clust, key=num_clust.get)

    max_index = max(num_clust, key=num_clust.get)

    log.info("Cluster no. " + str(min_index) + " has the least elements: " +
             str(num_clust[min_index]))
    log.info("Check INFO.log to view its contents!")

    content_arr = clust_content[min_index]

    log.info(
        "****  Contents of the cluster with minimum number of elements!  *****"
    )

    # Prints contents of min cluster
    input_index = 0
    for y in X:
        if input_index in content_arr:
            log.info(y)
        input_index += 1

    log.info("Cluster no. " + str(max_index) + " has the maximum elements: " +
             str(num_clust[max_index]))
    log.info("Check INFO.log to view its contents!")
    log.info(
        "Check DEBUG.log to view contents of all clusters along with the main input X!"
    )

    content_arr = clust_content[max_index]

    log.info(
        "***** Contents of the cluster with maximum number of elements! *****")
    # Prints contents of max cluster
    input_index = 0
    for y in X:
        if input_index in content_arr:
            log.info(y)
        input_index += 1

    log.debug("***** Contents of all clusters! *****")
    # Prints contents of all clusters

    for k in clust_content:
        content_arr = clust_content[k]
        log.debug("***** Contents of cluster #" + str(k) + ":  *****")
        log.debug("***** This cluster has " + str(num_clust[k]) +
                  " elements!  *****")

        input_index = 0
        for y in X:
            if input_index in content_arr:
                log.debug(y)
            input_index += 1


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
