"""
IMPORTANT: Quality and production chips are numbered from 1 to 5, 
with 1 being the worst and 5 being the best.
Do not use 0-indexed numbers for the quality and production chips.
The math used in this code is mainly theory about Markov chains, 
see https://www.probabilitycourse.com/chapter11/11_2_1_introduction.php
Productivity boost refers to the percentage *added* to the productivity of the machine.
So a productivity boost of 1.2 means that machine produces 120% *EXTRA* items 
compared to the base machine. Same thing goes for quality boost.
"""


import numpy as np
from backend.result_request import ResultRequest
from frontend.computation_request import ComputationRequest

def get_quality_chip_score():
    """
    Returns a list of quality boosts for each type of quality chip.
    Order is from worst to best.
    """
    return [0.025, 0.032, 0.04, 0.047, 0.062]

def get_productivity_chip_score():
    """
    Returns a list of productivity boosts for each type of productivity chip.
    Order is from worst to best.
    """
    return [0.1, 0.13, 0.16, 0.19, 0.25]

def calculate_productivity_boost(number_of_productivity_chips=0, 
                                 type_of_productivity_chip=5, 
                                 recycling=False, 
                                 fifty_percent_boost=False, 
                                 research_boost=0):
    """
    Calculates the total productivity boost from prod chips, research etc.
    """
    if recycling:
        #Recyclers always destroy 75% of the input, 
        #which is effectively a -75% productivity boost.
        return -0.75
    prod_boost_from_chips = (number_of_productivity_chips * 
                             get_productivity_chip_score()[type_of_productivity_chip - 1])
    prod_boost = research_boost + prod_boost_from_chips + 0.5 * fifty_percent_boost
    return min(prod_boost, 3) #productivity boost is capped at +300%

def calculate_quality_boost(number_of_quality_chips=5, type_of_quality_boost=5):
    """
    Returns the quality boost from quality chips.
    """
    quality_boost_from_chips = (number_of_quality_chips * 
                                get_quality_chip_score()[type_of_quality_boost - 1])
    return quality_boost_from_chips

def get_probabilities_of_upgrading(productivity_boost=1, quality_boost=1):
    """
    Returns a list of probabilities of upgrading by 0, 1, 2, 3 or 4 tiers.
    """
    #See https://wiki.factorio.com/Quality 
    #for information on how the probabilities are calculated.
    return [
        (1 + productivity_boost) * (1 - quality_boost),
        (1 + productivity_boost) * quality_boost * 9 / 10,
        (1 + productivity_boost) * quality_boost * 9 / 100,
        (1 + productivity_boost) * quality_boost * 9 / 1000,
        (1 + productivity_boost) * quality_boost * 1 / 1000
    ]

def get_part_of_transition_matrix(productivity_boost, quality_boost, recycling=False):
    """
    Returns upper right of the transition matrix if recycling is False,
    otherwise returns lower left of the transition matrix.
    """
    if recycling:
        productivity_boost = -0.75
    prob = get_probabilities_of_upgrading(productivity_boost, quality_boost)

    base_matrix = [
        [prob[0], prob[1], prob[2], prob[3], 1 + productivity_boost - np.sum(prob[0:4])],
        [0, prob[0], prob[1], prob[2], 1 + productivity_boost - np.sum(prob[0:3])],
        [0, 0, prob[0], prob[1], 1 + productivity_boost - np.sum(prob[0:2])],
        [0, 0, 0, prob[0], 1 + productivity_boost - prob[0]],
        [0, 0, 0, 0, 1 + productivity_boost]
    ]

    if recycling:
        #We don't recycle legendary items, so when recycling we set
        #the probability of producing a legendary item from legendary ingredients to 0.
        base_matrix[-1] = [0, 0, 0, 0, 0]
    
    return np.array(base_matrix)    

def concatenate_transition_matrices(upper_left, 
                                    upper_right, 
                                    lower_left, 
                                    bottom_right):
    """
    Concatenates the four parts of the transition matrix into one matrix.
    """
    return np.concatenate(
        (np.concatenate((upper_left, upper_right), axis=1),
        np.concatenate((lower_left, bottom_right), axis=1)),
        axis=0
    )

def get_upper_left_of_transition_matrix():
    """
    Returns the upper left of the transition matrix, which is always the same.
    """
    return np.array([
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0]
    ])

def get_bottom_right_of_transition_matrix():
    """
    Returns the bottom right of the transition matrix, which is always the same.
    """
    return np.array([
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,0],
        [0,0,0,0,1]
    ])

def is_electromagnetic_plant(machine_type: str) -> bool:
    """
    Returns True if the machine type is an electromagnetic plant, False otherwise.
    """
    return machine_type == "Electromagnetic plant"

def chip_type_to_number(chip_type: str) -> int:
    """
    Returns the number of the chip type (1-5).
    """
    #The .index method will throw a value exception if the chip type is not found,
    #but the frontend should ensure that the chip type is valid.
    return ["Normal", "Uncommon", "Rare", "Epic", "Legendary"].index(chip_type) + 1

def generate_transition_matrix(computation_request: ComputationRequest):
    """
    Returns the transition matrix for the Markov chain.
    """
    #See https://wiki.factorio.com/Quality for information on how 
    #the transition matrix is constructed.
    upper_left = get_upper_left_of_transition_matrix()
    bottom_right = get_bottom_right_of_transition_matrix()
    
    productivity_boost_assembly = calculate_productivity_boost(
        number_of_productivity_chips=computation_request.number_of_productivity_modules,
        type_of_productivity_chip=chip_type_to_number(
                                        computation_request.quality_of_production_modules), 
        recycling=False, 
        fifty_percent_boost=is_electromagnetic_plant(computation_request.machine_type),
        research_boost=computation_request.productivity_boost_from_research)
    qual_boost_assembly = calculate_quality_boost(number_of_quality_chips=
                                                 computation_request.number_of_quality_modules,
                                                 type_of_quality_boost=chip_type_to_number(
                                                 computation_request.quality_of_quality_modules))

    upper_right = get_part_of_transition_matrix(productivity_boost_assembly, 
                                                qual_boost_assembly, 
                                                recycling=False)

    productivity_boost_for_recycling = calculate_productivity_boost(
                                                                    recycling=True, 
                                                                    fifty_percent_boost=False)
    #I've chosen to hardcode the recycling step, since noone will realistically
    #want to experiment with it.
    quality_boost_for_recycling = calculate_quality_boost(
                                                    number_of_quality_chips=4, 
                                                    type_of_quality_boost=5)

    lower_left = get_part_of_transition_matrix(productivity_boost_for_recycling, 
                                               quality_boost_for_recycling, 
                                               recycling=True)

    transition_matrix = concatenate_transition_matrices(upper_left, 
                                                        upper_right, 
                                                        lower_left, 
                                                        bottom_right)
    
    return transition_matrix

def get_starting_distribution(computation_request: ComputationRequest) -> np.array:
    """
    Returns the starting distribution for the Markov chain.
    """
    #The starting distribution is the number of items of each quality
    #that the user starts out with.
    return np.array([computation_request.quality_1_count,
                     computation_request.quality_2_count,
                     computation_request.quality_3_count,
                     computation_request.quality_4_count,
                     0, 0, 0, 0, 0, 0])

def calculate_result_request(distribution: np.array) -> ResultRequest:
    """
    Returns the expected number of items of each quality after a number of iterations.
    """
    #Entry 0 in our distribution is the number of quality 1 items
    #that just left the recycling machine. Entry 5 is the number of quality 
    #1 items that just left the assembly machine.
    #We add those together to get the total number of quality 1 items. 
    #Similarly for the other qualities.
    #Final entry is the number of legendary items produced in total,
    #since we don't recycle legendary items.
    decimals = 2 #Number of decimals to round to.
    return ResultRequest(quality_1_count=round(distribution[0] + distribution[5], decimals),
                         quality_2_count=round(distribution[1] + distribution[6], decimals),
                         quality_3_count=round(distribution[2] + distribution[7], decimals),
                         quality_4_count=round(distribution[3] + distribution[8], decimals),
                         quality_5_count=round(distribution[4] + distribution[9], decimals))

def calculate_iterations(iterations: int, 
                         transition_matrix: np.array, 
                         starting_distribution: np.array) -> ResultRequest:
    """
    Returns the expected number of items of each quality after a number of iterations.
    """
    #IMPORTANT: A full cycle is 2 iterations, 
    #because the assembly machine and the recycling machine are in a cycle. 
    # So we lift the matrix to the power of 2 * number_of_iterations.
    distribution = starting_distribution @ \
        np.linalg.matrix_power(transition_matrix, 2 * iterations)
    result_request = calculate_result_request(distribution)
    return result_request

def run_simulation(computation_request: ComputationRequest) -> ResultRequest:
    """
    Runs the simulation and returns the result.
    """
    transition_matrix = generate_transition_matrix(computation_request)
    starting_distribution = get_starting_distribution(computation_request)
    return calculate_iterations(computation_request.number_of_iterations, 
                                transition_matrix,
                                starting_distribution)

