import abc
from typing import List, Tuple
from abc import abstractmethod
from gp_demo.gp_framework import Genotype, FitnessCalculator


class PopulationReport:
    """
    It's a POJO for whatever data we think is good to keep track of from generation to generation
    """
    def __init__(self, max_fitness, min_fitness, mean_fitness):
        self._max_fitness = max_fitness
        self._min_fitness = min_fitness
        self._mean_fitness = mean_fitness

    def to_list(self):
        return [self.max_fitness, self.min_fitness, self.mean_fitness]

    @staticmethod
    def header() -> List[str]:
        return ['max_fitness', 'min_fitness', 'mean_fitness']

    @property
    def max_fitness(self):
        return self._max_fitness

    @property
    def min_fitness(self):
        return self._min_fitness

    @property
    def mean_fitness(self):
        return self._mean_fitness


class PopulationManager(abc.ABC):
    """
    This abstract class wraps up useful default behavior for searching the solution space.
    Subclass and override the behavior in breed_herd and cull_herd. Then, just call lifecycle.
    """
    def __init__(self, population: List[Genotype], fitness_calculator: FitnessCalculator):
        """
        todo: should M = len(population)?
        :param population: The starting population
        :param fitness_calculator: This is used to judge our solutions
        """
        self._population = population
        self._fitness_calculator = fitness_calculator

    def calculate_population_fitness(self) -> Tuple[List[Tuple[Genotype, int]], PopulationReport]:
        """
        Use fitness_calculator to assign a rank to each Genotype in the population
        :return: each member of the population with their fitness, a summary of important findings
        """
        max_fitness = -1
        min_fitness = -1
        total_fitness = 0
        judged_population = []

        for genotype in self._population:
            fitness = self._fitness_calculator.calculate_fitness(genotype.to_string())
            judged_population.append((genotype, fitness))
            total_fitness += fitness
            if fitness > max_fitness:
                max_fitness = fitness
            if min_fitness < 0 or fitness < min_fitness:
                min_fitness = fitness

        report = PopulationReport(max_fitness, min_fitness, total_fitness / len(judged_population))
        return judged_population, report

    @abstractmethod
    def produce_offspring(self, population: List[Tuple[Genotype, int]]) -> List[Genotype]:
        """
        Create new Genotypes from the old ones
        :param population: A list of tuples pairing a Genotype with its fitness
        :return: The offspring of population
        """
        pass

    @abstractmethod
    def select_next_generation(self, parents: List[Tuple[Genotype, int]], children: List[Genotype]) -> List[Genotype]:
        """
        Select M individuals to make up the next generation of Genotypes
        :param parents: The old generation paired with their fitnesses
        :param children: The offspring of parents
        :return: the new generation
        """
        pass

    def lifecycle(self) -> PopulationReport:
        """
        Run the population of solutions through a selection process
        :return: a summary of important findings
        """
        judged_population, report = self.calculate_population_fitness()
        children = self.produce_offspring(judged_population)
        self._population = self.select_next_generation(judged_population, children)
        return report
