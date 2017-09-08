import sys
from AccessLog import *
import json




#print toJson("log-jtmelton.txt")

data = toJson("partial-log-july.txt")


#data = toJson("jul_log.txt")

#print data
#with open('data-Jul.json', 'w') as outfile:
#    json.dump(data, outfile)




json_to_python = json.loads(data)


######
#print json_to_python['name']
x = json_to_python["9969"]
print x
print x['STATUS']
print len(json_to_python)
#####


per_user = dict()
per_time = dict()
per_size = dict()
per_url = dict()
per_verb = dict()
per_zone = dict()
per_hr_req = dict()

net_req_hr = dict()


req_parameters = dict()


hostlist = []
req_per_hr_key_list = []  #keeps track of keys of the type _ip+hr+date+month
req_para_key = []

net_req_hr_key = [] # keeps track of keys of type hr+date+month. for finding requests received per hour 

hostcounter = dict()
counter = 0

for i in json_to_python:
    #print i, json_to_python[i]
    y = json_to_python[i]
    print "Printing status: " + y['STATUS']
    #per_user[y['HOST']].append(y['STATUS'])
    if y['HOST'] in per_user:
        #val = per_user[y['HOST']]
        #val.append(y['STATUS'])
        per_user[y['HOST']].append(y['STATUS'])
        time = y['TIME']
        hr = time.split(":")
        dt = hr[0]
        date = dt.split("/")

        per_time[y['HOST']].append(hr[1])
        per_size[y['HOST']].append(int(y['SIZE']))

        zn = time.split("-")
        per_zone[y['HOST']].append(zn[1])


        reque = y['REQUEST']
        req = reque.split()  
        per_verb[y['HOST']].append(req[0])
        per_url[y['HOST']].append(req[1])
        #count = per_hr_req[(y['HOST'], hr[1])]
        comp_key = str(y['HOST']) + '/' + str(hr[1]) + '/' + str(date[0]) + str(date[1])
        if comp_key in per_hr_req:  
            per_hr_req[comp_key] += 1
        else:
            per_hr_req[comp_key] = 1
            req_per_hr_key_list.append(comp_key)


        net_key = str(hr[1]) + '/' + str(date[0]) + str(date[1])
        if net_key in net_req_hr_key:
            net_req_hr[net_key] += 1
        else :
            net_req_hr[net_key] = 1
            net_req_hr_key.append(net_key)


        lst = req[1].split("&")
        #print len(lst)

        par_key = str(y['HOST']) + "/" + str(date[0]) + str(date[1])

        if par_key in req_parameters:
            req_parameters[par_key].append(len(lst))
        else :
            req_parameters[par_key] = [len(lst)]
            req_para_key.append(par_key)

        #print "Print per hr req "+ per_hr_req[(y['HOST'], hr[1])]



        #per_user[y['HOST']] = val
    else:
        per_user[y['HOST']] = [y['STATUS']]
        time = y['TIME']
        hr = time.split(":")
        dt = hr[0]
        date = dt.split("/")
        per_time[y['HOST']] = [hr[1]]
        per_size[y['HOST']] = [int(y['SIZE'])]

        zn = time.split("-")
        per_zone[y['HOST']] = [zn[1]]



        reque = y['REQUEST']
        req = reque.split()  
        per_verb[y['HOST']] = [req[0]]
        per_url[y['HOST']] =  [req[1]]
        comp_key = str(y['HOST']) + '/' + str(hr[1]) + '/' + str(date[0]) + str(date[1])

        per_hr_req[comp_key] = 1
        req_per_hr_key_list.append(comp_key)



        net_key = str(hr[1]) + '/' + str(date[0]) + str(date[1])
        if net_key in net_req_hr_key:
            net_req_hr[net_key] += 1
        else :
            net_req_hr[net_key] = 1
            net_req_hr_key.append(net_key)




        lst = req[1].split("&")
        #print len(lst)

        par_key = str(y['HOST']) + "/" + str(date[0]) + str(date[1])

        if par_key in req_parameters:
            req_parameters[par_key].append(len(lst))
        else :
            req_parameters[par_key] = [len(lst)]
            req_para_key.append(par_key)


        hostlist.append(y['HOST'])
        #****Ideally use per_user[counter] = [y['STATUS']]
        #*****And mapping of counter to ip is already available
        #IMP STUFF HERE *******
        #hostcounter[counter++]= y['HOST']




print "PRINTING PER_USER: "
print per_user[hostlist[0]]
var  = per_user[hostlist[0]]
print sorted(var, reverse = True) 



import numpy as np
X = np.array([[0.00,'0']]) 

#try to print a particular index of this hostlist
print "*****PRINTING A SAMPLE HOST: " + hostlist[0]
for x in hostlist:
    #print x
    #print per_user[x]
    word_counter = {}
    for word in per_user[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    #top_3 = popular_words[:3]
    max_status = popular_words[0]
    print x + ": " + max_status
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            #print l
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]
    #print ip + ": " + max_status
    print str(float(float(ip)/1000)) + ": " + max_status
    #le = [int(ip),max_status]
    le = [float(float(ip)/1000),max_status]
    #le = [23, 45]
    X = np.vstack([X,le])



print X


##For k-proto analysis:
#from kmodes import kmodes
#from kmodes import kprototypes

#kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

#result = kproto.fit_predict(X, categorical= 1)
#print "Printing result:"
#print result
#cluster by status



























from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt

from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin

from sklearn.preprocessing import StandardScaler






###Extract most frequent hour of the day
X = np.array([[0.00,0]]) 

#try to print a particular index of this hostlist
print "*****PRINTING A SAMPLE HOST: " + hostlist[0]
print "*****PRINTING MOST FREQ TIME:****** " + hostlist[0]

for x in hostlist:
    #print x
    #print per_user[x]
    word_counter = {}
    for word in per_time[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    #top_3 = popular_words[:3]
    max_time = popular_words[0]
    print x + ": " + max_time
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            #print l
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]


    print str(float(float(ip)/1000)) + ": " + max_time
    #le = [int(ip),max_status]
    le = [float(float(ip)/1000),max_time]

    #le = [23, 45]
    X = np.vstack([X,le])



print X


kmeans = KMeans(n_clusters=24, random_state=0).fit(X)
print kmeans.labels_
#cluster by size
























##############
#####*****SIZE******####
X = np.array([[0.00,0.00]]) 
#try to print a particular index of this hostlist
print "*****PRINTING A SAMPLE HOST: " + hostlist[0]
print "*****PRINTING AVG SIZE:****** " + hostlist[0]


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

for x in hostlist:
    
    avg_size = mean(per_size[x])
    print x + ": " + str(avg_size)
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            #print l
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]


    print str(float(float(ip)/1000)) + ": " + str(avg_size)
    #le = [int(ip),max_status]
    le = [float(float(ip)/1000),avg_size]
    #print le

    #le = [23, 45]
    X = np.vstack([X,le])
    #print X


print "USE FOR MEAN SHIFT"
print X

dend = X


#Print result for size
kmeans = KMeans(n_clusters=24, random_state=0).fit(X)
print kmeans.labels_










#################################################
####K-Nearest Neighbours######

from sklearn.neighbors import NearestNeighbors
nbrs = NearestNeighbors(n_neighbors=2, algorithm='ball_tree').fit(X)
distances, indices = nbrs.kneighbors(X)

print "Printing graph and neighbours"
print nbrs.kneighbors_graph(X)

print nbrs.kneighbors_graph(X).toarray()




from sklearn.neighbors.kde import KernelDensity
kde= KernelDensity(kernel='gaussian', bandwidth=0.2).fit(X)
print "Printing KDE:"
print kde.score_samples(X)



######################################################
###outlier:######

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neighbors import LocalOutlierFactor

np.random.seed(42)

# Generate train data
#X = 0.3 * np.random.randn(100, 2)
# Generate some abnormal novel observations
#X_outliers = np.random.uniform(low=-4, high=4, size=(20, 2))
#X = np.r_[X + 2, X - 2, X_outliers]

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
#plt.xlim((-5, 5))
#plt.ylim((-5, 5))
plt.legend([a, b],
           ["normal observations",
            "abnormal observations"],
           loc="upper left")
plt.show()


















####################################
######Outlier-unsupervised-elliptic#####

import numpy as np
from sklearn.covariance import EllipticEnvelope
from sklearn.svm import OneClassSVM
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn.datasets import load_boston

# Get data
X1 = np.array([[100, 01],  [111, 10], [001, 10], [111, 11], [001, 00], [100, 11], [111,01],[100,10], [001,10]]) 

X1 = np.array([[1, 1], [10,10] , [11,1] , [1,1] , [1,1000]]) 

# Define "classifiers" to be used
classifiers = {
    "Empirical Covariance": EllipticEnvelope(support_fraction=1.,
                                             contamination=0.261),
    "Robust Covariance (Minimum Covariance Determinant)":
    EllipticEnvelope(contamination=0.261),
    "OCSVM": OneClassSVM(nu=0.261, gamma=0.05)}
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
plt.title("Outlier detection on a real data set (boston housing)")
plt.scatter(X1[:, 0], X1[:, 1], color='black')
bbox_args = dict(boxstyle="round", fc="0.8")

plt.xlim((xx1.min(), xx1.max()))
plt.ylim((yy1.min(), yy1.max()))
plt.legend((legend1_values_list[0].collections[0],
            legend1_values_list[1].collections[0],
            legend1_values_list[2].collections[0]),
           (legend1_keys_list[0], legend1_keys_list[1], legend1_keys_list[2]),
           loc="upper center",
           prop=matplotlib.font_manager.FontProperties(size=12))
plt.ylabel("accessibility to radial highways")
plt.xlabel("pupil-teacher ratio by town")



plt.show()







########


































########################****DBSCAN****########
import numpy as np

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler


# #############################################################################
# Generate sample data
centers = dend
X, labels_true = make_blobs(n_samples=750, centers=centers, cluster_std=0.4,
                            random_state=0)

X = StandardScaler().fit_transform(X)

# #############################################################################
# Compute DBSCAN
db = DBSCAN(eps=0.3, min_samples=10).fit(X)
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
labels = db.labels_

# Number of clusters in labels, ignoring noise if present.
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

print('Estimated number of clusters: %d' % n_clusters_)
print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels_true, labels))
print("Completeness: %0.3f" % metrics.completeness_score(labels_true, labels))
print("V-measure: %0.3f" % metrics.v_measure_score(labels_true, labels))
print("Adjusted Rand Index: %0.3f"
      % metrics.adjusted_rand_score(labels_true, labels))
print("Adjusted Mutual Information: %0.3f"
      % metrics.adjusted_mutual_info_score(labels_true, labels))
print("Silhouette Coefficient: %0.3f"
      % metrics.silhouette_score(X, labels))

# #############################################################################
# Plot result
import matplotlib.pyplot as plt

# Black removed and is used for noise instead.
unique_labels = set(labels)
colors = [plt.cm.Spectral(each)
          for each in np.linspace(0, 1, len(unique_labels))]
for k, col in zip(unique_labels, colors):
    if k == -1:
        # Black used for noise.
        col = [0, 0, 0, 1]

    class_member_mask = (labels == k)

    xy = X[class_member_mask & core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=14)

    xy = X[class_member_mask & ~core_samples_mask]
    plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=tuple(col),
             markeredgecolor='k', markersize=6)

plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()




##################














#####MEAN SHIFT #########
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from sklearn.datasets.samples_generator import make_blobs

# #############################################################################
# Generate sample data



import numpy as np
centers = dend

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

print("number of estimated clusters : %d" % n_clusters_)

# #############################################################################
# Plot result
import matplotlib.pyplot as plt
from itertools import cycle

plt.figure(1)
plt.clf()

colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
for k, col in zip(range(n_clusters_), colors):
    my_members = labels == k
    cluster_center = cluster_centers[k]
    plt.plot(X[my_members, 0], X[my_members, 1], col + '.')
    plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=14)
plt.title('Estimated number of clusters: %d' % n_clusters_)
plt.show()












#XXXXXXXXXXXXXXXXX
#########SINGLE AND LINKAGE HAC*****#########
#cityblock, euclidean and chebychev: metrics for distance
import numpy as np
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt

X = dend

fig, axes23 = plt.subplots(2, 3)

for method, axes in zip(['single', 'complete',], axes23):
    z = hac.linkage(X, method=method)

    # Plotting
    axes[0].plot(range(1, len(z)+1), z[::-1, 2])
    knee = np.diff(z[::-1, 2], 2)
    axes[0].plot(range(2, len(z)), knee)

    num_clust1 = knee.argmax() + 2
    knee[knee.argmax()] = 0
    num_clust2 = knee.argmax() + 2

    axes[0].text(num_clust1, z[::-1, 2][num_clust1-1], 'possible\n<- knee point')

    part1 = hac.fcluster(z, num_clust1, 'maxclust')
    part2 = hac.fcluster(z, num_clust2, 'maxclust')

    clr = ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600' ,'#0099CC' ,
    '#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00' ,'#00CC01' ,'#0055CC']

    for part, ax in zip([part1, part2], axes[1:]):
        for cluster in set(part):
            ax.scatter(X[part == cluster, 0], X[part == cluster, 1], 
                       color=clr[cluster%10])

    m = '\n(method: {})'.format(method)
    plt.setp(axes[0], title='Screeplot{}'.format(m), xlabel='partition',
             ylabel='{}\ncluster distance'.format(m))
    plt.setp(axes[1], title='{} Clusters'.format(num_clust1))
    plt.setp(axes[2], title='{} Clusters'.format(num_clust2))

plt.tight_layout()
plt.show()














fig, axes23 = plt.subplots(2, 3)

for method, axes in zip(['ward', 'average'], axes23):
    z = hac.linkage(X, method=method)

    # Plotting
    axes[0].plot(range(1, len(z)+1), z[::-1, 2])
    knee = np.diff(z[::-1, 2], 2)
    axes[0].plot(range(2, len(z)), knee)

    num_clust1 = knee.argmax() + 2
    knee[knee.argmax()] = 0
    num_clust2 = knee.argmax() + 2

    axes[0].text(num_clust1, z[::-1, 2][num_clust1-1], 'possible\n<- knee point')

    part1 = hac.fcluster(z, num_clust1, 'maxclust')
    part2 = hac.fcluster(z, num_clust2, 'maxclust')

    clr = ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600' ,'#0099CC' ,
    '#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00' ,'#00CC01' ,'#0055CC']

    for part, ax in zip([part1, part2], axes[1:]):
        for cluster in set(part):
            ax.scatter(X[part == cluster, 0], X[part == cluster, 1], 
                       color=clr[cluster%10])

    m = '\n(method: {})'.format(method)
    plt.setp(axes[0], title='Screeplot{}'.format(m), xlabel='partition',
             ylabel='{}\ncluster distance'.format(m))
    plt.setp(axes[1], title='{} Clusters'.format(num_clust1))
    plt.setp(axes[2], title='{} Clusters'.format(num_clust2))

plt.tight_layout()
plt.show()













fig, axes23 = plt.subplots(2, 3)

for method, axes in zip(['centroid','median'], axes23):
    z = hac.linkage(X, method=method)

    # Plotting
    axes[0].plot(range(1, len(z)+1), z[::-1, 2])
    knee = np.diff(z[::-1, 2], 2)
    axes[0].plot(range(2, len(z)), knee)

    num_clust1 = knee.argmax() + 2
    knee[knee.argmax()] = 0
    num_clust2 = knee.argmax() + 2

    axes[0].text(num_clust1, z[::-1, 2][num_clust1-1], 'possible\n<- knee point')

    part1 = hac.fcluster(z, num_clust1, 'maxclust')
    part2 = hac.fcluster(z, num_clust2, 'maxclust')

    clr = ['#2200CC' ,'#D9007E' ,'#FF6600' ,'#FFCC00' ,'#ACE600' ,'#0099CC' ,
    '#8900CC' ,'#FF0000' ,'#FF9900' ,'#FFFF00' ,'#00CC01' ,'#0055CC']

    for part, ax in zip([part1, part2], axes[1:]):
        for cluster in set(part):
            ax.scatter(X[part == cluster, 0], X[part == cluster, 1], 
                       color=clr[cluster%10])

    m = '\n(method: {})'.format(method)
    plt.setp(axes[0], title='Screeplot{}'.format(m), xlabel='partition',
             ylabel='{}\ncluster distance'.format(m))
    plt.setp(axes[1], title='{} Clusters'.format(num_clust1))
    plt.setp(axes[2], title='{} Clusters'.format(num_clust2))

plt.tight_layout()
plt.show()
















###########################
#

from matplotlib import pyplot as pl
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np



X= dend

pl.scatter(X[:,0], X[:,1])
#plt.show()



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
pl.show()







pl.scatter(X[:,0], X[:,1])
#plt.show()



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
pl.show()




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
pl.show()













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
pl.show()








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
pl.show()


#SIZE DONE
##############











Y = np.array([[0.00,'0']]) 
Z = np.array([[0.00,'0']]) 
#to create for time-zone or not?


#try to print a particular index of this hostlist
print "*****PRINTING VERB:*******" + hostlist[0]
for x in hostlist:
    #print x
    #print per_user[x]
    word_counter = {}
    for word in per_verb[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    #top_3 = popular_words[:3]
    popular_verb = popular_words[0]
    print x + ": " + popular_verb







    word_counter = {}
    for word in per_url[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    #top_3 = popular_words[:3]
    popular_url = popular_words[0]
    print x + ": " + popular_url


    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            #print l
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]
    #print ip + ": " + max_status
    print str(float(float(ip)/1000)) + ": " + popular_verb
    #le = [int(ip),max_status]
    le = [float(float(ip)/1000), popular_verb]
    #le = [23, 45]
    X = np.vstack([X,le])




    print str(float(float(ip)/1000)) + ": " + popular_url
    #le = [int(ip),max_status]
    le = [float(float(ip)/1000), popular_url]
    #le = [23, 45]
    Y = np.vstack([Y,le])



print "Printing VERB"
print X
print "PRINTING URL"
print Y


####do k-proto




##For k-proto analysis:
#from kmodes import kmodes
#from kmodes import kprototypes

#kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

#result = kproto.fit_predict(X, categorical= 1)
#print "Printing result for verb:"
#print result


#kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

#result = kproto.fit_predict(Y, categorical= 1)
#print "Printing result for url:"
#print result





























#Is this okay to go with for one-hot encoding?? on the basis of counter approach. Will it affect distance
#in k-means clustering?? is there need for one-hot encoding here??

#Split time
#x = sent.split(":")
#print x[1]


import numpy as np
X = np.array([[100, 01],  [111, 10], [001, 10], [111, 11], [001, 00], [100, 11], [111,01],[100,10], [001,11]]) 

l = [999,99]
np.vstack([X,l])

X = np.vstack([X,l])




#create dict {hostip: counter} if hostip exists in the dict, ignore, else add the hostip-counter pair and increment counter. one hot encode
#the value corresponding to the ip. same time put the host_ip in array so that its array index is in sync with the counter
#hostcounter = dict()
#counter = 0



#if host in hostcounter:
#   continue
#else:
#   hostcounter[host] = counter++



#Load data from hson file
#with open('data.json') as data_file:    
#    data = json.load(data_file)


#can we have more than 2 features while clustering?








###########################
for x in req_per_hr_key_list:
    print x + ": " + str(per_hr_req[x])


print "############################################ Printing per hr req #########################################"

for x in net_req_hr_key:
    print x + ": " + str(net_req_hr[x])
    





print "############ Printing req_parameters ################"

for x in req_para_key:
    for y in req_parameters[x]:
        if y > 1:
                print x + ": " + str(y)




