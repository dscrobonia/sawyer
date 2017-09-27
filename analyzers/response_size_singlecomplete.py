import json
import logging

import matplotlib.pyplot as plt
import numpy as np
import scipy.cluster.hierarchy as hac

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
        "********    Printing Analysis #4: IP-Address and Response Size received: Single and Complete Hierarchical Clustering  ********\n Check test-single-complete.png for more info!")
    # print kmeans.labels_


    ### Analysis 4 (7): ######SINGLE AND COMPLETE HAC*****#########
    # cityblock, euclidean and chebychev: metrics for distance
    fig, axes23 = plt.subplots(2, 3)

    for method, axes in zip(['single', 'complete', ], axes23):
        z = hac.linkage(X, method=method)

        # Plotting
        axes[0].plot(range(1, len(z) + 1), z[::-1, 2])
        knee = np.diff(z[::-1, 2], 2)
        axes[0].plot(range(2, len(z)), knee)

        num_clust1 = knee.argmax() + 2
        knee[knee.argmax()] = 0
        num_clust2 = knee.argmax() + 2

        axes[0].text(num_clust1, z[::-1, 2][num_clust1 - 1], 'possible\n<- knee point')

        part1 = hac.fcluster(z, num_clust1, 'maxclust')
        part2 = hac.fcluster(z, num_clust2, 'maxclust')

        clr = ['#2200CC', '#D9007E', '#FF6600', '#FFCC00', '#ACE600', '#0099CC',
               '#8900CC', '#FF0000', '#FF9900', '#FFFF00', '#00CC01', '#0055CC']

        for part, ax in zip([part1, part2], axes[1:]):
            for cluster in set(part):
                ax.scatter(X[part == cluster, 0], X[part == cluster, 1],
                           color=clr[cluster % 10])

        m = '\n(method: {})'.format(method)
        plt.setp(axes[0], title='Screeplot{}'.format(m), xlabel='partition',
                 ylabel='{}\ncluster distance'.format(m))
        plt.setp(axes[1], title='{} Clusters'.format(num_clust1))
        plt.setp(axes[2], title='{} Clusters'.format(num_clust2))

    plt.tight_layout()
    ##plt.show()
    plt.savefig('test-single-complete.png')


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)
