#do pip install statistics

l = [15, 18, 2, 36, 12, 78, 5, 6, 9]
print reduce(lambda x, y: x + y, l) / len(l)

import statistics

items = [1, 2, 3, 6, 8]

statistics.median(items)
#>>> 3

print statistics.median(map(float, items))


#prints top 3
print sorted(l, reverse=True)[:3]

score = [350, 914, 569, 223, 947, 284, 567, 333, 697, 245, 227, 785, 120, 794, 343, 773, 293, 995]
##name = [Ryan, Stacy, Jenna, Peter, Sophie, Bryan, Cole, Andrea, Emily, Blake, Mike, Stephan, Rob, Eliza, Heather, Daniel, Elisabeth, Samantha]

#sorted(zip(score, name), reverse=True)[:3]
#So you understand what is going on:
#zip: takes iterables as it's arguments and takes one element from each iterable, placing them in a tuple.

# zip(score, name)
#[(350, 'Ryan'), (914, 'Stacy'), (569, 'Jenna'), (223, 'Peter'), (947, 'Sophie'), (284, 'Bryan'), (567, 'Cole'), (333, 'Andrea'), (697, 'Emily'), (245, 'Blake'), (22
##print sorted(zip(score, name), reverse=True)[:3]

json_data={"id":"XXXX", "name": "xyz", "user" : { "id": "XXXX", "username":"XYZ", "group":{"id": "XXXX"}}}
import json
data = json.dumps(json_data)
json_to_python = json.loads(data)
print json_to_python['name']
x = json_to_python['user']
print x
print x['username']
len(json_to_python)  #gives length of the dictionary object


sent = "GET /feed/ HTTP/1.1"
sent.split()
x = sent.split()
x[0] #http verb


sent.split(".")

#for client id
sent = "123.543.14.1"
sent.split(".")

#for date or hour
sent = "01/Aug/2017:10:31:35"
sent.split(":")
x = sent.split(":")
print x[1]
#extract hour


a = "100"
int(a) #convert to integer


word_list = ['Jellicle', 'Cats', 'are', 'black', 'and', 'white', 'Jellicle', 'Cats', 'are', 'rather', 'small;', 'Jellicle', 'Cats', 'are', 'merry', 'and', 'bright,', 'And', 'pleasant', 'to', 'hear', 'when', 'they', 'caterwaul.', 'Jellicle', 'Cats', 'have', 'cheerful', 'faces,', 'Jellicle', 'Cats', 'have', 'bright', 'black', 'eyes;', 'They', 'like', 'to', 'practise', 'their', 'airs', 'and', 'graces', 'And', 'wait', 'for', 'the', 'Jellicle', 'Moon', 'to', 'rise.', '']
word_counter = {}
for word in word_list:
     if word in word_counter:
         word_counter[word] += 1
     else:
         word_counter[word] = 1
 
popular_words = sorted(word_counter, key = word_counter.get, reverse = True)
top_3 = popular_words[:3]

print top_3


#"9969": {"STATUS": "302", "REQUEST": "GET /feed/ HTTP/1.1", "HOST": "35.189.215.158", "REFERER": "-", "USER": "-", "TIME": "01/Aug/2017:10:31:35 -0600", "USERAGENT": "Go-http-client/1.1", "IDENTITY": "-", "SIZE": "348"}

json_data= {"9969": {"STATUS": "302", "REQUEST": "GET /feed/ HTTP/1.1", "HOST": "35.189.215.158", "REFERER": "-", "USER": "-", "TIME": "01/Aug/2017:10:31:35 -0600", "USERAGENT": "Go-http-client/1.1", "IDENTITY": "-", "SIZE": "348"},
"9541": {"STATUS": "200", "REQUEST": "GET /wp-content/plugins/syntaxhighlighter/syntaxhighlighter3/scripts/shBrushDiff.js?ver=3.0.9b HTTP/1.1", "HOST": "66.195.148.2", "REFERER": "http://www.jtmelton.com/2010/09/21/preventing-log-forging-in-java/", "USER": "-", "TIME": "01/Aug/2017:09:46:41 -0600", "USERAGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "IDENTITY": "-", "SIZE": "850"},
"9542": {"STATUS": "404", "REQUEST": "GET /wp-content/plugins/syntaxhighlighter/syntaxhighlighter3/scripts/shBrushDiff.js?ver=3.0.9b HTTP/1.1", "HOST": "66.195.148.2", "REFERER": "http://www.jtmelton.com/2010/09/21/preventing-log-forging-in-java/", "USER": "-", "TIME": "01/Aug/2017:09:46:41 -0600", "USERAGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36", "IDENTITY": "-", "SIZE": "850"}

}

import json
data = json.dumps(json_data)
json_to_python = json.loads(data)
#print json_to_python['name']
x = json_to_python["9969"]
print x
print x['STATUS']
print len(json_to_python)

#for x in range(0, int(len(json_to_python))
#	y = json_to_python.keys(x)
#	print y

from collections import defaultdict
#per_user = defaultdict(list)
per_user = dict()

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
    	#per_user[y['HOST']] = val
    else:
    	per_user[y['HOST']] = [y['STATUS']]
    	hostlist.append(y['HOST'])
    	#****Ideally use per_user[counter] = [y['STATUS']]
    	#*****And mapping of counter to ip is already available
    	#IMP STUFF HERE *******
    	hostcounter[counter++]= y['HOST']


print "PRINTING PER_USER: "
print per_user["66.195.148.2"]
var  = per_user["66.195.148.2"]
print sorted(var, reverse = True) 

#try to print a particular index of this hostlist
print "*****PRINTING A SAMPLE HOST: " + hostlist[0]


#Is this okay to go with for one-hot encoding?? on the basis of counter approach. Will it affect distance
#in k-means clustering?? is there need for one-hot encoding here??





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
#	continue
#else:
#	hostcounter[host] = counter++


