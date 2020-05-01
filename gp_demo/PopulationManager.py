import abc
from typing import List, Tuple
from abc import abstractmethod
from gp_demo.FitnessCalculator import FitnessCalculator
from gp_demo.Genotype import Genotype
from gp_demo.Genotype import PhenotypeConverter


class LifecycleReport:
    """
    It's a POJO for whatever data we think is good to keep track of from generation to generation
    """
    def __init__(self, max_fitness=-1.0, min_fitness=-1.0, mean_fitness=-1.0, solution_found=False):
        self._max_fitness = max_fitness
        self._min_fitness = min_fitness
        self._mean_fitness = mean_fitness
        self._solution_found = solution_found

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

    @property
    def solution_found(self):
        return self._solution_found


class PopulationManager(abc.ABC):
    """
    This abstract class wraps up useful default behavior for searching the solution space.
    Subclass and override the behavior in breed_herd and cull_herd. Then, just call lifecycle.
    """
    def __init__(self, population: List[Genotype], fitness_calculator: FitnessCalculator,
                 phenotype_converter: PhenotypeConverter):
        """
        todo: should M = len(population)?
        :param population: The starting population
        :param fitness_calculator: This is used to judge our solutions
        :param phenotype_converter: converts the Genotypes into Phenotypes for use by fitness_calculator
        """
        self._population = population
        self._fitness_calculator = fitness_calculator
        self._phenotype_converter = phenotype_converter
        # this should be set in produce_offspring or select_next_generation and is returned by lifecycle
        self._newest_report: LifecycleReport = LifecycleReport()

    def calculate_population_fitness(self, population: List[Genotype])\
            -> Tuple[List[Tuple[Genotype, float]], LifecycleReport]:
        """
        Use fitness_calculator to assign a rank to each Genotype in the population
        :return: each member of the population with their fitness, a summary of important findings
        """
        max_fitness = -1
        min_fitness = -1
        total_fitness = 0
        judged_population = []

        for genotype in population:
            fitness = self._fitness_calculator.calculate_normalized_fitness(self._phenotype_converter.convert(genotype))
            judged_population.append((genotype, fitness))
            total_fitness += fitness
            if fitness > max_fitness:
                max_fitness = fitness
            if min_fitness < 0 or fitness < min_fitness:
                min_fitness = fitness

        report = LifecycleReport(max_fitness, min_fitness, total_fitness / len(judged_population), max_fitness == 1.0)
        return judged_population, report

    @abstractmethod
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        """
        Create new Genotypes from the old ones
        :param population: A list of tuples pairing a Genotype with its fitness
        :return: The parents (selected from population) who created the offspring, The offspring of population
        """
        pass

    @abstractmethod
    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        """
        Select M individuals to make up the next generation of Genotypes
        :param parents: The old generation paired with their fitnesses
        :param children: The offspring of parents
        :return: the new generation
        """
        pass

    def lifecycle(self) -> LifecycleReport:
        """
        Run the population of solutions through a selection process. self._population is not updated until the end
        of this method and can thus be accessed in produce_offspring and select_next_generation.
        :return: a summary of important findings
        """

        parents, children = self.produce_offspring(self._population)
        self._population = self.select_next_generation(parents, children)
        return self._newest_report
