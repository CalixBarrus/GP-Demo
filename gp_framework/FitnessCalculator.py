from enum import Enum
from typing import List
import abc


class Application(Enum):
    STRING_MATCH = 0


class FitnessCalculator(abc.ABC):
    def __init__(self, application_arguments: List[any]):
        """
        If there is a known target fitness, it should be specified in the child's constructor
        :param application_arguments: This varies depending on the needs of the concrete FitnessCalculator
        """
        self._application_arguments = application_arguments
        self._target_fitness = -1

    @property
    def target_fitness(self):
        return self._target_fitness

    def calculate_normalized_fitness(self, phenotype) -> float:
        return self.calculate_fitness(phenotype) / self._target_fitness

    @abc.abstractmethod
    def calculate_fitness(self, phenotype) -> int:
        """
        Calculate the fitness of the given phenotype
        :param phenotype: the phenotype to calculate the fitness of
        :return: the fitness of phenotype, a float between 0 and 1
        """
        pass


class FitnessCalculatorStringMatch(FitnessCalculator):
    def __init__(self, application_arguments: List[any]):
        super().__init__(application_arguments)
        self._target_fitness = self.calculate_fitness(application_arguments[0])

    def calculate_fitness(self, phenotype: str, application_arguments: List[any] = None) -> int:
        """
        This is similar to the other function, but returns an unnormalized value
        """
        # Assume that the phenotype is a string of the same length as the target_string
        if application_arguments is None:
            application_arguments = self._application_arguments
        target_string = application_arguments[0]

        if not isinstance(target_string, str):
            raise InvalidArgumentException
        if len(target_string) != len(phenotype):
            return 0

        fitness = 0
        for i in range(len(phenotype)):
            distance = abs(ord(target_string[i]) - ord(phenotype[i]))
            fitness += 127 - distance
        return fitness


def create_FitnessCalculator(application: Application, application_parameters: List[any]) -> FitnessCalculator:
    if application == Application.STRING_MATCH:
        return FitnessCalculatorStringMatch(application_parameters)
    else:
        raise InvalidArgumentException


class InvalidApplicationException(Exception):
    pass


class InvalidArgumentException(Exception):
    pass
