# Created by Kayla Patterson 07/16/2020
# This file maps each employee to their perspective
# resources and exports it as a pickle file

import pandas as pd
import os.path
import json

from resource import Resource

if __name__ == "__main__":

    file_path = os.path.expanduser("../../data/smalldata/small_usage.csv")
    read_file = pd.read_csv(file_path, chunksize = 10000)
    employee_resources = {}

    # Reads csv file and use a dictionary to map employees id
    # to a set of their resources
    for chunk in read_file:
        for index, row in chunk.iterrows():
            employee_id = int(row['anon_person_id'])
            resource = (int(row['resource_attr_1']), int(row['resource_attr_2']))

            # If employee_id is in dictionary add current resource
            # else create new dictionary key and map it to a new set of resources
            if employee_id in employee_resources:
                employee_resources[employee_id].append(resource)
            else:
                employee_resources[employee_id] = list()
                employee_resources[employee_id].append(resource)


    with open(os.path.expanduser("../../data/smalldata/small_employee_resource_map.json"), "w") as f:
        json.dump(employee_resources, f)
