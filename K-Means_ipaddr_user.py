from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin

from sklearn.preprocessing import StandardScaler

def ClusterIndicesNumpy(clustNum, labels_array): #numpy 
    return np.where(labels_array == clustNum)[0]

def ClusterIndicesComp(clustNum, labels_array): #list comprehension
    return np.array([i for i, x in enumerate(labels_array) if x == clustNum])



X = np.array([[100, 1],  [010, 4], [001, 7],
                [010, 5], [001, 8], [100, 2], [010,6],[100,3], [001,9]])

kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
print kmeans.labels_

print kmeans.cluster_centers_

print "Printing 1sr cluster before"
print X[ClusterIndicesNumpy(1,kmeans.labels_)]
print "Printing X before"
print X
X = StandardScaler().fit_transform(X)
print "Printing X after"
print X

colors = np.array([x for x in 'bgrcmykbgrcmykbgrcmykbgrcmyk'])
colors = np.hstack([colors] * 20)


kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
if hasattr(KMeans, 'labels_'):
    y_pred = KMeans.labels_.astype(np.int)
else:
    y_pred = kmeans.predict(X)


print "Printing first cluster"
print X[ClusterIndicesNumpy(0,kmeans.labels_)]


print "Printing second cluster"
print X[ClusterIndicesNumpy(1,kmeans.labels_)]


print "Printing third cluster"
print X[ClusterIndicesNumpy(2,kmeans.labels_)]



plt.subplots_adjust(bottom=.05, top=.9, left=.05, right=.95)

plt.subplot(321)

print "Priting x[:0]"
print X[:, 0]
        
plt.scatter(X[:, 0], X[:, 1], color=colors[y_pred].tolist())
plt.show()










