from random import shuffle
from Particle import Particle as TSPParticle, calculate_tour_length  # Renamed the Particle class


class TSP_Solver:
    def __init__(self):
        self.cities_positions = []
        self.population_size = 2
        self.num_iterations = 15
        self.population = None
        self.tour = []
        self.best_g_tour = None
        self.best_tour_distance = float('inf')

    def read_cities(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                x, y = map(lambda coord: int(coord), line.split(','))
                self.cities_positions.append((x, y))
        # print(self.cities_positions)
        return self.cities_positions

    def generate_initial_tour(self):
        for _ in range(self.population_size):
            tour = self.cities_positions[:]
            shuffle(tour)
            self.tour = tour
            # print(self.tour)
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

    def run(self):
        # Initialise population
        self.population = self.initialise_population()
        self.best_g_tour = self.generate_initial_tour()
        self.best_tour_distance = float('inf')
        for particle in self.population:
            particle.initial_velocity()
            # print(particle.velocity_vector)

        for iteration in range(self.num_iterations):
            for particle in self.population:
                current_tour_distance = calculate_tour_length(particle.tour)

                if current_tour_distance < self.best_tour_distance:
                    self.best_tour_distance = current_tour_distance
                    # self.best_g_tour = particle.tour
                    # print(particle.tour)
                # print(particle.velocity_vector)
                particle.update_velocity(self.best_g_tour, particle.p_best_tour)
                # print(particle.velocity_vector)
                particle.update_tour()
                # print(particle.tour)
                # print(self.best_tour_distance, current_tour_distance)
            print(f"Iteration {iteration + 1}: Best tour distance = {self.best_tour_distance}")
        print(f"Best tour: {self.best_g_tour}")


if __name__ == '__main__':
    tsp_solver = TSP_Solver()
    tsp_solver.read_cities('csv_cities/difficulty_10.csv')
    tsp_solver.generate_initial_tour()
    tsp_solver.run()

