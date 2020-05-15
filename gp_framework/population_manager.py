from typing import List, Tuple, Collection
from abc import abstractmethod, ABC

from gp_framework.fitness_calculator import FitnessCalculator
from gp_framework.bytegenotype import Genotype


class LifecycleReport:
    """
    It's a POJO for whatever data we think is good to keep track of from generation to generation
    """

    def __init__(self, max_fitness=-1.0, diversity=-1.0, solution: Genotype = None):
        self._max_fitness = max_fitness
        self._diversity = diversity
        self._solution = solution

    def to_list(self):
        return [self.max_fitness, self.diversity]

    @staticmethod
    def header() -> List[str]:
        return ['max_fitness', 'diversity']

    @property
    def max_fitness(self):
        return self._max_fitness

    @property
    def diversity(self):
        return self._diversity

    @property
    def solution(self) -> Genotype:
        return self._solution


class PopulationManager(ABC):
    """
    This abstract class wraps up useful default behavior for searching the solution space.
    Subclass and override the behavior in produce_offspring and select_next_generation. Then, just call lifecycle.
    """

    def __init__(self, population: List[Genotype],
                 fitness_calculator: FitnessCalculator, name: str = "Unnamed PopulationManager"):
        """
        :param population: The starting population
        calculator, this converts the provided genotype to a phenotype accepted
        by the fitness_calculator.
        :param fitness_calculator: This is used to judge our solutions
        :param name: the name that this PopulationManager will be known as in reports
        """
        self._population = population
        self._fitness_calculator = fitness_calculator
        # this should be set in produce_offspring or select_next_generation and is returned by lifecycle
        self._newest_report: LifecycleReport = LifecycleReport()
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def make_LifecycleReport(self, genotypes: Collection[Genotype]) -> LifecycleReport:
        max_fitness = -1
        fittest_genotype = None

        for genotype in genotypes:
            fitness = self._fitness_calculator.calculate_fitness(genotype)
            if fitness > max_fitness:
                max_fitness = fitness
                fittest_genotype = genotype

        unique_genotypes = set(genotypes)
        diversity = len(unique_genotypes) / len(genotypes)

        return LifecycleReport(max_fitness, diversity, fittest_genotype)

    def calculate_population_fitness(self, population: Collection[Genotype]) -> List[Tuple[Genotype, float]]:
        """
        Use fitness_calculator to assign a rank to each Genotype in the population
        :return: each member of the population with their fitness, a summary of important findings
        """

        judged_population: List[Tuple[Genotype, float]] = []

        for genotype in population:
            fitness = self._fitness_calculator.calculate_normalized_fitness(genotype)
            judged_population.append((genotype, fitness))

        return judged_population

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
