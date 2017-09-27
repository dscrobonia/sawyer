import json
import logging

import matplotlib.font_manager
import matplotlib.pyplot as plt
import numpy as np
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM

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
        "********    Printing Analysis #4: IP-Address and Response Size received: Elliptic Envelope   ********"
    )
    log.info(
        "********    Check the image elliptic.png saved in the working directory   ********"
    )

    # print kmeans.labels_

    ####################################
    ## Analysis 4 (4): Outlier-unsupervised-elliptic (Currently not working our data)#####
    X1 = X

    # Define "classifiers" to be used
    classifiers = {
        "Empirical Covariance":
        EllipticEnvelope(support_fraction=1., contamination=0.261),
        "Robust Covariance (Minimum Covariance Determinant)":
        EllipticEnvelope(contamination=0.261),
        "OCSVM":
        OneClassSVM(nu=0.261, gamma=0.05)
    }
    colors = ['m', 'g', 'b']
    legend1 = {}
    legend2 = {}

    # Learn a frontier for outlier detection with several classifiers
    xx1, yy1 = np.meshgrid(np.linspace(-8, 28, 500), np.linspace(3, 40, 500))
    xx2, yy2 = np.meshgrid(np.linspace(3, 10, 500), np.linspace(-5, 45, 500))
    for i, (clf_name, clf) in enumerate(classifiers.items()):
        plt.figure(1)
        clf.fit(X1)
        Z1 = clf.decision_function(np.c_[xx1.ravel(), yy1.ravel()])
        Z1 = Z1.reshape(xx1.shape)
        legend1[clf_name] = plt.contour(
            xx1, yy1, Z1, levels=[0], linewidths=2, colors=colors[i])

    legend1_values_list = list(legend1.values())
    legend1_keys_list = list(legend1.keys())

    # Plot the results (= shape of the data points cloud)
    plt.figure(1)  # two clusters
    plt.title(
        "Outlier detection on a real data set: IP-response size received:")
    plt.scatter(X1[:, 0], X1[:, 1], color='black')
    bbox_args = dict(boxstyle="round", fc="0.8")

    plt.xlim((xx1.min(), xx1.max()))
    plt.ylim((yy1.min(), yy1.max()))
    plt.legend(
        (legend1_values_list[0].collections[0],
         legend1_values_list[1].collections[0],
         legend1_values_list[2].collections[0]),
        (legend1_keys_list[0], legend1_keys_list[1], legend1_keys_list[2]),
        loc="upper center",
        prop=matplotlib.font_manager.FontProperties(size=12))
    plt.ylabel("Response size received")
    plt.xlabel("Host-IP address")

    ##plt.show()
    plt.savefig('elliptic.png')


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
