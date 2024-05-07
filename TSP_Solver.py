from random import shuffle
from Particle import Particle as Particle, calculate_tour_length


class TSP_Solver:
    def __init__(self, population_size=50, num_iterations=50):
        self.cities_positions = []
        self.population_size = population_size
        self.num_iterations = num_iterations
        self.population = None
        self.tour = []
        self.g_best_tour = None
        self.g_best_distance = float('inf')

    # Read in the csv files with city coordinates
    def read_cities(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                x, y = map(lambda coord: int(coord), line.split(','))
                self.cities_positions.append((x, y))
        return self.cities_positions

    # Generate an initial tour for each particle
    def generate_initial_tour(self):
        tours = [self.cities_positions[:] for _ in range(self.population_size)]
        for tour in tours:
            shuffle(tour)
            self.tour = tour
        return self.tour

    # Initialise a population of particles
    def initialise_population(self):
        return [Particle(self.generate_initial_tour()) for _ in range(self.population_size)]

    # Check if there is a change compared to a number of previous iterations
    def check_stopping_condition(self, previous_best_distances, stopping_margin, number_of_iterations_for_stopping):
        # Check if the number of previous distances is at least as large as the number
        # of iterations specified for stopping condition
        # and check if the new distance is within the stopping margin to the previous best distance
        if len(previous_best_distances) >= number_of_iterations_for_stopping and \
                all(abs(self.g_best_distance - distance) <= stopping_margin for distance in previous_best_distances):
            print("Stopping condition reached: Convergence achieved.")
            print(f"Best tour: {self.g_best_tour}")
            print(f"Best distance: {self.g_best_distance}")
            return True
        return False

    def run(self):
        # Initialise population
        self.population = self.initialise_population()
        # Initialise best global tour
        self.g_best_tour = self.generate_initial_tour()
        # Initialise best tour distance
        self.g_best_distance = float('inf')
        # Margin for stopping condition
        stopping_margin = 0.0000000001
        # How many previous iterations to compare for stopping criterion
        num_of_iterations_for_stop = 50
        previous_best_distances = [self.g_best_distance] * num_of_iterations_for_stop

        for particle in self.population:
            particle.initial_velocity()
        for iteration in range(self.num_iterations):
            # Update previous best distances
            previous_best_distances.pop(0)
            previous_best_distances.append(self.g_best_distance)
            for particle in self.population:
                current_tour_distance = calculate_tour_length(particle.tour)
                # If the current tour is better than the best global tour than replace it
                if current_tour_distance < self.g_best_distance:
                    self.g_best_distance = current_tour_distance
                    self.g_best_tour = particle.tour

                particle.update_velocity(self.g_best_tour, particle.p_best_tour)
                particle.update_tour()

                if self.check_stopping_condition(previous_best_distances, stopping_margin, num_of_iterations_for_stop):
                    return self.g_best_tour
            print(f"Iteration {iteration + 1}: Best tour distance = {self.g_best_distance}")
            print(f"Best tour: {self.g_best_tour}")
            print(f"Best distance: {self.g_best_distance}")

