'''
This file should be runnable to print map_statistics using 
$ python stats.py
'''

from collections import namedtuple
from ways import load_map_from_csv


def map_statistics(roads):
    '''return a dictionary containing the desired information
    You can edit this function as you wish'''
    Stat = namedtuple('Stat', ['max', 'min', 'avg'])
    return {
        'Number of junctions' : roads.junctionCounter,
        'Number of links' : roads.linkCounter,
        'Outgoing branching factor': Stat(max=roads.max_link_by_junction, min=roads.min_link_by_junction,
                                          avg=roads.link_by_junction_avg),
        'Link distance' : Stat(max=roads.linkMaxDistance, min=roads.linkMinDistance, avg=roads.linkAvgDist),
        # value should be a dictionary
        # mapping each road_info.TYPE to the no' of links of this type
        'Link type histogram': {
            'motorway': roads.myHistogram.count(0),
            'motorway_link': roads.myHistogram.count(1),
            'trunk':  roads.myHistogram.count(2),
            'trunk_link': roads.myHistogram.count(3),
            'primary': roads.myHistogram.count(4),
            'primary_link': roads.myHistogram.count(5),
            'secondary': roads.myHistogram.count(6),
            'secondary_link': roads.myHistogram.count(7),
            'tertiary': roads.myHistogram.count(8),
            'tertiary_link': roads.myHistogram.count(9),
            'residential': roads.myHistogram.count(10),
            'living_street': roads.myHistogram.count(11),
            'unclassified': roads.myHistogram.count(12)
        },  # tip: use collections.Counter
    }


def print_stats():
    for k, v in map_statistics(load_map_from_csv()).items():
        print('{}: {}'.format(k, v))

        
if __name__ == '__main__':
    from sys import argv
    assert len(argv) == 1
    print_stats()