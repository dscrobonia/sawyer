import sys
from AccessLog import *
import json




#print toJson("log-jtmelton.txt")
data = toJson("partial-log-july.txt")
print data
with open('data-Jul.json', 'w') as outfile:
    json.dump(data, outfile)



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




hostlist = []

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
        per_time[y['HOST']].append(hr[1])
        per_size[y['HOST']].append(int(y['SIZE']))

        zn = time.split("-")
        per_zone[y['HOST']].append(zn[1])


        reque = y['REQUEST']
        req = reque.split()  
        per_verb[y['HOST']].append(req[0])
        per_url[y['HOST']].append(req[1])





        #per_user[y['HOST']] = val
    else:
        per_user[y['HOST']] = [y['STATUS']]
        time = y['TIME']
        hr = time.split(":")
        per_time[y['HOST']] = [hr[1]]
        per_size[y['HOST']] = [int(y['SIZE'])]

        zn = time.split("-")
        per_zone[y['HOST']] = [zn[1]]



        reque = y['REQUEST']
        req = reque.split()  
        per_verb[y['HOST']] = [req[0]]
        per_url[y['HOST']] =  [req[1]]




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
X = np.array([[0,'0']]) 

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
X = np.array([[0,'0']]) 

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
X = np.array([[0,'0']]) 
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

    #le = [23, 45]
    X = np.vstack([X,le])



print X

dend = X


#Print result for size
kmeans = KMeans(n_clusters=24, random_state=0).fit(X)
print kmeans.labels_



#XXXXXXXXXXXXXXXXX
#########SINGLE AND LINKAGE HAC*****#########
#cityblock, euclidean and chebychev: metrics for distance
import numpy as np
import scipy.cluster.hierarchy as hac
import matplotlib.pyplot as plt



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











Y = np.array([[0,'0']]) 
Z = np.array([[0,'0']]) 
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


    
