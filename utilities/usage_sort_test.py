
from csv_sort import external_sort
import pandas as pd
import os
import unittest

class TestExternalSortAccuracy(unittest.TestCase):
    # Tests that external_sort sorts accurately
    def test_accuracy(self):
        input_path = os.path.expanduser("~/data/user_resources.csv")
        test_path = os.path.expanduser("./testing_dataset.csv")
        df = pd.read_csv(input_path)
        chunked_df = pd.read_csv(input_path,chunksize=100000)
        external_sort(chunked_df,test_path)
        external_sorted = pd.read_csv(test_path)
        internal_sorted = df.sort_values(by=['user_id'])
        internal_sorted.reset_index(drop=True,inplace=True)

        # make sure that we have the same
        # (types are not preserved when writting to csv)
        internal_sorted['user_id'] = pd.to_numeric(internal_sorted['user_id'])
        external_sorted['user_id'] = pd.to_numeric(external_sorted['user_id'])

        #we onlt care about the user_ids so we are going to just compare those
        internal_list = internal_sorted['user_id'].tolist()
        external_list = external_sorted['user_id'].tolist()

        same = True
        for i,e in zip(internal_list,external_list):
            if i != e:
                print("internal: %d  external: %d"%(i,e))
                same = False

        self.assertTrue(same)

        #clean up the file we wrote
        os.remove(test_path)

if __name__ == '__main__':
    unittest.main()
