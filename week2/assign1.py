import sys


#open the file with distances and initialize the matrix of distances
f = open('clustering1.txt', 'r')
graf = [[sys.maxsize]*0 for x in range(0)]

line_no = 0
num_nodes = 0
num_edges = 0
edges = []
evert = []
svert = []
graf = [[0]*0 for x in range(0)]
max_distance=0

for line in f:
	if (line_no==0):
		#read the number of nodes from the first line
		pair = line.strip().split()
		num_nodes = int(int(pair[0]))	
		
		#initialize the distance matrix, by setting elements on the diagonal to 0 and all other to MAX LOG INT
		graf = [[sys.maxsize]*num_nodes for x in range(num_nodes)]
		for ind in range(0,num_nodes):
			graf[ind][ind]=0
			
	else:
		#from every line 
		items = line.strip().split()
		v1 = int(items[0])
		v2 = int(items[1])
		edge_cost  = int(items[2])
		graf[v1-1][v2-1] = edge_cost
		graf[v2-1][v1-1] = edge_cost
		num_edges+=1
		max_distance=max(max_distance,edge_cost)
		
	line_no = line_no+1	


print 'num nodes and edges %d and %d' % (num_nodes, num_edges)
f.close()

#order by edge cost in increasing order
#while there are no K=4 cluster, join the closest pair ofclusters

clusts = {}
for ind in range(0,num_nodes):
	clusts[ind]=set()
	clusts[ind].add(ind)
	
while (len(clusts)>4):
	#look for the closest pair of clusters and merge them
	min_dist=max_distance+1
	curr_first=-1
	curr_second=-1
	for first_key in clusts.keys():
		for second_key in clusts.keys():	
			if (first_key!=second_key):
				#for two clusters i.e. keys, determine the distance between the two
				cluster_pair_dist=graf[first_key][second_key]
				#if it is smaller than the minimum recorded distance then record that
				if (cluster_pair_dist<min_dist):
					min_dist=cluster_pair_dist
					curr_first=first_key
					curr_second=second_key
					
	#merge curr_first and curr_second and remove curr_second
	#also update the graf matrix by updating the distance between curr_first and all other clusters
	for key in clusts.keys():
		if (key!=curr_first and key!=curr_second):
			graf[key][curr_first]=min(graf[key][curr_first],graf[key][curr_second])
			graf[curr_first][key]=min(graf[key][curr_first],graf[key][curr_second])
		
	for elem in clusts[curr_second]:
		clusts[curr_first].add(elem)
		
	del clusts[curr_second]
	
			
print 'Remaining number of clusters is %d'%(len(clusts))

for ind in clusts.keys():
	print 'Cluster %s has %d elements'%(ind,len(clusts[ind]))

for key1 in clusts.keys():
	for key2 in clusts.keys():
		print '  (%d,%d)-%d'%(key1,key2,graf[key1][key2])
	print '\n'
	
				


	
