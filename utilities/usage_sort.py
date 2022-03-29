# Written by Dean Alvarez
# Last Modified: 7/8/20
import csv
import os
import pandas as pd
import heapq
import glob

class Row:
    #this is a custom class for the row data in our user_resources dataset.
    #the purpose of this is so we can create a heap for mering chunks
    def __init__(self,user_id,access_year,access_month,
            resource_attr_1,resource_attr_2,count,reader_number):
        self.user_id = int(user_id)
        self.access_year = access_year
        self.access_month = access_month
        self.count = count
        self.resource_attr_1 = resource_attr_1
        self.resource_attr_2 = resource_attr_2
        self.reader_number = reader_number

    def __eq__(self,other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.user_id == other.user_id

    def __lt__(self,other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.user_id < other.user_id

def write_csv_out(rows, out_path):
    with open(out_path, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        for row in rows:
            info = [row.user_id,row.access_year,row.access_month,
                    row.resource_attr_1,row.resource_attr_2,row.count]
            csv_writer.writerow(info)

def write_header(header, out_path):
    info = [header[1], header[2], header[3], header[4], header[5], header[6]]
    with open(out_path, 'a') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(info)

# This is an external sort for CSV files.
# It is suited for our specific dataset but could be modified
# Algorithm info:
# read and sort a chunk of the data using conventional methods
# write sorted data to disk
# repeat until all data is in sorted chunks
# read small amount from each chunk
# merge these mini-chunks
# In particular, I merge these mini-chunks with a min-heap. I load the first
# element from each chunk into the heap then I pop the top of the minheap and
# add another item from the chunk that the item which was popped origninated from
# complexity: nlog(n), the sorting part is nlog(n) and the merging part is
# more or less a heap-sort so it is also nlog(n).
#
# visit https://en.wikipedia.org/wiki/External_sorting for more info
def external_sort(dataframe,output_path):
    # chunk the csv into chunks size chunk_size and sort these chunks by user_id
    # write these sorted chunks to temporary files
    chunk_number = 0
    for chunk in dataframe:
        sorted_chunk = chunk.sort_values(by=['anon_person_id'])
        sorted_chunk.to_csv('tmp%d.csv'%chunk_number)
        chunk_number+= 1


    readers = []
    heap = []
    header = None
    for i in range(chunk_number):
        f = open('tmp%d.csv'%i)
        reader = csv.reader(f,delimiter=',')
        readers.append(reader)
        header = next(reader) #skip the header
        row = next(reader)
        row_obj = Row(row[1],row[2],row[3],row[4],row[5],row[6],i)
        heapq.heappush(heap,row_obj)


    write_header(header,output_path)

    write_number = 5000000 #number to write at a time
    out_list = []

    # while the heap isn't empty, write the smallest row (sorted by user_id)
    # to the out file. Call this row r.
    # if the chunk is not empty, add a row from the chunk r originated from
    # to the minheap
    while(len(heap) > 0):
        min_item = heapq.heappop(heap)
        out_list.append(min_item)
        if(len(out_list) > write_number):
            write_csv_out(out_list,output_path)
            out_list.clear()
        reader_number = min_item.reader_number
        reader = readers[reader_number]
        try:
            row = next(reader)
            row_obj = Row(row[1],row[2],row[3],row[4],row[5],row[6],reader_number)
            heapq.heappush(heap,row_obj)
        except:
            pass

    #clean tmp files
    for f in glob.glob("./tmp*.csv"):
        os.remove(f)

if __name__ ==  "__main__":
    #row per chunk. This should be changed based on how much ram is avaliable
    chunk_size = 10000000

    input_path = os.path.expanduser("~/data/new/user-resource-2009.csv")
    output_path = os.path.expanduser("~/data/new/sorted_user_resources.csv")

    reader = pd.read_csv(input_path,chunksize=chunk_size)
    external_sort(reader,output_path)
