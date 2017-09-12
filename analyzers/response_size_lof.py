import json
import logging
from logging.handlers import RotatingFileHandler

import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import LocalOutlierFactor


def analyze(data):
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
        "********   Analysis #4 (3) :  IP-Address and Response Size received: LocalOutlierFactor  ********")
    # print kmeans.labels_
    logger_attack.info(
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
