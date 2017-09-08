import json
import nltk

from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier

from pprint import pprint
from sklearn.model_selection import train_test_split


from sklearn.cluster import KMeans




#with open('pos_features_trained_sentences.json') as data_file:    
#    json_data = json.load(data_file)


featuresets = []



featuresets = [
({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),

({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),

({"ip_1":"1", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False),  

({"ip_1":"1", "date_diff": "0", "response_type": "0", "byte_diff":"0",

"ip_1_1":"1", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False ), 

({"ip_1":"1", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1", "date_diff_1": "0", "response_type_1": "0", "byte_diff_1":"0",
}, False),

({"ip_1":"1", "date_diff": "0", "response_type": "0", "byte_diff":"0",

"ip_1_1":"1", "date_diff_1": "0", "response_type_1": "0", "byte_diff_1":"0",
}, False), 


({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False),


({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1", "date_diff_1": "0", "response_type_1": "0", "byte_diff_1":"0",
}, False), 


({"ip_1":"1", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"0",
}, False), 


({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "0", "byte_diff":"0",

"ip_1_1":"0",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"1",
}, False), 


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"1",

"ip_1_1":"0",  "date_diff_1": "1", "response_type_1": "0", "byte_diff_1":"0",
},False),

({"ip_1":"0",  "date_diff": "1", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0",  "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False), 

({"ip_1":"1",  "date_diff": "1", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1",  "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False), 


({"ip_1":"1",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"0",
},False), 

({"ip_1":"1",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"1",
},False), 

({"ip_1":"1",  "date_diff": "0", "response_type": "1", "byte_diff":"1",

"ip_1_1":"1",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"0",
},False), 

({"ip_1":"1",  "date_diff": "0", "response_type": "1", "byte_diff":"1",

"ip_1_1":"1",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"1",
},False), 

({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"1",  "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"0",
}, False), 


({"ip_1":"0",  "date_diff": "0", "response_type": "0", "byte_diff":"0",

"ip_1_1":"1",  "date_diff_1": "1", "response_type_1": "0", "byte_diff_1":"0",
},False),

({"ip_1":"0",  "date_diff": "0", "response_type": "0", "byte_diff":"0",

"ip_1_1":"0",  "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
},False),  


({"ip_1":"0",  "date_diff": "0", "response_type": "0", "byte_diff":"1",

"ip_1_1":"0",  "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
},False), 

({"ip_1":"0",  "date_diff": "0", "response_type": "0", "byte_diff":"1",

"ip_1_1":"0",  "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"1",
},False), 

({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0",  "date_diff_1": "0", "response_type_1": "0", "byte_diff_1":"0",
},False),


({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"1",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, False),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"1",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"1",
}, False),

({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"1",
}, False),


({"ip_1":"0",  "date_diff": "1", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "1", "response_type_1": "1", "byte_diff_1":"0",
}, False),


({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),

({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),

({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),

({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),

({"ip_1":"0", "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True),


({"ip_1":"0",  "date_diff": "0", "response_type": "1", "byte_diff":"0",

"ip_1_1":"0", "date_diff_1": "0", "response_type_1": "1", "byte_diff_1":"0",
}, True)

]


train_data,test_data = train_test_split(featuresets, test_size=0.20, train_size=0.80)


classifier = nltk.NaiveBayesClassifier.train(train_data)

print "Printing accuracy with Naive Bayes:"
print nltk.classify.accuracy(classifier, test_data)

print "Showing most informative features with Naive Bayes:"

print classifier.show_most_informative_features()

classifier = nltk.DecisionTreeClassifier.train(train_data)


print "Printing accuracy with Decision Tree:"

print nltk.classify.accuracy(classifier, test_data)


print "Printing pseudo code for depth 4:"
print(classifier.pseudocode(depth=4))


km = KMeans(n_clusters=2)
#km.fit(featuresets)

words = ['apple', 'Doppler', 'applaud', 'append', 'barker', 
         'baker', 'bismark', 'park', 'stake', 'steak', 'teak', 'sleek']

dist = [distance.edit_distance(words[i], words[j]) 
        for i in range(1, len(words))
        for j in range(0, i)]

labels, error, nfound = PC.kmedoids(dist, nclusters=3)
cluster = dict()
for word, label in zip(words, labels):
    cluster.setdefault(label, []).append(word)
for label, grp in cluster.items():
    print(grp)
