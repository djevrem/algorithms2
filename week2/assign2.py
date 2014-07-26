import sys
import time

def make_set(elements, leaders, groups):

	group = set(elements)
	groups[elements[0]] = group
	for i in group:
		leaders[i] = elements[0]


def union(element1, element2, leaders, groups):

	leader1=leaders[element1]
	leader2=leaders[element2]
	
	if leader1==leader2:
		return
		
	group1=groups[element1]
	group2=groups[element2]

	if len(group1) < len(group2):
            element1, leader1, group1, element2, leader2, group2 = element2, leader2, group2, element1, leader1, group1

	group1 |= group2
	del groups[leader2]
	for i in group2:
		leaders[i] = leader1


def find(element, leaders):
	return leaders[element]
	
	
def hamming_candidates(value,num_bits,node_dict):

	cands=set()

	#1 bit	
	for i in range(0,num_bits):
		cand = value ^ (1 << i)
		if (node_dict[cand]==1):
			cands.add(cand)	
		
	#2 bits
	for i in range(0,num_bits):
		cand = value ^ (1 << i)
		for j in range(0,num_bits):
			if (j!=i):
				cand2 = cand ^ (1 << j)
				if (node_dict[cand2]==1):
					cands.add(cand2)
			
	return cands
				

start_time = time.time()
				
#open the file with distances and initialize the matrix of distances
f = open('clustering_big.txt', 'r')

line_no = 0
num_nodes = 0
num_bits = 0
nodes={}


node_dict={}


for line in f:
	if (line_no==0):
		#read the number of nodes from the first line
		pair = line.strip().split()
		num_nodes = int(int(pair[0]))	
		num_bits = int(int(pair[1]))	
		for i in range(0,2**num_bits):
			node_dict[i]=0
			
	else:
		#from every line 
		items = line.strip().split()
		node_val=0
		for i in range(0,len(items)):
			node_val*=2
			node_val+=int(items[i].strip())
			
		nodes[node_val]=node_val
		node_dict[node_val]=1
		
		
	line_no = line_no+1	
f.close()


clusters_merged=True
num_clusters=num_nodes


# for every node s
# generate hamming candidates that are also in graph; put them in a dictionary

i=num_nodes
node_keys=nodes.keys()

leaders={}
groups={}

for node in nodes.keys():
	elements=[node]
	make_set(elements, leaders, groups)

for node in nodes.keys():
	
	cands = hamming_candidates(node, num_bits, node_dict)
	
	for cand in cands:
		union(find(node, leaders), find(cand, leaders), leaders, groups)
			



print 'Max number of clusters is %d'%len(groups)
print '--- %s seconds ---' % (time.time() - start_time)
