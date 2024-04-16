from random import shuffle
from Particle import Particle as Particle, calculate_tour_length  # Renamed the Particle class
import app_gui as app_gui


class TSP_Solver:
    def __init__(self, population_size=120, num_iterations=500):
        self.cities_positions = []
        self.population_size = population_size
        self.num_iterations = num_iterations
        self.population = None
        self.tour = []
        self.best_g_tour = None
        self.best_tour_distance = float('inf')

    # Read in the csv files with city coordinates
    def read_cities(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                x, y = map(lambda coord: int(coord), line.split(','))
                self.cities_positions.append((x, y))
        return self.cities_positions

    # generate an initial tour for each particle
    def generate_initial_tour(self):
        for _ in range(self.population_size):
            tour = self.cities_positions[:]
            shuffle(tour)
            self.tour = tour
        return self.tour

    # initialise a population of particles
    def initialise_population(self):
        population = []
        for _ in range(self.population_size):
            initial_tours = self.generate_initial_tour()
            particle = Particle(initial_tours)
            population.append(particle)
        return population

    # check if there is changed compared to a number of previous iterations
    def check_stopping_condition(self, previous_best_distances, stopping_margin, number_of_iterations_for_stopping):
        # check if the number of previous distances is at least as large as the number
        # of iterations specified for stopping condition
        # and check if the new distance is within the stopping margin to the previous best distance
        if len(previous_best_distances) >= number_of_iterations_for_stopping and \
                all(abs(self.best_tour_distance - distance) <= stopping_margin for distance in previous_best_distances):
            print("Stopping condition reached: Convergence achieved.")
            print(f"Best tour: {self.best_g_tour}")
            return True
        return False

    def run(self):
        # Initialise population
        self.population = self.initialise_population()
        self.best_g_tour = self.generate_initial_tour()
        self.best_tour_distance = float('inf')
        stopping_margin = 0.0000000001
        # how many previous iterations to compare for stopping criterion
        number_of_iterations_for_stopping = 50
        previous_best_distances = [float('inf')] * number_of_iterations_for_stopping

        for particle in self.population:
            particle.initial_velocity()

        for iteration in range(self.num_iterations):
            previous_best_distances.pop(0)
            previous_best_distances.append(self.best_tour_distance)
            for particle in self.population:
                current_tour_distance = calculate_tour_length(particle.tour)

                if current_tour_distance < self.best_tour_distance:
                    self.best_tour_distance = current_tour_distance
                    self.best_g_tour = particle.tour

                particle.update_velocity(self.best_g_tour, particle.p_best_tour)
                particle.update_tour()

                if self.check_stopping_condition(previous_best_distances, stopping_margin, number_of_iterations_for_stopping):
                    return self.best_g_tour
            print(f"Iteration {iteration + 1}: Best tour distance = {self.best_tour_distance}")
            print(f"Best tour: {self.best_g_tour}")


if __name__ == '__main__':
    tsp_solver = TSP_Solver()
    tsp_solver.read_cities('csv_cities/difficulty_20.csv')
    tsp_solver.generate_initial_tour()
    app_gui.run_gui()

