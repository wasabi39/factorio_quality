import numpy as np
#IMPORTANT: Quality and production chips are numbered from 1 to 5, with 1 being the worst and 5 being the best.
#Do not use 0-indexed numbers for the quality and production chips.
#The math used in this code is mainly theory about Markov chains, see https://www.probabilitycourse.com/chapter11/11_2_1_introduction.php
#Productivity boost refers to the percentage *added* to the productivity of the machine.
#So a productivity boost of 1.2 means that machine produces 120% *EXTRA* items compared to the base machine.
#Same thing goes for quality boost.

def get_quality_chip_score():
    return [0.025, 0.032, 0.04, 0.047, 0.062]

def get_productivity_chip_score():
    return [0.1, 0.13, 0.16, 0.19, 0.25]

def get_productivity_research_boost():
    return 1.2

def calculate_productivity_boost(number_of_productivity_chips=0, type_of_productivity_chip=5, recycling=False, fifty_percent_boost=False):
    if recycling:
        return -0.75 #recyclers always destroy 75% of the input, which is effectively a -75% productivity boost
    productivity_boost_from_chips = number_of_productivity_chips * get_productivity_chip_score()[type_of_productivity_chip - 1]
    productivity_boost = get_productivity_research_boost() + productivity_boost_from_chips + 0.5 * fifty_percent_boost
    return min(productivity_boost, 3) #productivity boost is capped at +300%

def calculate_quality_boost(number_of_quality_chips=5, type_of_quality_boost=5):
    quality_boost_from_chips = number_of_quality_chips * get_quality_chip_score()[type_of_quality_boost - 1]
    return quality_boost_from_chips

def get_probabilities_of_upgrading_by_number_of_tiers(productivity_boost=1, quality_boost=1):
    #See https://wiki.factorio.com/Quality for information on how the probabilities are calculated.
    #The first element is the probability of not upgrading, the second is the probability of upgrading by 1 tier, etc.
    return [
        (1 + productivity_boost) * (1 - quality_boost),
        (1 + productivity_boost) * quality_boost * 9 / 10,
        (1 + productivity_boost) * quality_boost * 9 / 100,
        (1 + productivity_boost) * quality_boost * 9 / 1000,
        (1 + productivity_boost) * quality_boost * 1 / 1000
    ]


def get_part_of_transition_matrix(productivity_boost, quality_boost, recycling=False):
    if recycling:
        productivity_boost = -0.75
    probabilities = get_probabilities_of_upgrading_by_number_of_tiers(productivity_boost, quality_boost)
    #Key difference: We don't recycle legendary items, so we set the probability of producing a legendary item from a legendary item to 0
    if recycling:
        return np.array([[probabilities[0], probabilities[1], probabilities[2], probabilities[3], 1 + productivity_boost - np.sum(probabilities[0:4])],
                        [0, probabilities[0], probabilities[1], probabilities[2], 1 + productivity_boost - np.sum(probabilities[0:3])],
                        [0, 0, probabilities[0], probabilities[1], 1 + productivity_boost - np.sum(probabilities[0:2])],
                        [0, 0, 0, probabilities[0], 1 + productivity_boost - probabilities[0]],
                        [0, 0, 0, 0, 0]])    
    return np.array([[probabilities[0], probabilities[1], probabilities[2], probabilities[3], 1 + productivity_boost - np.sum(probabilities[0:4])],
                    [0, probabilities[0], probabilities[1], probabilities[2], 1 + productivity_boost - np.sum(probabilities[0:3])],
                    [0, 0, probabilities[0], probabilities[1], 1 + productivity_boost - np.sum(probabilities[0:2])],
                    [0, 0, 0, probabilities[0], 1 + productivity_boost - probabilities[0]],
                    [0, 0, 0, 0, 1 + productivity_boost]])    

def concatenate_transition_matrices(upper_left_of_transition_matrix, upper_right_of_transition_matrix, lower_left_of_transition_matrix, bottom_right_of_transition_matrix):
    return np.concatenate(
        (np.concatenate((upper_left_of_transition_matrix, upper_right_of_transition_matrix), axis=1),
        np.concatenate((lower_left_of_transition_matrix, bottom_right_of_transition_matrix), axis=1)),
        axis=0
    )

def generate_transition_matrix():
    #See https://wiki.factorio.com/Quality for information on how the transition matrix is constructed.
    upper_left_of_transition_matrix = np.array([
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0]])
    bottom_right_of_transition_matrix = np.array([
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,0],
                          [0,0,0,0,1]])
    
    productivity_boost_for_assembly = calculate_productivity_boost(number_of_productivity_chips=0, type_of_productivity_chip=5,recycling=False, fifty_percent_boost=True)
    quality_boost_for_assembly = calculate_quality_boost(number_of_quality_chips=5, type_of_quality_boost=5)

    upper_right_of_transition_matrix = get_part_of_transition_matrix(productivity_boost_for_assembly, quality_boost_for_assembly, recycling=False)

    productivity_boost_for_recycling = calculate_productivity_boost(recycling=True, fifty_percent_boost=False)
    quality_boost_for_recycling = calculate_quality_boost(number_of_quality_chips=4, type_of_quality_boost=5)

    lower_left_of_transition_matrix = get_part_of_transition_matrix(productivity_boost_for_recycling, quality_boost_for_recycling, recycling=True)

    transition_matrix = concatenate_transition_matrices(upper_left_of_transition_matrix, upper_right_of_transition_matrix, lower_left_of_transition_matrix, bottom_right_of_transition_matrix)
    return transition_matrix

def calculate_iterations(number_of_iterations=1):
    transition_matrix = generate_transition_matrix()
    starting_distribution = np.array([1,0,0,0,0,0,0,0,0,0])
    #IMPORTANT: A full cycle is 2 iterations, because the assembly machine and the recycling machine are in a cycle. So we lift the maftrix to the power of 2 * number_o_iterations.
    final_distribution = starting_distribution @ np.linalg.matrix_power(transition_matrix, 2 * number_of_iterations)
    #Note: Entry 0 in our distribution is the percentage of quality 1 items that just left the recycling machine,
    #entry 5 is the percentage of quality of 1 items that just left the assembly machine.
    #We add those together to get the total number of quality 1 items. Similarly for the other qualities.
    final_distribution_summarized = np.array([final_distribution[0] + final_distribution[5],
                                   final_distribution[1] + final_distribution[6],
                                   final_distribution[2] + final_distribution[7],
                                   final_distribution[3] + final_distribution[8],
                                   final_distribution[4] + final_distribution[9]])
    return final_distribution_summarized

np.set_printoptions(suppress=True)
print(calculate_iterations(number_of_iterations=10))
#print(generate_transition_matrix())