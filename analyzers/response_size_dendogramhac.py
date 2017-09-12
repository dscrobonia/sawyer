import json
import logging
from logging.handlers import RotatingFileHandler

import matplotlib.pyplot as pl
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage


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
        "********    Printing Analysis #4: IP-Address and Response Size received: Hierarchical clustering dendograms  ********")

    ###########################
    ### Analysis 4 (10): ###### Ward linkage dendogram: *****#########

    pl.scatter(X[:, 0], X[:, 1])
    # plt.show()



    Z = linkage(X, 'ward')

    # calculate full dendrogram
    pl.figure(figsize=(25, 10))
    pl.title('Hierarchical Clustering Dendrogram: Ward linkage')
    pl.xlabel('sample index')
    pl.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    pl.savefig('test-ward-linkage.png')
    ##pl.show()

    logger_attack.info("Please check test-ward-linkage.png to view dendogram for ward linkage.")

    ### Analysis 4 (11): ###### Single linkage dendogram: *****#########

    Z = linkage(X, 'single')

    # calculate full dendrogram
    pl.figure(figsize=(25, 10))
    pl.title('Hierarchical Clustering Dendrogram: Single linkage')
    pl.xlabel('sample index')
    pl.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    ##pl.show()
    pl.savefig('test-single-linkage.png')

    logger_attack.info("Please check test-single-linkage.png to view dendogram for single linkage.")

    ### Analysis 4 (12): ###### Complete linkage dendogram: *****#########
    Z = linkage(X, 'complete')

    # calculate full dendrogram
    pl.figure(figsize=(25, 10))
    pl.title('Hierarchical Clustering Dendrogram: Complete linkage')
    pl.xlabel('sample index')
    pl.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    ##pl.show()

    pl.savefig('test-complete-linkage.png')

    logger_attack.info("Please check test-complete-linkage.png to view dendogram for complete linkage.")

    ### Analysis 4 (13): ###### Median linkage dendogram: *****#########
    Z = linkage(X, 'median')

    # calculate full dendrogram
    pl.figure(figsize=(25, 10))
    pl.title('Hierarchical Clustering Dendrogram: Median linkage')
    pl.xlabel('sample index')
    pl.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    ##pl.show()

    pl.savefig('test-median-linkage.png')

    logger_attack.info("Please check test-median-linkage.png to view dendogram for median linkage.")

    ### Analysis 4 (14): ###### Centroid linkage dendogram: *****#########



    Z = linkage(X, 'centroid')

    # calculate full dendrogram
    pl.figure(figsize=(25, 10))
    pl.title('Hierarchical Clustering Dendrogram: Centroid linkage')
    pl.xlabel('sample index')
    pl.ylabel('distance')
    dendrogram(
        Z,
        leaf_rotation=90.,  # rotates the x axis labels
        leaf_font_size=8.,  # font size for the x axis labels
    )
    ##pl.show()
    pl.savefig('test-centroid-linkage.png')

    logger_attack.info("Please check test-centroid-linkage.png to view dendogram for centroid linkage.")


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
