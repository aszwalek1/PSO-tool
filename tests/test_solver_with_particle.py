import unittest
from TSP_Solver import TSP_Solver

class IntegrationTest(unittest.TestCase):
    def setUp(self):
        # Initialize a TSP Solver instance
        self.tsp_solver = TSP_Solver()

    def test_solver_initialisation(self):
        self.assertIsNotNone(self.tsp_solver)

    def test_solver_run(self):
        self.tsp_solver.read_cities('test1.csv')
        self.tsp_solver.generate_initial_tour()
        self.tsp_solver.run()

    # Add more integration tests as needed

if __name__ == '__main__':
    unittest.main()
