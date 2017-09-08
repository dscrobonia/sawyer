import sys
from AccessLog import *
import json



data = toJson("log-jtmelton.txt")
#data = toJson("july-log.txt")
#print data
#with open('data-Jul.json', 'w') as outfile:
#    json.dump(data, outfile)



json_to_python = json.loads(data)




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
    y = json_to_python[i]
    if y['HOST'] in per_user:
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
        




##Cluster here:
##Analysis 1: IP address and Response Status Cluster
import numpy as np
X = np.array([[0,'0']]) 



for x in hostlist:


    word_counter = {}
    for word in per_user[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)

    max_status = popular_words[0]
    #print x + ": " + max_status
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):

            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]

    #print str(float(float(ip)/1000)) + ": " + max_status

    le = [float(float(ip)/1000),max_status]

    X = np.vstack([X,le])


print "Printing IP: Status code"
print X


##For k-proto analysis:
from kmodes import kmodes
from kmodes import kprototypes

#Adjust number of clusters here
kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

result = kproto.fit_predict(X, categorical= 1)
print "Printing result for 4 clusters by host-ip and status:"
print result
#cluster by status


























##Analysis 2: Cluster by most frequent hour of the day
from sklearn.cluster import KMeans
import numpy as np
from sklearn.cluster import MiniBatchKMeans, KMeans
from sklearn.metrics.pairwise import pairwise_distances_argmin
from sklearn.preprocessing import StandardScaler

###Extract most frequently used hour of the day
X = np.array([[0,'0']]) 


print "*****PRINTING MOST FREQ TIME PER USER:****** " 
for x in hostlist:
    word_counter = {}
    for word in per_time[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    max_time = popular_words[0]
    #print x + ": " + max_time
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]


    #print str(float(float(ip)/1000)) + ": " + max_time
    le = [float(float(ip)/1000),max_time]

    X = np.vstack([X,le])


print "Printing IP:hour"
print X

print "Printing k-means for host IP and most frequent hour, clusters 24"
kmeans = KMeans(n_clusters=24, random_state=0).fit(X)
print kmeans.labels_

























##############
#####*****SIZE******####
##Analysis 3: IP address and size of the response received
X = np.array([[0,'0']]) 

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

for x in hostlist:
    
    avg_size = mean(per_size[x])
    #print x + ": " + str(avg_size)
    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):
            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]


    #print str(float(float(ip)/1000)) + ": " + str(avg_size)
    le = [float(float(ip)/1000),avg_size]

    X = np.vstack([X,le])


print "Print IP addresss: Response Size"
print X


#Print result for size
kmeans = KMeans(n_clusters=10, random_state=0).fit(X)
print kmeans.labels_











###Analysis 4: Most frequently used http verb
###Analysis 5: Most frequently requested resource url


Y = np.array([[0,'0']]) 
Z = np.array([[0,'0']]) 



#Try to print a particular index of this hostlist
print "*****PRINTING VERB:*******"
for x in hostlist:
  
    word_counter = {}
    for word in per_verb[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    popular_verb = popular_words[0]
    #print x + ": " + popular_verb





    word_counter = {}
    for word in per_url[x]:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
    popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
    popular_url = popular_words[0]
    #print x + ": " + popular_url


    y = x.split(".")
    ip = ""
    for z in range(4):
        l = len(y[z])
        l = 3 - l
        if(l>0):

            zero = ""
            for t in range(3 - len(y[z])):
                zero = zero + "0"
            y[z] = zero + y[z]

        ip = ip + y[z]

    #print str(float(float(ip)/1000)) + ": " + popular_verb
    le = [float(float(ip)/1000), popular_verb]
    X = np.vstack([X,le])



    #print str(float(float(ip)/1000)) + ": " + popular_url
    le = [float(float(ip)/1000), popular_url]
    Y = np.vstack([Y,le])



print "Printing IP:VERB"
print X
print "PRINTING IP:URL"
print Y





##For k-proto analysis:
#from kmodes import kmodes
#from kmodes import kprototypes

kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

result = kproto.fit_predict(X, categorical= 1)
print "Printing result for verb:"
print result


kproto = kprototypes.KPrototypes(n_clusters=10, init='Cao', verbose=2)

result = kproto.fit_predict(Y, categorical= 1)
print "Printing result for url:"
print result

