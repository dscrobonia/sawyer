import json
import logging

import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import LocalOutlierFactor

log = logging.getLogger(__name__)


def analyze(data):
    # Convert this to python data for us to be able to run ML algorithms
    json_to_python = json.loads(data)

    # Data pre-processing here:
    per_size = dict()  # IP-Response size
    hostlist = dict()

    for i in json_to_python:

        y = json_to_python[i]
        hostlist[y['HOST']] = 1

        if y['HOST'] in per_size:

            per_size[y['HOST']].append(int(y['SIZE']))

        else:

            per_size[y['HOST']] = [int(y['SIZE'])]

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
        "********   Analysis #4 (3) :  IP-Address and Response Size received: LocalOutlierFactor  ********")
    # print kmeans.labels_
    log.info(
        "******** Please check the image test-save-outlier-LOF.png saved in your working directory for more info. ********")

    ######################################################
    ##Analysis : 4 (3): Outlier detection: 
    np.random.seed(42)

    # fit the model
    clf = LocalOutlierFactor(n_neighbors=20)

    y_pred = clf.fit_predict(X)
    y_pred_outliers = y_pred[200:]

    # plot the level sets of the decision function
    xx, yy = np.meshgrid(np.linspace(-5, 5, 50), np.linspace(-5, 5, 50))
    Z = clf._decision_function(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.title("Local Outlier Factor (LOF)")
    plt.contourf(xx, yy, Z, cmap=plt.cm.Blues_r)

    a = plt.scatter(X[:200, 0], X[:200, 1], c='white',
                    edgecolor='k', s=20)
    b = plt.scatter(X[200:, 0], X[200:, 1], c='red',
                    edgecolor='k', s=20)
    plt.axis('tight')
    # plt.xlim((-5, 5))
    # plt.ylim((-5, 5))
    plt.legend([a, b],
               ["normal observations",
                "abnormal observations"],
               loc="upper left")
    ##plt.show()
    plt.savefig('test-save-outlier-LOF.png')


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
