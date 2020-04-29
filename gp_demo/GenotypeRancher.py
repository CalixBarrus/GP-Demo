import abc
from typing import List, Tuple
from abc import abstractmethod
from gp_demo.gp_framework import Genotype, FitnessCalculator


class HerdReport:
    """
    It's a POJO for whatever data we think is good to keep track of from generation to generation
    """
    def __init__(self, max_fitness, min_fitness, mean_fitness):
        self.max_fitness = max_fitness
        self.min_fitness = min_fitness
        self.mean_fitness = mean_fitness


class GenotypeRancher(abc.ABC):
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

    def judge_herd(self) -> Tuple[List[Tuple[Genotype, int]], HerdReport]:
        """
        Use fitness_calculator to assign a rank to each Genotype in the population
        :return: each member of the population with their fitness, a summary of important findings
        """
        max_fitness = -1
        min_fitness = -1
        total_fitness = 0
        judged_population = []

        for genotype in self._population:
            fitness = self._fitness_calculator.calculate_fitness(genotype, None)
            judged_population.append((genotype, fitness))
            total_fitness += fitness
            if fitness > max_fitness:
                max_fitness = fitness
            if min_fitness < 0 or fitness < min_fitness:
                min_fitness = fitness

        report = HerdReport(max_fitness, min_fitness, total_fitness / len(judged_population))
        return judged_population, report

    @abstractmethod
    def breed_herd(self, population: List[Tuple[Genotype, int]]) -> List[Genotype]:
        """
        Create new Genotypes from the old ones
        :param population: A list of tuples pairing a Genotype with its fitness
        :return: The offspring of population
        """
        pass

    @abstractmethod
    def cull_herd(self, parents: List[Tuple[Genotype, int]], children: List[Genotype]) -> List[Genotype]:
        """
        Select M individuals to make up the next generation of Genotypes
        :param parents: The old generation paired with their fitnesses
        :param children: The offspring of parents
        :return: the new generation
        """
        pass

    def lifecycle(self) -> HerdReport:
        """
        Run the population of solutions through a selection process
        :return: a summary of important findings
        """
        judged_population, report = self.judge_herd()
        children = self.breed_herd(judged_population)
        self._population = self.cull_herd(judged_population, children)
        return report
