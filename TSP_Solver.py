from random import shuffle
from Particle import Particle as TSPParticle, calculate_tour_length  # Renamed the Particle class
import app_gui as app_gui


class TSP_Solver:
    def __init__(self, population_size=20, num_iterations=10):
        self.cities_positions = []
        self.population_size = population_size
        self.num_iterations = num_iterations
        self.population = None
        self.tour = []
        self.best_g_tour = None
        self.best_tour_distance = float('inf')

    def read_cities(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                x, y = map(lambda coord: int(coord), line.split(','))
                self.cities_positions.append((x, y))
        return self.cities_positions

    def generate_initial_tour(self):
        for _ in range(self.population_size):
            tour = self.cities_positions[:]
            shuffle(tour)
            self.tour = tour
        return self.tour

    def update_tour(self):
        for particle in self.population:
            particle.update_tour()

    def initialise_population(self):
        population = []
        for _ in range(self.population_size):
            initial_tours = self.generate_initial_tour()
            particle = TSPParticle(initial_tours)
            population.append(particle)
        return population

    def check_stopping_condition(self, previous_best_distances, stopping_margin):
        if all(abs(self.best_tour_distance - distance) <= stopping_margin for distance in previous_best_distances):
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
        previous_best_distances = [float('inf')] * 2

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

                if self.check_stopping_condition(previous_best_distances, stopping_margin):
                    return self.best_g_tour
            print(f"Iteration {iteration + 1}: Best tour distance = {self.best_tour_distance}")
            print(f"Best tour: {self.best_g_tour}")


if __name__ == '__main__':
    tsp_solver = TSP_Solver()
    tsp_solver.read_cities('csv_cities/difficulty_5.csv')
    tsp_solver.generate_initial_tour()
    # tsp_solver.run()
    app_gui.run_gui()

