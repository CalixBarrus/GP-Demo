from gp_framework.population_manager import PopulationManager, Genotype
from random import choice
from typing import List, Tuple
from gp_framework.fitness_calculator import StringPhenotypeConverter, FitnessCalculator

string_converter = StringPhenotypeConverter(11)
MUTATION_RATE = .008


class SimpleManager(PopulationManager):
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True)  # it's still in tuple form
        fittest_individual: Genotype = judged_population[0][0]
        print(string_converter.convert(fittest_individual))

        children = []

        for genotype in population:
            children.append(self.create_genotype([genotype, fittest_individual]))

        return population, children

    @staticmethod
    def create_genotype(parents: List[Genotype]) -> Genotype:
        """
        Randomly select bits of the parent Genotypes to create a new child Genotype
        :param parents: A list of all the possible parents for the child Genotype
        """
        child_byte_array = bytearray()
        for i in range(len(parents[0])):
            parent = choice(parents)
            child_byte_array.append(parent[i])
        child = Genotype(child_byte_array)
        child.mutate(MUTATION_RATE)
        return child

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        self._newest_report = self.make_LifecycleReport(children)
        return children


class MultipleChildrenManager(PopulationManager):
    def __init__(self, population: List[Genotype], fitness_calculator: FitnessCalculator, name: str):
        super().__init__(population, fitness_calculator, name)
        self._num_children = 3

    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True)  # it's still in tuple form
        fittest_individual: Genotype = judged_population[0][0]
        print(string_converter.convert(fittest_individual))

        children = []

        for genotype in population:
            children += self.produce_multiple_children([fittest_individual, genotype])

        return population, children

    def produce_multiple_children(self, parents: List[Genotype]) -> List[Genotype]:
        children = []
        for i in range(self._num_children):
            children.append(MultipleChildrenManager.create_genotype(parents))
        return children

    @staticmethod
    def create_genotype(parents: List[Genotype]) -> Genotype:
        """
        Randomly select bits of the parent Genotypes to create a new child Genotype
        :param parents: A list of all the possible parents for the child Genotype
        """
        child_byte_array = bytearray()
        for i in range(len(parents[0])):
            parent = choice(parents)
            child_byte_array.append(parent[i])
        child = Genotype(child_byte_array)
        child.mutate(MUTATION_RATE)
        return child

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        judged_population = self.calculate_population_fitness(parents + children)
        judged_population.sort(key=lambda e: e[1], reverse=True)
        next_generation = [judged_population[i][0] for i in range(int(len(judged_population) / (self._num_children + 1)))]
        self._newest_report = self.make_LifecycleReport(next_generation)
        return next_generation
