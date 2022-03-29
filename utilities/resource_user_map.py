# This file saves the dictionary of the resources to the set of useres
# as a pickle file. It also contains the Resource class

import pandas as pd
import os.path
import timeit
import pickle
from resource import Resource


if __name__ == "__main__":

    input_path = os.path.expanduser("../../data/sorted_user_resources.csv")
    reader = pd.read_csv(input_path, chunksize = 100000)
    resource_users = {}

    start = timeit.default_timer()

    for chunk in reader:
        for index, row in chunk.iterrows():
            resource = Resource(row['resource_attr_1'],row['resource_attr_2'])
            if resource in resource_users:
                resource_users[resource].add(row['anon_person_id'])
            else:
                resource_users[resource] = {row['anon_person_id']}

    end = timeit.default_timer()
    print("Time: ", end - start)
    PATH = os.path.expanduser("../../data/resource_employee_map.pkl")
    with open(PATH,"wb") as f:
        pickle.dump(resource_users,f)
