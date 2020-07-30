'''
Parse input and run appropriate code.
Don't use this file for the actual work; only minimal code should be here.
We just parse input and call methods from other modules.
'''

#do NOT import ways. This should be done from other files
#simply import your modules and call the appropriate functions
import sys

import help
from ways import draw
import queue
import os

my_road = help.create_road()


def dfs(source):
    start = help.find_junction(my_road, source)
    visited, stack = set(), [start.index]
    j = 0
    path = list()
    while stack:
        vertex_num = stack.pop()
        vertex = help.find_junction(my_road, vertex_num)
        if vertex.index not in visited:
            visited.add(vertex.index)
            path.append(vertex.index)
            neighbors = help.compute_neighbors(vertex)
            for neighbor in neighbors:
                i = help.find_junction(my_road, neighbor)
                if i.index not in visited:
                   stack.append(i.index)
                   break
        j = j + 1
        if j > 7:
            break
    return path


def problems_list(filename):
    import csv
    from itertools import islice
    problems = list()
    with open(filename, 'rt') as f:
        it = islice(f, 0, sys.maxsize)
        for row in csv.reader(it):
            str = row[0]
            problems.append(str)
    return problems


def time_travel(source, target, algo, dict1, result_path, f, dict2=None):
    path = "results/"
    if not os.listdir(path):
        try:
            os.mkdir(path)
        except:
            pass
    total_time = dict1[target]
    if algo == 'ucs':
        f.write(str(source) + ', ' + str(target) + ': ' + str(total_time) + '\n')
    if algo == 'astar'or algo == 'ida':
        estimed_time = dict2[source]
        f.write(str(source) + ', ' + str(target) + ': ' + str(estimed_time) + ' , ' +
                str(total_time) + '\n')


def find_ucs_rout(source, target, compute_dist):
    'call function to find path, and return list of indices'
    visited = dict()
    parentDict = dict()
    start = help.find_junction(my_road, source)
    goal = help.find_junction(my_road, target)
    queue = help.My_Priority_Queue()
    queue.put((0, start))
    while queue:
        cost, node = queue.get()
        if node.index not in visited:
            visited[node.index] = cost
            if node.index == target:
                path = help.find_path(source, target, parentDict)
                return path
            neighbors = help.compute_neighbors(node)
            for neighbor in neighbors:
                i = help.find_junction(my_road, neighbor)
                if i == node:
                    continue
                distance = compute_dist(my_road, node, i)
                if i.index not in visited:
                    new_cost = cost + distance
                    if queue.__contains__(i):
                        if visited[i.index] > new_cost:
                            queue.__remove__(i)
                            parentDict[i.index] = node
                            queue.put((new_cost, i))
                    else:
                        parentDict[i.index] = node
                        queue.put((new_cost, i))
    return "NO PATH"


def find_astar_route(source, target, compute_dist, h):
    parentDict = dict()
    start = help.find_junction(my_road, source)
    goal = help.find_junction(my_road, target)
    queue = help.My_Priority_Queue()
    f_score = dict()
    g_score = dict()
    for junc in my_road.junctions():
        g_score[junc.index] = sys.maxsize
        f_score[junc.index] = sys.maxsize
    f_score[start.index] = h(start.lat, start.lon, goal.lat, goal.lon)
    g_score[start.index] = 0
    score_in_queue = dict()
    queue.put((f_score[start.index], start))
    score_in_queue[start.index] = h(start.lat, start.lon, goal.lat, goal.lon)
    while queue:
        score_f, node = queue.get()
        if node.index == target:
            path = help.find_path(source, target, parentDict)
            return path
        neighbors = help.compute_neighbors(node)
        for neighbor in neighbors:
            i = help.find_junction(my_road, neighbor)
            distance = compute_dist(my_road, node, i)
            new_cost = g_score[node.index] + distance
            if new_cost < g_score[i.index]:
                    parentDict[i.index] = node
                    g_score[i.index] = new_cost
                    f_score[i.index] = g_score[i.index] + h(i.lat, i.lon, goal.lat, goal.lon)
                    if not queue.__contains__(i):
                        queue.put((f_score[i.index], i))
                        score_in_queue[i.index] = f_score[i.index]
                    else:
                        if score_in_queue[i.index] > f_score[i.index]:
                            queue.__remove__(i)
                            parentDict[i.index] = node
                            queue.put((f_score[i.index], i))
                            score_in_queue[i.index] = f_score[i.index]
    return "NO PATH"


def find_idastar_route(source, target, compute_dist, h):
    start = help.find_junction(my_road, source)
    goal = help.find_junction(my_road, target)
    limit = h(start.lat, start.lon, goal.lat, goal.lon)
    path = list()
    path.append(start.index)
    g_score = dict()
    g_score[start.index] = 0
    f_score = dict()
    f_score[start.index] = h(start.lat, start.lon, goal.lat, goal.lon)
    while True:
        found, solution = dfs_s(start, 0, path, limit, goal, h, compute_dist, g_score)
        if found == "PATH FOUND":
            final_path = solution
            return final_path
        if found == sys.maxsize:
            "NO PATH EXIST"
        limit = found


def dfs_s(state, cost, path, f_limit, goal, h, compute_cost, g_score):
    g_score[state.index] = cost
    new_f = cost + h(state.lat, state.lon, goal.lat, goal.lon)
    if new_f > f_limit:
        return new_f, path
    if state == goal:
        return "PATH FOUND", path
    min = sys.maxsize
    neighbors = help.compute_neighbors(state)
    for neighbor in neighbors:
        i = help.find_junction(my_road, neighbor)
        if neighbor not in path:
            path.append(neighbor)
            new_cost = compute_cost(my_road, state, i) + cost
            g_score[i.index] = new_cost
            solution, path = dfs_s(i, new_cost, path, f_limit, goal, h, compute_cost, g_score)
            if solution == "PATH FOUND":
                return "PATH FOUND", path
            elif solution < min:
                min = solution
            path.pop()
    return min, path


def dispatch(argv):
    from sys import argv
    source, target = int(argv[2]), int(argv[3])
    if argv[1] == 'ucs':
        path = find_ucs_rout(source, target, help.compute_cost)
    elif argv[1] == 'astar':
        path = find_astar_route(source, target, help.compute_cost, help.euclidean_distance_speed)
    elif argv[1] == 'idastar':
        path = find_idastar_route(source, target, help.compute_cost, help.euclidean_distance_speed)
    print(' '.join(str(j) for j in path))


if __name__ == '__main__':
    from sys import argv
    dispatch(argv)
