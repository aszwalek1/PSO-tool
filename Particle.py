import random
import math
import numpy as np
from itertools import permutations


# calculates distance between two given points
def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# calculates a sum of distances between cities in a tour
def calculate_tour_length(cities_positions):
    cities_positions = np.array(cities_positions)
    distances = np.linalg.norm(cities_positions - np.roll(cities_positions, -1, axis=0), axis=1)
    total_distance = np.sum(distances)
    return total_distance


class Particle:
    def __init__(self, tour, inertia_weight=0.7, cognitive_param=0.5, social_param=0.5):
        self.tour = tour[:]
        self.velocity_vector = []  # Initialise empty velocity vector
        self.p_best_tour = tour[:]  # Personal best tour initially same as current tour
        self.p_best_distance = float('inf')  # Initialise personal best distance as infinity
        # parameters
        self.inertia_weight = inertia_weight
        self.cognitive_param = cognitive_param
        self.social_param = social_param

    def initial_velocity(self):
        self.velocity_vector = [random.uniform(0, 1) for _ in range(len(self.tour))]

    def update_tour(self):
        swap_indices = []
        for i, bit in enumerate(self.velocity_vector):
            if bit == 1:
                swap_indices.append(i)

        # Copy of the current tour
        new_tour = self.tour[:]

        # Swap the cities based on the velocity vector
        for i, j in zip(swap_indices[:-1], swap_indices[1:]):
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

        new_distance = calculate_tour_length(new_tour)

        # Update the personal best tour and distance if it is better
        if new_distance < self.p_best_distance:
            self.p_best_tour = new_tour
            self.p_best_distance = new_distance

        self.tour = new_tour

        return self.p_best_tour

    def update_velocity(self, g_best_tour, p_best_tour):
        updated_velocity = []

        for i in range(len(self.tour)):
            # c1 - cognitive coefficient
            cognitive_part = random.random() * self.cognitive_param * calculate_distance(p_best_tour[i],
                                                                                         self.tour[i - 1])
            # c2 - social coefficient
            social_part = random.random() * self.social_param * calculate_distance(g_best_tour[i], self.tour[i - 1])
            inertia_part = self.inertia_weight * self.velocity_vector[i]

            velocity = cognitive_part + social_part + inertia_part

            # thresholds are problem specific
            thresholds = {5: 4, 10: 150, 15: 250, 20: 280}
            threshold = thresholds.get(len(self.tour), 200)
            if velocity > threshold:
                binary_velocity = 1
            else:
                binary_velocity = 0
            updated_velocity.append(binary_velocity)

        self.velocity_vector = updated_velocity


