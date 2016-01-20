from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop

def dijkstras_shortest_path(src, dst, graph, adj):
  path = []
  dist = {}
  prev = {}
  queue = []

  heappush(queue, (0, src))
  dist = {src: 0}
  prev = {src: None}
  
  while queue:
    u = heappop(queue)
    neighbors = adj(graph, u[1])

    for v in neighbors:
      alt = neighbors[v] + dist.get(u[1])
      if v not in dist or alt < dist[v]:
        dist[v] = alt
        prev[v] = u
        heappush(queue, (alt, v))

    if u[1] == dst:
      path = []
      while u:
        path.append(u[1])
        u = prev[u[1]]
      path.reverse()
      return path

def navigation_edges(level, cell):
  steps = {}
  x, y = cell
  for dx in [-1,0,1]:
    for dy in [-1,0,1]:
      
      new_dist = sqrt(dx*dx+dy*dy)
      next_cell = (x + dx, y + dy)
      
      if new_dist > 0 and next_cell in level['spaces']:
        steps[next_cell] = new_dist
        

  return steps

def test_route(filename, src_waypoint, dst_waypoint):
  level = load_level(filename)
  
  show_level(level)
  
  src = level['waypoints'][src_waypoint]
  dst = level['waypoints'][dst_waypoint]
  
  path = dijkstras_shortest_path(src, dst, level, navigation_edges)
  
  if path:
    show_level(level, path)
  else:
    print "No path possible!"

if __name__ ==  '__main__':
  import sys
  _, filename, src_waypoint, dst_waypoint = sys.argv
  test_route(filename, src_waypoint, dst_waypoint)
