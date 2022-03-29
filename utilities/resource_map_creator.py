# This file saves the dictionary of the resources to the set of useres
# as a pickle file. It also contains the Resource class

import pandas as pd
import os.path
import timeit
import pickle

class Resource:

    def __init__(self, attr_1, attr_2):
        self.attr_1 = int(attr_1)
        self.attr_2 = int(attr_2)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        else:
            return self.attr_1 == other.attr_1 and self.attr_2 == other.attr_2

    # We hash resources based off of attr1 and attr2
    # This technique is called cantor pairing
    # See en.wikipedia.org/wiki/Pairing_function for more information
    def __hash__(self):
        return (((self.attr_1+self.attr_2+1)*(self.attr_1+self.attr_2)//2)
                +self.attr_2)


    @staticmethod
    def overlap_ratio(set1, set2):
        num_in_common = len(set1.intersection(set2))
        total_unique_elements = len(set1)+len(set2)-num_in_common
        return num_in_common/total_unique_elements


if __name__ == "__main__":

    input_path = os.path.expanduser("../../data/sorted_usage_table.csv")
    reader = pd.read_csv(input_path, chunksize = 100000)
    resource_users = {}

    start = timeit.default_timer()

    for chunk in reader:
        for index, row in chunk.iterrows():
            resource = Resource(row['resource_attr_1'],row['resource_attr_2'])
            if resource in resource_users:
                resource_users[resource].add(row['user_id'])
            else:
                resource_users[resource] = {row['user_id']}

    end = timeit.default_timer()
    print("Time: ", end - start)

    with open(os.path.expanduser("../../data/resource_employee_map.pkl"),"wb") as f:
        pickle.dump(resource_users,f)
