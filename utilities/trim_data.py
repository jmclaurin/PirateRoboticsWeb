
import csv, json, pickle
from random import randint

import numpy as np
import pandas as pd

from company import Company
from employee import Employee

# Get subtree hierarchy
with open('../../data/smalldata/small_company_hierarchy.json', 'r') as infile:
    small_company = json.load(infile)

# Build set of ids within subtree
small_employee_ids = set()

def read_employees_from_tree(company_hierarchy, employee_ids):
    """ Recursive function to get a list of employee ids in the tree"""
    if(company_hierarchy.get("Reports") is None):
        employee_ids.add(int(company_hierarchy.get("Employee")))
        return

    employee_ids.add(int(company_hierarchy.get("Employee")))
    for report in company_hierarchy.get("Reports"):
        company_hierarchy = report
        read_employees_from_tree(company_hierarchy)

read_employees_from_tree(small_company, small_employee_ids)
print(small_employee_ids)
print(len(small_employee_ids))

# Trim user datset to subtree employees
columns = ["anon_person_id", "anon_department", "anon_cost_center_num", "anon_manager_person_id",
        "anon_location_country","anon_lowest_dir_person_id", "anon_visible_job_family", "anon_person_type"]

small_user = pd.DataFrame(columns=columns)

with open('../../data/sorted_user.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for user in reader:
        if(int(user[0]) in small_employee_ids):
            employee_data = { "anon_person_id": user[0],
                            "anon_department": user[1],
                            "anon_cost_center_num": user[2],
                            "anon_manager_person_id": user[3],
                            "anon_location_country": user[4],
                            "anon_lowest_dir_person_id": user[5],
                            "anon_visible_job_family": user[6],
                            "anon_person_type": user[7] }
            small_user.append(employee_data, ignore_index=True)


small_user.to_csv("../../data/smalldata/small_user.csv", index=False)
print(small_user)

# Trim usage dataset to subtree employees
columns = ["anon_person_id", "access_year", "access_month", "resource_attr_1",
        "resource_attr_2","count"]

small_usage = pd.DataFrame(columns=columns)

big_usage = pd.read_csv("../../data/user-resource-2009.csv", chunksize = 10000, iterator=True)
for chunk in big_usage:
    for index, resource in chunk.iterrows():
        if(int(resource[0]) in small_employee_ids):
            usage_data = { "anon_person_id": resource[0],
                        "access_year": resource[1],
                        "access_month":resource[2],
                        "resource_attr_1": resource[3],
                        "resource_attr_2": resource[4],
                        "count":resource[5]
                        }
            small_usage.append(usage_data, ignore_index=True)

small_usage.to_csv("../../data/smalldata/small_usage.csv", index=False)
print(small_usage)
