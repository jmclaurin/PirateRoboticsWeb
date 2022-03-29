# This file writes a condensed user resource table based on the targeted users
# Written by Dean Alvarez

import pandas as pd
import os.path
import timeit
import csv

def write_rows(rows,path):
    with open(path,'a', newline = '') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

def get_target_users():
    path = os.path.expanduser("../../../data/target_users.csv")
    target_users = set()
    with open(path,'r', newline = '') as f:
        reader = csv.reader(f)
        for row in reader:
            target_users.add(int(row[0]))
    
    return target_users

if __name__ == "__main__":

    input_path = os.path.expanduser("../../../data/new/sorted_user_resources.csv")
    output_path = os.path.expanduser("../../../data/new/target_usage_table_1.csv")
    reader = pd.read_csv(input_path, chunksize = 100000)
    target_users = get_target_users()
    row_buffer = []
    max_buffer = 100000
    start = timeit.default_timer()

    for chunk in reader:
        for index, row in chunk.iterrows():
            anon_id = int(row['anon_person_id'])
            attr_1 = int(row['resource_attr_1'])
            attr_2 = int(row['resource_attr_2'])
            if anon_id in target_users:
               row = [attr_1,attr_2,anon_id]
               row_buffer.append(row)
            if len(row_buffer) > max_buffer:
                write_rows(row_buffer,output_path)
                row_buffer.clear()
    

    write_rows(row_buffer,output_path)
    end = timeit.default_timer()
    print("Time: ", end - start)

