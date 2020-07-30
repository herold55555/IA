import sys

from ways import tools
from ways import graph
from ways import info
from queue import PriorityQueue
import math


def compute_neighbors(junction):
    neighbors = set()
    i = 0
    for link in junction.links:
        for nodeNumber in link:
            if nodeNumber == junction.index:
                continue
            if i > 0:
                break
            if nodeNumber not in neighbors:
                neighbors.add(nodeNumber)
            i = i + 1
        i = 0
    return neighbors


def compute_distance(lat1, lon1, lat2, lon2):
    return tools.compute_distance(lat1, lon1, lat2, lon2)


def find_junction(roads, index):
    junction = roads.findJunction[index]
    return junction


def create_road():
    return graph.load_map_from_csv(filename='israel.csv', start=0, count=sys.maxsize)


def find_path(source, target, dictonary):
    path = list()
    path.append(target)
    node = dictonary[target]
    while node.index != source:
       path.append(node.index)
       node = dictonary[node.index]
    path.append(source)
    path.reverse()
    return path


def road_info(road_index):
    return info.ROAD_DICTONARY[road_index]


class My_Priority_Queue(PriorityQueue):

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue

    def __remove__(self, item):
        new_queue = My_Priority_Queue()
        while not self.empty():
            node = self.get()
            if node == item:
                continue
            new_queue.put(node)
        return new_queue


def euclidean_distance_speed(x1, y1, x2, y2):
    distance = compute_distance(x1, y1, x2, y2)
    max_speed = 110
    """""
    for i in range(len(info.ROAD_DICTONARY)):
        if i > max_speed:
            max_speed = i
    """""
    cost = distance / max_speed
    return cost


def compute_cost(my_road, node1, node2):
    link = my_road.findLink(node1.index, node2.index)
    distance = link.distance / 1000
    speed = road_info(link.highway_type)
    cost = distance / speed
    return cost


def euclidean_dist(x1, y1, x2, y2):
    x = x2 - x1
    y = y2 - y1
    x = x**2
    y = y**2
    distance = math.sqrt(x + y)
    return distance