# Created by Kayla Patterson 07/08/2020
# Test file for normalizing_data.py

import unittest
from normalizing_data import normalize
import pandas as pd
from pandas._testing import assert_frame_equal

class TestNormalizationData(unittest.TestCase):
    def test_data_normalized(self):
        #Test that data is being normalized
        df = pd.DataFrame({
            'id_1':[1, 2, 3],
            'id_2':[1, 1, 1],
            'id_3':[1, 2, 3]
            })

        normalize(df,3)

        expected = pd.DataFrame({
            'id_1':[0.0, 0.5, 1.0],
            'id_2':[0.0, 0.0, 0.0],
            'id_3':[0.0, 0.5, 1.0]
            })

        assert_frame_equal(df, expected, check_dtype=False)

if __name__ == '__main__':
    unittest.main()
