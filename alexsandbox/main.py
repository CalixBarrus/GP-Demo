from typing import Tuple
from gp_demo.gp_framework import *

def search_for_phenotype(target_phenotype: str, max_iterations: int, population: List[Genotype], fitness_calculator: FitnessCalculator) -> Tuple[str, int, int]:
    best_string = ""
    best_string_fitness = 0
    iterations = 0
    target_fitness = fitness_calculator.calculate_fitness(target_phenotype, [target_phenotype])
    genotype = population[0]

    print("Starting phenotype:", genotype.to_string())
    print("Target Fitness:", target_fitness)

    while iterations < max_iterations and best_string_fitness < target_fitness:
        genotype.mutate(.2)
        phenotype = genotype.to_string()
        fitness = fitness_calculator.calculate_fitness(phenotype, [target_phenotype])
        # print("phenotype:", genotype.to_string(), "fitness:", fitness)
        if fitness > best_string_fitness:
            best_string = phenotype
            best_string_fitness = fitness
            print("New best:", phenotype, "with fitness:", best_string_fitness, "after", iterations, "iterations")
        iterations += 1

    return (best_string, best_string_fitness, iterations)

def main():
    genotype = Genotype(bytearray([0x4a, 0x4b, 0x4c, 0x4d]))
    fitness_calculator = create_FitnessCalculator(Application.STRING_MATCH)

    search_results = []
    for i in range(100):
        print("\n\nBeginning search {}.".format(i))
        search_results.append(search_for_phenotype("asdf", 1_000_000, [genotype], fitness_calculator))

    for result in search_results:
        print(result)


main()
