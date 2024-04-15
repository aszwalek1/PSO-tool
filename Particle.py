import random
import math
import numpy as np
from itertools import permutations


def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def calculate_tour_length(cities_positions):
    cities_positions = np.array(cities_positions)
    distances = np.linalg.norm(cities_positions - np.roll(cities_positions, -1, axis=0), axis=1)
    total_distance = np.sum(distances)
    return total_distance


def logistic_transformation(x):
    return 1 / (1 + np.exp(-x))


class Particle:
    def __init__(self, tour, inertia_weight=0.01, cognitive_param=0.01, social_param=0.01):
        self.tour = tour[:]
        self.velocity_vector = []  # Initialise empty, to be populated later
        self.p_best_tour = tour[:]  # Personal best tour initially same as current tour
        self.p_best_distance = float('inf')  # Initialise personal best distance as infinity
        # parameters
        self.inertia_weight = inertia_weight
        self.cognitive_param = cognitive_param
        self.social_param = social_param

    def initial_velocity(self):
        self.velocity_vector = [random.uniform(0, 1) for _ in range(len(self.tour))]

    def update_tour(self):
        swap_indices = [i for i, bit in enumerate(self.velocity_vector) if bit == 1]

        # Generate all possible permutations of swap indices
        permuted_indices = list(permutations(swap_indices))

        # Evaluate the tour distance for each permutation
        best_tour = self.tour[:]
        best_distance = calculate_tour_length(best_tour)

        for indices in permuted_indices:
            # Copy the current tour
            new_tour = best_tour[:]
            # Swap the cities based on permutation
            for i, j in zip(indices[:-1], indices[1:]):
                new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
            # Calculate the new distance of a tour
            new_distance = calculate_tour_length(new_tour)
            # Update the best tour and distance if it is better
            if new_distance < best_distance:
                best_tour = new_tour
                best_distance = new_distance
                self.p_best_tour = best_tour

        self.tour = best_tour
        return self.tour

    def update_velocity(self, g_best_tour, p_best_tour):
        updated_velocity = []

        for i in range(len(self.tour)):
            # c1 - cognitive coefficient
            cognitive_part = random.random() * self.cognitive_param * calculate_distance(p_best_tour[i], self.tour[i-1])
            # c2 - social coefficient
            social_part = random.random() * self.social_param * calculate_distance(g_best_tour[i], self.tour[i-1])
            inertia_part = self.inertia_weight * self.velocity_vector[i]

            velocity = cognitive_part + social_part + inertia_part

            if velocity > 1:
                updated_velocity.append(1)
            elif velocity < 1:
                updated_velocity.append(0)
            else:
                updated_velocity.append(random.uniform(0, 1))
            # print(cognitive_part, social_part, inertia_part)

        self.velocity_vector = updated_velocity

