import json
import logging

import matplotlib.pyplot as plt
import numpy as np
from sklearn import metrics
from sklearn.cluster import DBSCAN
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    # Data pre-processing here:
    per_size = dict()  # IP-Response size
    hostlist = dict()

    for y in json_to_python:

        hostlist[y['HOST']] = 1

        if y['HOST'] in per_size:

            per_size[y['HOST']].append(int(y['SIZE']))

        else:

            per_size[y['HOST']] = [int(y['SIZE'])]

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
        "********    Printing Analysis #4: IP-Address and Response Size received: DBSCAN  ********"
    )
    log.info("Check the image test-dbscan.png for more info!")
    # print kmeans.labels_
    X1 = X

    # #############################################################################
    # Generate sample data
    centers = X1
    X, labels_true = make_blobs(
        n_samples=750, centers=centers, cluster_std=0.4, random_state=0)

    X = StandardScaler().fit_transform(X)

    # #############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=0.3, min_samples=10).fit(X)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    log.info('Estimated number of clusters: %d' % n_clusters_)
    log.info(
        "Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
    log.info("Completeness: %0.3f" % metrics.completeness_score(
        labels_true, labels))
    log.info("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
    log.info("Adjusted Rand Index: %0.3f" % metrics.adjusted_rand_score(
        labels_true, labels))
    log.info("Adjusted Mutual Information: %0.3f" %
             metrics.adjusted_mutual_info_score(labels_true, labels))
    log.info(
        "Silhouette Coefficient: %0.3f" % metrics.silhouette_score(X, labels))

    # #############################################################################
    # Plot result

    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [
        plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))
    ]
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_member_mask = (labels == k)

        xy = X[class_member_mask & core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            'o',
            markerfacecolor=tuple(col),
            markeredgecolor='k',
            markersize=14)

        xy = X[class_member_mask & ~core_samples_mask]
        plt.plot(
            xy[:, 0],
            xy[:, 1],
            'o',
            markerfacecolor=tuple(col),
            markeredgecolor='k',
            markersize=6)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    ##plt.show()
    plt.savefig('test-dbscan.png')


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
