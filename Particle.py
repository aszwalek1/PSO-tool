import math
import random

import numpy as np


# Calculate distance between two given points
def calculate_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


# Calculate a sum of distances between cities in a tour
def calculate_tour_length(cities_positions):
    cities_positions = np.array(cities_positions)
    distances = np.linalg.norm(cities_positions - np.roll(cities_positions, -1, axis=0), axis=1)
    total_distance = np.sum(distances)
    return total_distance


class Particle:
    def __init__(self, tour, inertia_weight=0.5, cognitive_param=0.5, social_param=0.5):
        self.tour = tour[:]
        self.velocity_vector = []  # Initialise empty velocity vector
        self.p_best_tour = tour[:]  # Personal best tour initially same as current tour
        self.p_best_distance = float('inf')  # Initialise personal best distance as infinity
        # parameters
        self.inertia_weight = inertia_weight
        self.cognitive_param = cognitive_param
        self.social_param = social_param

    # Initialise  velocity as a vector with binary values assigned randomly
    def initial_velocity(self):
        self.velocity_vector = [1 if random.random() < 0.5 else 0 for _ in range(len(self.tour))]

    # ----------------- VERSION 1 - calculates tour length after all swaps are performed ----------------
    # def update_tour(self):
    #     swap_indices = [i for i, bit in enumerate(self.velocity_vector) if bit == 1]
    #
    #     # Copy of the current tour
    #     new_tour = self.tour[:]
    #
    #     # Swap the cities based on the velocity vector
    #     for i, j in zip(swap_indices[:-1], swap_indices[1:]):
    #         new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
    #
    #     # Calculate the length of the new tour after all the swaps have been performed
    #     new_distance = calculate_tour_length(new_tour)
    #
    #     # Update the personal best tour and distance if it is better
    #     if new_distance < self.p_best_distance:
    #         self.p_best_tour = new_tour
    #         self.p_best_distance = new_distance
    #
    #     self.tour = new_tour
    #
    #     return self.p_best_tour

    # ---------------  VERSION 2 - calculates length after each swap ------------------------
    def update_tour(self):
        swap_indices = [i for i, bit in enumerate(self.velocity_vector) if bit == 1]

        # Copy of the current tour
        new_tour = self.tour[:]
        best_tour = self.p_best_tour  # Initialize best_tour with personal best tour
        best_distance = self.p_best_distance  # Initialize best_distance with personal best distance

        # Perform one swap at the time and compare the new tour with current best
        for i, j in zip(swap_indices[:-1], swap_indices[1:]):
            # Create a copy of the tour for each swap
            current_tour = new_tour[:]
            current_tour[i], current_tour[j] = current_tour[j], current_tour[i]

            # Calculate the distance of the current tour
            current_distance = calculate_tour_length(current_tour)

            # Check if the current tour is better than the best tour found so far
            if current_distance < self.p_best_distance:
                best_tour = current_tour
                best_distance = current_distance

        # Update the personal best tour and distance if a better tour is found
        if best_distance < self.p_best_distance:
            self.p_best_tour = best_tour
            self.p_best_distance = best_distance

        # Update the tour with the best tour found
        self.tour = best_tour

        return self.p_best_tour

    def update_velocity(self, g_best_tour, p_best_tour):
        updated_velocity = []

        for i in range(len(self.tour)):
            # c1 - cognitive coefficient
            # Needs to be divided to scale down to range around (0, 1)
            cognitive_part = random.random() * self.cognitive_param * (calculate_distance(p_best_tour[i],
                                                                                          self.tour[i - 1]) / 1000)

            # c2 - social coefficient
            social_part = random.random() * self.social_param * (calculate_distance(g_best_tour[i],
                                                                                    self.tour[i - 1]) / 1000)

            velocity = cognitive_part + social_part + self.inertia_weight

            # Translate velocity to binary values
            if velocity > 0.75:
                binary_velocity = 1
            else:
                binary_velocity = 0
            updated_velocity.append(binary_velocity)

        self.velocity_vector = updated_velocity
