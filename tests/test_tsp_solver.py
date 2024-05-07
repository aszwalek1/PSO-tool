import unittest
from hamcrest import assert_that, equal_to, has_length
from TSP_Solver import TSP_Solver
import os


class TestTSPSolver(unittest.TestCase):
    def setUp(self):
        self.tsp_solver = TSP_Solver(population_size=10, num_iterations=10)

        current_directory = os.path.dirname(__file__)
        os.chdir(current_directory)

        self.cities = self.tsp_solver.read_cities('test1.csv')
        self.tsp_solver.run()

    def test_read_cities(self):
        # Test that the cities are read
        expected_number_of_cities = 8
        assert_that(self.cities, has_length(expected_number_of_cities))

    def test_generate_initial_tour(self):
        # Test generating initial tour
        tour = self.tsp_solver.generate_initial_tour()
        expected_tour_length = 8
        assert_that(tour, has_length(expected_tour_length))

    def test_initialise_population(self):
        # Test initialising the population of particles
        population = self.tsp_solver.initialise_population()
        expected_population_size = 10
        assert_that(population, has_length(expected_population_size))


if __name__ == '__main__':
    unittest.main()
