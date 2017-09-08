# needed imports
from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
import numpy as np


X = np.array([[066195148.002, 0],  [066195148.022, 1 ], [066195548.002, 1], 
	[066195948.002, 0], [066695948.002, 1], [066895948.002, 1],
	 [366195948.002, 0],[566195948.002,0], [566195948.002, 1], 
	 [066895948.002, 0], [066195148.002, 0], 	 [066895948.002, 1], [066195548.002, 0],
	  [366195948.002, 1],[566195948.002,1]])


plt.scatter(X[:,0], X[:,1])
#plt.show()



Z = linkage(X, 'ward')



# calculate full dendrogram
plt.figure(figsize=(25, 10))
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    leaf_rotation=90.,  # rotates the x axis labels
    leaf_font_size=8.,  # font size for the x axis labels
)
plt.show()
