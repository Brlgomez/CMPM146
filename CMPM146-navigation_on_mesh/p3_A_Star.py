#A*
from heapq import heappush, heappop           
from math import *                                                         
def find_path(src, dest, mesh):   
    v = src                                                         
    vF = src                                                                             
    dF = dest                                                                            
    q = []                                                                    
    visited = []                                                                         
    rightboxes = []                                                                      
    d = {}                                                                               
    p = {}                      
    dist = {}
    cost_so_far = {}
    #visited.append(src)                                                               
    for z in mesh['boxes']:                                                            
        if (z[0] <= src[0] and z[1] >= src[0] and z[2]<= src[1] and z[3] >= src[1]):     
            v = z                                                                        
            vF = v                                  
            visited.append(v)                                                            
            dist[v] = 0
            cost_so_far[v] = 0
        if(z[0] <= dest[0] and z[1] >= dest[0] and z[2] <= dest[1] and z[3] >= dest[1]): 
            dF = z 
                                             
        
    count = 0                                                                        
    heappush(q,(0,(src, v)))                                                    
    while q:                                                                             
        dV, v = heappop(q)                          
        count += 1                                                                   
        if v[1] is dF:
            break                                                                        
        neighbors = mesh['adj'].get(v[1],[])                                         
        for w in neighbors:
            xNext = min(w[1]-1, max(w[0], v[0][0]))
            yNext = min(w[3]-1, max(w[2], v[0][1]))
            
            alt = dist[v[1]] + sqrt(((v[0][0]-v[0][1])*(v[0][0]-v[0][1])) + ((xNext-yNext)*(xNext-yNext)))
            cost = cost_so_far[v[1]] + abs(dest[0] - xNext) + abs(dest[1] - yNext)
            #visited.append(w)
            if w not in dist or alt < dist[w]:
                cost_so_far[w] = cost                   
                dist[w] = alt
                visited.append(w)
                co = (xNext, yNext)
                if w == dF:
                    co = dest
                p[co] = v[0]
                priority = cost + abs(dest[0] - xNext) + abs(dest[1] - yNext)
                heappush(q, (priority,(co,w)))
    
    #path = []                                                 
    if v[1] is dF:                                                              
        path = []                                                                        
        list = []
        node = dest
        prev = (0, 0)
        while node in p:
            path.append((p[node], node))
            node = p[node]
        path.append((src, node))
        path.reverse()
        return(path, visited)
    else:
        print "ERROR"
        path = []
        return(path, visited)
