from operator import itemgetter
from typing import Tuple
from gp_demo.gp_framework import *
from gp_demo.PopulationManager import *


class MyManager(PopulationManager):

    def produce_offspring(self, population: List[Tuple[Genotype, int]]) -> List[Genotype]:
        children = []
        fittest_individual = max(population, key=itemgetter(1))[0]
        for _ in range(len(population)):
            child = fittest_individual
            child.mutate(.1)
            children.append(child)

        return children

    def select_next_generation(self, parents: List[Tuple[Genotype, int]], children: List[Genotype]) -> List[Genotype]:
        return children


def main():
    starting_population = [generate_random_genotype(4) for _ in range(3)]
    fitness_calculator = create_FitnessCalculator(Application.STRING_MATCH)
    manager3 = MyManager([generate_random_genotype(4) for _ in range(3)], fitness_calculator)
    manager10 = MyManager([generate_random_genotype(4) for _ in range(10)])


main()
