import numpy as np
from kmodes import kmodes
from kmodes import kprototypes



X = np.array([[066195148.002, 'GET'],  [066195148.022, 'GET' ], [066195548.002, 'POST'],
                [066195948.002, 'GET'], [066695948.002, 'POST'], [066895948.002, 'POST'], [366195948.002, 'GET'],[566195948.002, 'GET'] ])

kproto = kprototypes.KPrototypes(n_clusters=4, init='Cao', verbose=2)

result = kproto.fit_predict(X, categorical=[1])



print "Printing result:"
print X






X = np.array([[066195148.002, 'GET'],  [066195148.022, 'POST' ], [066195548.002, 'POST'], 
	[066195948.002, 'GET'], [066695948.002, 'POST'], [066895948.002, 'POST'],
	 [366195948.002, 'GET'],[566195948.002,'GET'], [566195948.002, 'POST'], 
	 [066895948.002, 'GET'], [066195148.002, 'GET'], 	 [066895948.002, 'POST'], [066195548.002, 'GET'],
	  [366195948.002, 'POST'],[566195948.002,'POST']])





#[3 0 5 2 4 1 3 0 5 2 4 1]  #for diff of 5 goes by category
#Y  = np.array([[10, 'cat'],[20, 'cat'],[30, 'cat'],[40, 'cat'],[50, 'cat'], [10, 'dog'],[20, 'dog'],
#        [30, 'dog'], [40, 'dog'], [50, 'dog']])
#[1 2 4 3 0 1 2 4 3 0]






#[2 2 0 0 1 1 5 5 3 3 4 4]
#Y  = np.array([[10, 'cat'],[11, 'cat'],[30, 'cat'],[31, 'cat'],[50, 'cat'], [51, 'cat'], [110, 'dog'],[111, 'dog'],
#        [130, 'dog'], [132, 'dog'], [150, 'dog'], [152, 'dog']])






X = np.array([[066195148.002, 'GET'],  [066195148.022, 'POST' ], [066195548.002, 'POST'], 
	[066195948.002, 'GET'], [066695948.002, 'POST'], [066895948.002, 'POST'],
	 [366195948.002, 'GET'],[566195948.002,'GET'], [566195948.002, 'POST'], 
	 [066895948.002, 'GET'], [066195148.002, 'GET'], 	 [066895948.002, 'POST'], [066195548.002, 'GET'],
	  [366195948.002, 'POST'],[566195948.002,'POST']])







Y = n.array([[12.01, 'Fail'],[12.05, 'Fail'],[12.10, 'Fail'],[12.15, 'Fail'], [12.18, 'Pass'],
	[12.20, 'Fail'],  [21.45, 'Fail'], [21.59, 'Pass']])

#[2 2 2 2 3 2 1 0]
#Expected type of result







