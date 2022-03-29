# Created by Kayla Patterson 07/16/2020
# This file maps each user to their perspective
# resources and exports it as a pickle file

import pandas as pd
import os.path
import pickle

# importing Resource class
from resource_map_creator import Resource

if __name__ == "__main__":

    file_path = os.path.expanduser("../../data/smalldata/sorted_user_resources.csv")
    read_file = pd.read_csv(file_path, chunksize = 10000)
    user_resources = {}


    # Reads csv file and use a dictionary to map user ids
    # to a set of their resources
    for chunk in read_file:
        for index, row in chunk.iterrows():
            user_id = row['user_id']
            resource = Resource(row['resource_attr_1'], row['resource_attr_2'])

            # If user_id is in dictionary add current resource
            # else create new dictionary key and map it to a new set of resources
            if user_id in user_resources:
                user_resources[user_id].add(resource)
            else:
                user_resources[user_id] = set()
                user_resources[user_id].add(resource)


    with open(os.path.expanduser("../../data/smalldata/small_user_resouce_map.pkl"), "wb") as f:
        pickle.dump(user_resources,f)
