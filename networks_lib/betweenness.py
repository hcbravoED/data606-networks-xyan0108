import numpy as np
from collections import deque
from networks_lib.distance import bfs_distance
from collections import defaultdict

## TODO: Implement this function
##
## Implements the breadth-first algorithm of Girvan-Newman to compute
##   number (fractional) of shortest paths starting from a given vertex
##   that go through each edge of the graph
##
## Input:
##   - vertex (int): index of vertex paths start from
##   - mat (np.array): n-by-n adjacency matrix
##
## Output:
##   (np.array): n-by-n edge count matrix
##
## Note: assume input adjacency matrix is binary and symmetric
def edge_counts(vertex, mat):
    num_vertices = mat.shape[0]
    res = np.zeros((num_vertices, num_vertices))

    
## Look for the nodes on the same level by finding nodes with same distance to the starting vertex, also are adjacent to each other. Then remove the adjacency between these nodes so that the connections will not show up in root-to-leaf process.  
    dist_mat = bfs_distance (mat)
    mat_copy = mat.copy()  
    for node1 in range (num_vertices):
        for node2 in range (num_vertices):
            if dist_mat[vertex, node1] == dist_mat[vertex, node2]:
                if mat_copy [node1, node2] == 1:
                    mat_copy [node1, node2] = 0
## print(mat_copy)
## output revised mat_copy
##  [[0 1 0 0 0 0 0]
##  [1 0 1 1 0 0 0]
##  [0 1 0 0 0 0 0]
##  [0 1 0 0 1 1 0]
##  [0 0 0 1 0 0 1]
##  [0 0 0 1 0 0 1]
##  [0 0 0 0 1 1 0]]                    


## Look for the nodes on each level of the search tree.    
    level = defaultdict(list)     
    level_count = np.unique(dist_mat[vertex])
    for i in range (len(level_count)):
        for node in range (num_vertices):
            if dist_mat[vertex, node] == level_count[i]:
                level[level_count[i]].append(node)
##  print (level.items()) for vertex 'E'
## output:
## dict_items([(0.0, [4]), (1.0, [3, 6]), (2.0, [1, 5]), (3.0, [0, 2])])


## Find leaves. If the distance between vertex 'E' and one node is longer than the distances between vertex 'E' and the node's all the neighbors, the node is a leaf.
    leaves = []  
    for v in range (num_vertices):
        count_child = 0
        for u in range (num_vertices):
            if dist_mat[v,u] == 1:
                if dist_mat[vertex,v] < dist_mat[vertex,u]:
                    count_child += 1
        if count_child == 0:
            leaves.append(v)     
## print (leaves)
## output: [0, 2, 5]


## Root to Leaf: Acquire edge-count for each node.
## Input: modified adjacency matrix of size 7 by 7
## Output: a dictionary of shortest path counts for each node, with 7 key:value pairs.
##    - create boolean array 'visited' of length 7
##    - initialize all vertices u as `visited[u]=False` except for the starting vertex 'E'
##    - set the shortest path number for 'E' as 1
##    - push tuple '(E/4, 1)' to a FIFO queue 'Q'
##    - while 'Q' is not empty:
##        - Pop tuple '(w, edge_count)' from the top of 'Q'
##        - for each neighbor 'v' of 'w'
##            - if 'visited[v] = False', set 'visited[v] = True'
##            - for each neighbor 'u' of 'v'
##                - if u have been visited (partent(s) of v)
##                - add the edge_count of u to the edge_count of v
    Q = deque()
    edge_counts_ = {}
    visited = np.full((num_vertices), False)    
        
    visited[vertex] = True
    edge_counts_[vertex] = 1
    Q.append((vertex,1))
    while Q:
        pop = Q.popleft()
        w = pop[0]
        count = pop[1]
        for v in range(num_vertices):
            if visited[v] == False:
                if mat_copy[w,v]:
                    visited[v] = True
                    edge_count = 0                    
                    for u in range(num_vertices):
                        if mat_copy[v,u]:
                            if visited[u] == True:
                                edge_count += edge_counts_[u]                               
                                edge_counts_[v] = edge_count
                    Q.append((v,edge_count))
## print (edge_counts_)
## output:
## {4: 1, 3: 1, 6: 1, 1: 1, 5: 2, 0: 1, 2: 1}
## print (Q)
## output:
##    deque([(3, 1)])
##    deque([(3, 1), (6, 1)])
##    deque([(6, 1), (1, 1)])
##    deque([(6, 1), (1, 1), (5, 2)])
##    deque([(5, 2), (0, 1)])
##    deque([(5, 2), (0, 1), (2, 1)]) 

## Find child(ren) for each node.
    
    children = defaultdict(list)
    for v in range (num_vertices):
        for w in range (num_vertices):
            if mat[v,w] == 1:
                if dist_mat[vertex,v] < dist_mat[vertex,w]:
                    children[v].append(w)
    #print(children.items())
                    
## Compute weighted edge count
    credit = {}
    for i in reversed(range(len(level_count))):
        for v in level[i]:
            credit_v = 0
            if v in leaves:
                credit[v] = 1
                #for w in mat_copy[v]:
                 #   if mat_copy[w,v] == 1:
                  #      res[w,v] = res [v,w] = (edge_counts_[w]/edge_counts_[v])*credit[v]
            else:
                for c in children[v]:
                    credit_v += ((edge_counts_[v]/edge_counts_[c])*credit[c])
                    credit[v] = credit_v + 1
                    res[c,v] = res[v,c] = ((edge_counts_[v]/edge_counts_[c])*credit[c])    
## print (credit)
## dict_items([(0, [1, 2]), (1, [3]), (3, [4, 5, 6])])
## {4: 1, 5: 1, 6: 1, 3: 4.0, 1: 5.0, 2: 1, 0: 7.0}
## dict_items([(1, [0, 2, 3]), (3, [4, 5, 6])])
## {4: 1, 5: 1, 6: 1, 0: 1, 2: 1, 3: 4.0, 1: 7.0}
## dict_items([(1, [3]), (2, [0, 1]), (3, [4, 5, 6])])
## {4: 1, 5: 1, 6: 1, 3: 4.0, 0: 1, 1: 5.0, 2: 7.0}
## dict_items([(1, [0, 2]), (3, [1, 4, 5, 6])])
## {0: 1, 2: 1, 1: 3.0, 4: 1, 5: 1, 6: 1, 3: 7.0}
## dict_items([(1, [0, 2]), (3, [1, 5]), (4, [3, 6]), (6, [5])])
## {0: 1, 2: 1, 1: 3.0, 5: 1, 3: 4.5, 6: 1.5, 4: 7.0}
## dict_items([(1, [0, 2]), (3, [1, 4]), (5, [3, 6]), (6, [4])])
## {0: 1, 2: 1, 1: 3.0, 4: 1, 3: 4.5, 6: 1.5, 5: 7.0}
## dict_items([(1, [0, 2]), (3, [1]), (6, [3, 4, 5])])
## {0: 1, 2: 1, 1: 3.0, 3: 4.0, 4: 1, 5: 1, 6: 7.0}             
   #print (res)
    return res

## Compute edge betweeness for a graph
## 
## Input: 
##   - mat (np.array): n-by-n adjacency matrix. 
##
## Output:
##   (np.array): n-by-n matrix of edge betweenness
##
## Notes: Input matrix is assumed binary and symmetric
def edge_betweenness(mat):
    res = np.zeros(mat.shape)
    num_vertices = mat.shape[0]
    for i in range(num_vertices):
        res += edge_counts(i, mat)
    return res / 2.