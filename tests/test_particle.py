import unittest
import random
from hamcrest import assert_that, close_to, equal_to
from Particle import Particle, calculate_distance, calculate_tour_length
from unittest.mock import patch


class TestParticle(unittest.TestCase):

    def test_calculate_distance(self):
        city1 = (120, 450)
        city2 = (132, 560)
        expected_distance = 110.65260954898
        actual_distance = calculate_distance(city1, city2)
        assert_that(actual_distance, close_to(expected_distance, delta=0.0001))

    def test_tour_length(self):
        cities_positions = [(579, 782), (237, 609), (576, 579), (543, 317), (881, 179)]
        expected_tour_length = 2027.1456787510542
        actual_tour_length = calculate_tour_length(cities_positions)
        assert_that(actual_tour_length, close_to(expected_tour_length, delta=0.0001))

    def test_initial_velocity(self):
        # test random using seed
        seed = 10
        random.seed(seed)
        tour_length = 5
        # create an instance of Particle
        particle = Particle([0] * tour_length)
        particle.initial_velocity()
        expected_velocity_vector = [0, 1, 0, 1, 0]
        # check that the vector is the same length as the tour
        assert_that(len(particle.velocity_vector), equal_to(tour_length))
        # check that the velocity vector is the same as expected
        assert_that(particle.velocity_vector, equal_to(expected_velocity_vector))

    @patch('Particle.calculate_tour_length')
    def test_update_tour(self, mock_calculate_tour_length):
        # Specify the mock return values for calculate_tour_length
        mock_calculate_tour_length.side_effect = [84.85281, 56.56854, 100]

        # Create a particle instance
        city_coordinates = [(30, 40), (10, 20), (50, 60)]
        particle_instance = Particle(city_coordinates)

        # Set the particle's velocity vector and personal best tour
        particle_instance.velocity_vector = [1, 1, 0]
        particle_instance.p_best_tour = city_coordinates

        # Call the method for the test
        particle_instance.update_tour()

        # Define the expected tour
        expected_tour = [(10, 20), (30, 40), (50, 60)]

        # Assert that the tour and personal best tour are the same
        assert_that(particle_instance.tour, equal_to(expected_tour))
        assert_that(particle_instance.p_best_tour, equal_to(expected_tour))

    @patch('Particle.random')
    def test_update_velocity(self, mock_random):
        mock_random.random.return_value = 0.5

        # Initialise a Particle instance
        city_coordinates = [(30, 40), (10, 20), (50, 60)]
        particle_instance = Particle(city_coordinates)

        # Define the parameters
        g_best_tour = [(0, 0), (1, 1), (2, 2)]
        p_best_tour = [(3, 3), (4, 4), (5, 5)]
        particle_instance.cognitive_param = 0.5
        particle_instance.social_param = 0.5
        particle_instance.inertia_weight = 0.5

        # Call the method
        particle_instance.update_velocity(g_best_tour, p_best_tour)

        # Assert that the velocity vector is as expected
        expected_velocity = [0, 0, 0]
        assert_that(particle_instance.velocity_vector, equal_to(expected_velocity))


if __name__ == '__main__':
    unittest.main()
