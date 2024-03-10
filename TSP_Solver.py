import math
from random import shuffle


def calculate_distance(city1, city2):
    return math.dist(city1, city2)


class TSP_Solver:
    def __init__(self):
        self.num_cities = 0
        self.cities_positions = []
        self.indexed_cities = []
        self.population_size = []
        self.num_iterations = 0
        self.population = None

    def read_cities(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                x, y = map(lambda coord: int(coord), line.split(','))
                self.cities_positions.append((x, y))
            print(self.cities_positions)
        return self.cities_positions

    def generate_initial_tour(self):
        shuffle(self.cities_positions)
        print(self.cities_positions)

    def calculate_velocity(self):
        pass

    def update_velocities(self):
        pass


if __name__ == '__main__':
    tsp_solver = TSP_Solver()
    tsp_solver.read_cities('csv_cities/difficulty_5.csv')
    tsp_solver.generate_initial_tour()
