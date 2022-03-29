# Created by Tedi Mitiku 07/08/2020
# Test cases for distance_valiation.py

import unittest
from distance_validation import l2_distance, cosine_distance
import numpy as np
import pandas as pd
import math,random

#Test l2 distance function
class TestEuclideanDistanceFunction(unittest.TestCase):
    def test_zero_distance(self):
        #Make sure that the distance between and user and themselves is 0
        user_one_attributes = [1, 2, 3, 5, 18, 10]
        self.assertEqual(l2_distance(user_one_attributes, user_one_attributes), 0)

    def test_same_output(self):
        #Make sure that the output is the same when switching inputs
        user_one_attributes = [1, 2, 3, 5, 18, 10]
        user_two_attributes = [5, 7, 2, 1, 9, 5]
        self.assertAlmostEqual(l2_distance(user_one_attributes, user_two_attributes), 12.80624847)
        self.assertAlmostEqual(l2_distance(user_two_attributes, user_one_attributes), 12.80624847)

    def test_float(self):
        #Make sure that the output is correct with floating point numbers
        user_one_attributes = [0.1, 0.2, 0.3, 0.5, 1.8, 1]
        user_two_attributes = [0.5, 0.7, 0.2, 0.1, 0.9, 0.5]
        self.assertAlmostEqual(l2_distance(user_one_attributes, user_two_attributes), 1.280624847)
        self.assertAlmostEqual(l2_distance(user_two_attributes, user_one_attributes), 1.280624847)

#Test cosine distance function created by Kayla Patterson 07/14/2020
class TestCosineDistanceFunction(unittest.TestCase):
    def test_zero_distance(self):
        #Ensure that two users that are the same is equal to 1
        #Cosine Distance is different from Euclidean since when users are the same the
        #output would be 1, instead of 0. Since, the cosine distance calculates the angle.
        user_one_attributes = [1, 3, 5, 7, 8, 14]
        result = cosine_distance(user_one_attributes, user_one_attributes)
        expected = np.array([[1.0]])
        np.testing.assert_array_almost_equal(result, expected)

    def test_same_output(self):
        #Make sure that the output is the same when switching inputs
        user_one_attributes = [1, 2, 4, 6, 8, 9]
        user_two_attributes = [3, 5, 6, 7, 9, 2]
        result_1 = cosine_distance(user_one_attributes, user_two_attributes)
        result_2 = cosine_distance(user_two_attributes, user_one_attributes)
        expected = np.array([[0.832522]])
        np.testing.assert_array_almost_equal(result_1, expected)
        np.testing.assert_array_almost_equal(result_2, expected)

    def test_float(self):
        #Make sure that the output is correct with floating point numbers
        user_one_attributes = [0.2, 0.4, 0.6, 0.7, 0.1, 0.9]
        user_two_attributes = [0.1, 0.3, 0.5, 1.4, 0.9, 3]
        result = cosine_distance(user_one_attributes, user_two_attributes)
        expected = np.array([[0.884321]])
        np.testing.assert_array_almost_equal(result, expected)

if __name__ == '__main__':
    unittest.main()
