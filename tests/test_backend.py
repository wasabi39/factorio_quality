"""
Since this is a small personal project, I have decided to write
just a small handful of test cases for the backend.
The most important things to test are that the end result
and that the transition matrix are generated correctly.
The main purpose of testing the backend is to ensure that
the Markov chain calculations do not break during refactoring.
"""

import unittest
import numpy as np

from backend import generate_transition_matrix, run_simulation
from computation_request import ComputationRequest

class TestBackend(unittest.TestCase):
    def test_generate_transition_matrix(self):
        """
        Test that the transition matrix is generated properly.
        """
        computation_request = ComputationRequest(
            productivity_boost_from_research=0,
            machine_type="Electromagnetic plant",
            quality_of_production_modules="Legendary",
            number_of_productivity_modules=0,
            quality_of_quality_modules="Legendary",
            number_of_quality_modules=5,
            number_of_iterations=1,
            quality_1_count=1,
            quality_2_count=0,
            quality_3_count=0,
            quality_4_count=0)
        result = generate_transition_matrix(computation_request)
        
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(result.shape, (10, 10))
        #Check that first 5 rows sum to 1.5 each due to the 50% productivity boost.
        #Check that the next 4 rows sum to 0.25 each 
        #due to the -75% productivity boost when recycling.
        #Check that the last row sums to 1, it should be [0,0,0,0,0,0,0,0,0,1].
        expected_row_sums = [1.5] * 5 + [0.25] * 4 + [1]
        for row in range(10):
            self.assertAlmostEqual(np.sum(result[row]), 
                                   expected_row_sums[row],
                                   places=5)
            
    def test_entire_backend(self):
        """
        Call the very-top level function in backend.py with a realistic
        simulation request to ensure that the entire script is working as intended.
        """
        computation_request = ComputationRequest(
            productivity_boost_from_research=1.50,
            machine_type="Electromagnetic plant",
            quality_of_production_modules="Legendary",
            number_of_productivity_modules=1,
            quality_of_quality_modules="Legendary",
            number_of_quality_modules=4,
            number_of_iterations=10,
            quality_1_count=1000,
            quality_2_count=1000,
            quality_3_count=1000,
            quality_4_count=1000)
        
        result = run_simulation(computation_request)
        
        self.assertAlmostEqual(result.quality_1_count, 0.42, places=2)
        self.assertAlmostEqual(result.quality_2_count, 2.91, places=2)
        self.assertAlmostEqual(result.quality_3_count, 10.18, places=2)
        self.assertAlmostEqual(result.quality_4_count, 24.11, places=2)
        self.assertAlmostEqual(result.quality_5_count, 6182.18, places=2)


if __name__ == '__main__':
    unittest.main()
    