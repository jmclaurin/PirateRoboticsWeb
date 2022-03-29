
# Created by Kayla Patterson 07/07/20
# This class allows for data to be normalized between the ranges of 0 - 1
# which allows for data to be analyzed efficiently.

import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#Normalizing data between the range of 0 - 1
def normalize(data, cols):
    """Normalizes the data between the range of 0 -1 using
       the scikit-learn library.

    Args:
        data(DataFrame): The data in the DataFrame
        cols(int): The # of columns in data to normalize

    """
    min_max_scaler = MinMaxScaler()
    data.iloc[:,0:cols] = min_max_scaler.fit_transform(data.iloc[:,0:cols])
