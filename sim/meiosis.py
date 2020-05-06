import math

from gp_framework.population_manager import PopulationManager, Genotype
from gp_framework.fitness_calculator import StringPhenotypeConverter, FitnessCalculator
from gp_framework.genotype import generate_random_population
from random import choice, randint
from typing import List, Tuple

MUTATION_RATE = .005


class SimpleManager(PopulationManager):
    """
    Takes a very simplistic approach to creating new Genotypes from existing ones
    """
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True)  # it's still in tuple form
        fittest_individual: Genotype = judged_population[0][0]

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
    """
    Each set of parent Genotypes produces multiple child Genotypes
    """
    def __init__(self, population: List[Genotype], fitness_calculator: FitnessCalculator, name: str):
        super().__init__(population, fitness_calculator, name)
        # M is the population size. This variable is used to make sure the actual population size stays constant
        self._M = len(population)
        self._num_children = 3

    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True)  # it's still in tuple form
        fittest_individual: Genotype = judged_population[0][0]

        children = []

        for genotype in population:
            children += self.produce_multiple_children([fittest_individual, genotype, choice(population)])

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
        combined_population = parents + children
        unique_population = set(combined_population)
        # print('# unique Genotypes:', len(unique_population))
        judged_population = self.calculate_population_fitness(unique_population)
        judged_population.sort(key=lambda e: e[1], reverse=True)

        next_generation = [judged_population[i][0] for i in range(self._M)]
        # Make LifecycleReport with combined_population so that we actually know what the diversity is
        self._newest_report = self.make_LifecycleReport(combined_population)
        return next_generation


class DiversityManager(PopulationManager):
    """
    Encourages diversity in the population
    """
    def __init__(self, population: List[Genotype], fitness_calculator: FitnessCalculator, name: str):
        super().__init__(population, fitness_calculator, name)
        # M is the population size. This variable is used to make sure the actual population size stays constant
        self._M = len(population)
        self._num_children = 2

    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True)  # it's still in tuple form
        fittest_individual: Genotype = judged_population[0][0]

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

    def _choose_genotypes_from_sorted_unique_list(self, genotypes: List[Genotype]) -> List[Genotype]:
        """
        Takes in all the unique Genotypes from the population and selects some to keep
        :param genotypes: A sorted list of unique Genotypes
        """
        splitting_point = math.floor(self._M/2)
        good = [genotypes[i] for i in range(self._M - splitting_point)]
        # bad = [genotypes[i] for i in range(-1, -splitting_point-1, -1)]
        bad = generate_random_population(splitting_point, len(genotypes[0])) #insert garbage Genotypes
        return good + bad

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        combined_population = parents + children
        unique_population = set(combined_population)
        # print('# unique Genotypes:', len(unique_population))
        judged_population = self.calculate_population_fitness(unique_population)
        judged_population.sort(key=lambda e: e[1], reverse=True)

        # Make LifecycleReport with combined_population so that we actually know what the diversity is
        self._newest_report = self.make_LifecycleReport(combined_population)
        return self._choose_genotypes_from_sorted_unique_list([g[0] for g in judged_population])


class TournamentManager(PopulationManager):
    """
    Uses tournament selection
    """
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        parents = []
        for pair in judged_population:
            parents.append(max(pair, choice(judged_population), key=lambda t: t[1])[0]) # this is where the tournament happens
        children = self.create_offspring(parents)
        return parents, children

    def create_offspring(self, parents: List[Genotype]) -> List[Genotype]:
        children = []
        for _ in parents:
            children.append(self.crossover_and_mutate(choice(parents), choice(parents)))
        return children

    @staticmethod
    def crossover_and_mutate(parent1: Genotype, parent2: Genotype) -> Genotype:
        child_array = []
        for i in range(len(parent1)):
            parent_choice = randint(0, 1)
            parent: Genotype
            if parent_choice == 0:
                parent = parent1
            else:
                parent = parent2
            child_array.append(parent[i])
        child = Genotype(bytearray(child_array))
        child.mutate(MUTATION_RATE)
        return child

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        self._newest_report = self.make_LifecycleReport(children)
        return children
