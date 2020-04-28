import numpy as np
from collections import deque

## TODO: Implement this function
##
## input:
##   mat (np.array): adjacency matrix for graph
## 
## returns:
##   (np.array): distance matrix
##
## Note: You can assume input matrix is binary, square and symmetric 
##       Your output should be square and symmetric
def bfs_distance(mat):
    num_vertices = mat.shape[0]    
    res = np.full((num_vertices, num_vertices), np.inf)
    Q = deque()
    # Finish this loop
    # Done
    for u in range(num_vertices):
        visited = np.full((num_vertices), False)
        res[u,u] = 0
        Q.append((u,0))
        visited[u] = True
        while Q:
            pop = Q.popleft()
            w = pop[0]
            distance = pop[1]
            for v in range(num_vertices):
                if visited[v] == False:
                    if mat[w,v]:
                        Q.append((v,distance + 1))
                        visited[v] = True
                        res[u,v] = distance + 1 
    return res

## TODO: Implement this function
##
## input:
##   mat (np.array): adjacency matrix for graph
## 
## returns:
##   (list of np.array): list of components
##
## Note: You can assume input matrix is binary, square and symmetric 
##       Your output should be square and symmetric
def get_components(mat):
    dist_mat = bfs_distance(mat)
    num_vertices = mat.shape[0]
    available = [True for _ in range(num_vertices)]
    components = []

    while any(available):
        for v in range (num_vertices):
            if available [v] == True:
                available[v] = False
                component = []
                queue = deque([v])
                while queue:
                    node = queue.popleft()
                    component.append(node)
                    for w in range (num_vertices):
                        if available[w] == True:
                            if dist_mat[v,w] < np.inf:
                                available[w] = False
                                queue.append(w)               
                components.append(component)
    # finish this loop       
    # done
    
    # this is for testing purposes remove from final solution
    #components = [np.arange(num_vertices)]
    return components
