#BFS
from heapq import heappush, heappop
class treeNode:
    def __init__(self, parent = None, value = None):
        self.parentNode = parent
        self.value = value

def find_path(src, dest, mesh):
    v = src
    vF = src
    dF = dest
    q = []
    btree = treeNode()
    visited = []
    rightboxes = []
    d = {}
    p = {}
    #visited.append(src)
    treeVisit = []
    finalNode = treeNode()
    for z in mesh['boxes']:
        #d[z] = False
        if (z[0] <= src[0] and z[1] >= src[0] and z[2]<= src[1] and z[3] >= src[1]):
            v = z
            vF = v
            btree = treeNode(value = v)
            visited.append(v)
            d[v]= True
        if(z[0] <= dest[0] and z[1] >= dest[0] and z[2] <= dest[1] and z[3] >= dest[1]):
            dF = z
    count = 0
    treeVisit.append(btree)
    heappush(q,(d[v],v))
    while q:
        dV, v = heappop(q)
        pnode = treeNode(parent = treeVisit[count], value = v)
        count+=1
        treeVisit.append(pnode)
        if v is dF:
            finalNode = pnode
            break
        neighbors = mesh['adj'].get(v,[])
        for w in neighbors:
            if w not in d:
                tnode = treeNode(parent = treeVisit[count], value = w)
                visited.append(w)      
                p[w] = v
                d[w] = True
                heappush(q, (d[w],w))


    #path = []
    if v == dF:
        tempNode = finalNode
        path = []
        list = []
        
        while tempNode is not None:
            list.append(tempNode)
            tempNode = tempNode.parentNode
            
        list.reverse()    
            
        xNext = min(list[0].value[1]-1, max(list[0].value[0], src[0]))
        yNext = max(list[0].value[3]+1, min(list[0].value[2], src[1]))
        path.append(((src[0], src[1]), (xNext, yNext)))
        
        for node in list:
            if node == list[0]:
                continue
            cx = xNext 
            cy = yNext
            xNext = min(node.value[1]-1, max(node.value[0], cx))
            yNext = max(node.value[3]+1, min(node.value[2], cy))
            path.append(((cx, cy), (xNext, yNext)))
            #node = visited[node]
        path.append(((xNext, yNext), (dest[0], dest[1])))
        #path.reverse()
        
    #print path
    return (path, visited)
