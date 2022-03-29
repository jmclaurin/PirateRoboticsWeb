# This file does some basic analysis on the intersection of the resources
# with the highest usage

import pickle
from resource_map_creator import Resource

resource_map = pickle.load( open("../../data/resource_map.pkl", "rb") )

most_used = set()

for i in range(10):
    temp = None
    most_used_usage = 0
    for resource in resource_map.keys():
        if (len(resource_map[resource]) >= most_used_usage
            and not resource in most_used
        ):
            temp = resource
            most_used_usage = len(resource_map[resource])
    most_used.add(temp)


for r2 in most_used:
    for r1 in most_used:
        if(r1 != r2):
            print(Resource.overlap_ratio(resource_map[r1],resource_map[r2]))
    print(" ")
