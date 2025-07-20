import unittest
import numpy as np
from src.ml_visualization.cost_functions import compute_cost

class TestCostFunctions(unittest.TestCase):

    def test_compute_cost(self):
        # Test case 1: Simple linear relationship
        x = np.array([1, 2, 3])
        y = np.array([2, 4, 6])
        w = 2
        b = 0
        expected_cost = 0.0  # Perfect prediction
        cost = compute_cost(x, y, w, b)
        self.assertAlmostEqual(cost, expected_cost, places=5)

        # Test case 2: Linear relationship with some error
        x = np.array([1, 2, 3])
        y = np.array([2, 5, 6])
        w = 2
        b = 0
        expected_cost = 1.0  # (0^2 + 1^2 + 0^2) / 2 = 1.0
        cost = compute_cost(x, y, w, b)
        self.assertAlmostEqual(cost, expected_cost, places=5)

        # Test case 3: Different weights and bias
        x = np.array([1, 2, 3])
        y = np.array([1, 2, 3])
        w = 1
        b = 1
        expected_cost = 0.0  # Perfect prediction
        cost = compute_cost(x, y, w, b)
        self.assertAlmostEqual(cost, expected_cost, places=5)

if __name__ == '__main__':
    unittest.main()