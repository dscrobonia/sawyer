import json
import logging
from itertools import cycle

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

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

    log.info(
        "********    Printing Analysis #4: IP-Address and Response Size received: MEAN SHIFT algorithm   ********"
    )
    log.info("Please check the graph at test-mean-shift.png for more info!")
    # print kmeans.labels_

    ## Analysis 4 (6): MEAN SHIFT algorithm: (IP-response size) #########
    # #############################################################################
    # Generate sample data
    X1 = X

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

    log.info("number of estimated clusters : %d" % n_clusters_)

    # #############################################################################
    # Plot result
    plt.figure(1)
    plt.clf()

    colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        my_members = labels == k
        cluster_center = cluster_centers[k]
        plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
        plt.plot(
            cluster_center[0],
            cluster_center[1],
            'o',
            markerfacecolor=col,
            markeredgecolor='k',
            markersize=14)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    ##plt.show()
    plt.savefig('test-mean-shift.png')


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
