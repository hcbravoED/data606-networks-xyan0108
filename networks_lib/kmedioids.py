import numpy as np
import random as random

## TODO: Implement this function
## Done
## Input:
##  - dmat (np.array): symmetric array of distances
##  - K (int): Number of clusters
##
## Output:
##   (np.array): initialize by choosing random number of points as medioids
def random_init(dmat, K):
    num_vertices = dmat.shape[0]
    medioids = np.array(random.sample(list(np.arange(num_vertices)), k=K), dtype=np.int)
    print (medioids)
    return medioids

## TODO: Implement this function
## Done
## Input:
##   - dmat (np.array): symmetric array of distances
##   - medioids (np.array): indices of current medioids
##
## Output:
##   - (np.array): assignment of each point to nearest medioid
def assign(dmat, medioids):
    num_vertices = dmat.shape[0]
    assignment = np.zeros((num_vertices), dtype=np.int)
    medioid0 = medioids[0]
    medioid1 = medioids[1]
    for v in range (num_vertices):
        if dmat[medioid0,v].astype(int) > dmat[medioid1,v].astype(int):
            assignment[v] = 1
        else:
            assignment[v] = 0  
    print(assignment)
    return assignment

## TODO: Implement this function
## Done
## Input:
##   - dmat (np.array): symmetric array of distances
##   - assignment (np.array): cluster assignment for each point
##   - K (int): number of clusters
##
## Output:
##   (np.array): indices of selected medioids
def get_medioids(dmat, assignment, K):
    num_vertices = dmat.shape[0]
    dist_array = np.sum(dmat, axis = 0)
    medioids = np.zeros((K), dtype=np.int)
    
    for k in range (K):
        distance = {}
        for v in range (num_vertices):
            if assignment[v] == k:
                distance_v = 0
                for w in range (num_vertices):
                    if assignment[v] == assignment[w]:
                        distance_v += dmat[v,w]                       
                distance[v] = distance_v
        temp = min(distance.values())
        key = [key for key in distance if distance[key] == temp]
        medioids[k] = np.array([min(key)])                
    print (medioids)
    return medioids

## TODO: Finish implementing this function
## 
## Input:
##   - dmat (np.array): symmetric array of distances
##   - K (int): number of clusters
##   - niter (int): maximum number of iterations
##
## Output:
##   - (np.array): assignment of each point to cluster
def kmedioids(dmat, K, niter=10):
    num_vertices = dmat.shape[0]

    # we're checking for convergence by seeing if medioids
    # don't change so set some value to compare to
    old_medioids = np.full((K), np.inf, dtype=np.int)
    medioids = random_init(dmat, K)
    
    # this is here to define the variable before the loop
    assignment = np.full((num_vertices), np.inf)
   
    it = 0
    while np.any(old_medioids != medioids) and it < niter:
        it += 1
        old_medioids = medioids
        assignment = assign(dmat, medioids)
        medioids = get_medioids(dmat, assignment, K)
        # finish implementing this section
        # done

    print (assignment)
    return assignment
        