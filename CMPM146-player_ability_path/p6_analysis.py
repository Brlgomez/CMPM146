from p6_game import Simulator
from heapq import heappush, heappop
import random

ANALYSIS = {}
prev = {}
begin = {}

def analyze(design):
    sim = Simulator(design)
    init = sim.get_initial_state()
    moves = sim.get_moves()
    next_state = sim.get_next_state(init, moves[0])
    position, abilities = init # or None if character dies
    
    #ANALYSIS[init] = init

    queue = []
    visited = []
    queue.append((init, []))
    visited.append(init)
    #print queue

    while queue:
        current_state, p = queue.pop(0)
        #if current_state != sim.get_end_goal():
        #   break        
        for m in sim.get_moves():
            next_state = sim.get_next_state(current_state, m)
            if next_state is not None and next_state not in visited and next_state not in ANALYSIS:
                ANALYSIS[next_state] = p
                visited.append(next_state)
                queue.append((next_state, p + [next_state]))


def inspect((i,j), draw_line):
    possible = False
    for w in ANALYSIS:
        if i is w[0][0] and j is w[0][1]:
            possible = True
            p = ANALYSIS[w]
            #print p
            draw_line(w[0],p[-1][0],w[1],w[1])
            for n in range(len(p)):
                try:
                    draw_line(p[n][0], p[n+1][0], w[1], p[n][1])
                except IndexError:
                    "ignore error"
    if possible == False:
        print "Path not possible"

                
        '''
        if w is not None:
            print prev[w]
            draw_line(prev[w], w[0])
        if w[0] is (i, j):
            break
        '''
