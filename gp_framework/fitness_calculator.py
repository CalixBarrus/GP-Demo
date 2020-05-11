import math
from enum import Enum, auto
from typing import List, Dict
from abc import ABC, abstractmethod
from gp_framework.genotype import Genotype
from gp_framework.phenotype.phenotype import PhenotypeConverter
from gp_framework.exception import InvalidParameterException, InvalidApplicationException
from gp_framework.phenotype.number_generator import NumberGenerator, NumberGeneratorPhenotypeConverter
from gp_framework.phenotype.string_search import StringPhenotypeConverter
from gp_framework.phenotype.blackjack import Player, BlackJackTable, PlayerParameters, PlayerConverter


class Application(Enum):
    STRING_MATCH = auto()
    PRIMES = auto()
    BLACK_JACK = auto()


class PopulationFitnessCalculator(ABC):
    def __init__(self, phenotype_converter: PhenotypeConverter, target_fitness: int):
        self._converter = phenotype_converter
        self._target_fitness = target_fitness

    @property
    def target_fitness(self):
        return self._target_fitness

    def calculate_normalized_fitness(self, population: List[Genotype]) -> Dict[Genotype, float]:
        return {elem[0]: elem[1]/self._target_fitness for elem in self.calculate_fitness(population)}

    @abstractmethod
    def calculate_fitness(self, population: List[Genotype]) -> Dict[Genotype, int]:
        """
        Calculate the fitness of every genotype in the population. They will be automatically converted to a phenotype.
        :return: A dictionary mapping each genotype to an integer representing its fitness
        """
        pass


class FitnessCalculator(ABC):
    def __init__(self, phenotype_converter: PhenotypeConverter, application_arguments: List[any]):
        """
        If there is a known target fitness, it should be specified in the child's constructor
        :param application_arguments: This varies depending on the needs of the concrete FitnessCalculator
        """
        self._application_arguments = application_arguments
        self._target_fitness = -1
        self._converter = phenotype_converter

    @property
    def target_fitness(self):
        return self._target_fitness

    def calculate_normalized_fitness(self, genotype: Genotype) -> float:
        return self.calculate_fitness(genotype) / self._target_fitness

    @abstractmethod
    def calculate_fitness(self, genotype: Genotype) -> int:
        """
        Calculate the fitness of the given phenotype
        :param genotype: the Genotype to calculate the fitness of. It will be
        automatically converted to the correct phenotype.
        :return: the fitness of phenotype
        """
        pass

    @property
    def converter(self) -> PhenotypeConverter:
        return self._converter


class FitnessCalculatorStringMatch(FitnessCalculator):
    def __init__(self, phenotype_converter: PhenotypeConverter, application_arguments: List[any]):
        super().__init__(phenotype_converter, application_arguments)
        self._target_string = application_arguments[0]
        self._target_fitness = self.calculate_fitness_of_string(self._target_string)

    def _to_string(self, genotype: Genotype) -> str:
        return self._converter.convert(genotype)

    def calculate_fitness_of_string(self, string: str):
        if len(self._target_string) != len(string):
            return 0

        fitness = 0
        for i in range(len(string)):
            distance = abs(ord(self._target_string[i]) - ord(string[i]))
            fitness += 127 - distance
        return fitness

    def calculate_fitness(self, genotype: Genotype) -> int:
        """
        This is similar to the other function, but returns an unnormalized value
        """

        phenotype = self._to_string(genotype)
        return self.calculate_fitness_of_string(phenotype)

    @staticmethod
    def _normalize_ascii_value(value: int) -> int:
        # This can always be tweaked later if the target string is to include
        # some symbol outside the range [32, 126].
        """if 32 <= value <= 126:
            return value
        value = (abs(value) % (126 - 32)) + 32"""
        return value


class FitnessCalculatorPrimes(FitnessCalculator):
    def __init__(self, target_num_primes: int, phenotype_converter: NumberGeneratorPhenotypeConverter,
                 application_arguments: List[any]):
        super().__init__(phenotype_converter, application_arguments)
        self._length_of_list_of_primes = target_num_primes
        self._target_fitness = self._length_of_list_of_primes

    @staticmethod
    def _is_prime(x: int) -> bool:
        for i in range(2, math.ceil(math.sqrt(x))):
            if x % i == 0:
                return False
        return True

    def calculate_fitness(self, genotype: Genotype) -> int:
        prime_number_generator: NumberGenerator = self._converter.convert(genotype)
        prime_number_generator.make_list(self._length_of_list_of_primes)
        set_of_primes = {x for x in prime_number_generator.list_of_numbers}
        fitness = 0
        # check in the set so as not to double count anything
        for num in set_of_primes:
            if self._is_prime(num):
                fitness += 1
        return fitness


class PopulationFitnessCalculatorBlackJack(PopulationFitnessCalculator):
    def __init__(self, target_fitness, number_of_rounds):
        super().__init__(PlayerConverter(), target_fitness)
        self._number_of_rounds = number_of_rounds  # how many rounds the players play

    def calculate_fitness(self, population: List[Genotype]) -> Dict[Genotype, int]:
        players = []
        for genotype in population:
            players.append(self._converter.convert(genotype))
        table = BlackJackTable(players)
        table.play_rounds(self._number_of_rounds)
        fitness_dict = {}
        for i in range(len(players)):
            fitness_dict[population[i]] = table.players[i].money
        return fitness_dict


class FitnessCalculatorBlackJack(FitnessCalculator):
    def __init__(self, phenotype_converter: PhenotypeConverter, application_arguments: List[any]):
        super().__init__(phenotype_converter, application_arguments)
        self._target_fitness = application_arguments[0]
        self._number_of_rounds = application_arguments[1]

    def calculate_fitness(self, genotype: Genotype) -> int:
        player = self._converter.convert(genotype)
        table = BlackJackTable([player])
        table.play_rounds(self._number_of_rounds)
        return player.money


def make_FitnessCalculator(application: Application, parameters: List[any]) -> FitnessCalculator:
    if application == Application.STRING_MATCH:
        if not isinstance(parameters[0], str):
            raise InvalidParameterException("First Parameter must be a str.")
        target_length = len(parameters[0])
        return FitnessCalculatorStringMatch(StringPhenotypeConverter(target_length), parameters)
    elif application == Application.PRIMES:
        if not isinstance(parameters[0], int):
            raise InvalidParameterException("First Parameter must be an int.")
        target_num_primes = parameters[0]  # how many primes we are trying to generate
        return FitnessCalculatorPrimes(target_num_primes, NumberGeneratorPhenotypeConverter(), parameters)
    elif application == Application.BLACK_JACK:
        if not isinstance(parameters[0], int):
            raise InvalidParameterException("Please specify how much total winnings is the goal.")
        if not isinstance(parameters[1], int):
            raise InvalidParameterException("Please specify how many rounds will be given to each player")
        return FitnessCalculatorBlackJack(PlayerConverter(), parameters)
    else:
        raise InvalidApplicationException("{} is not a valid choice".format(str(application)))


def make_PopulationFitnessCalculator(application: Application, parameters: List[any]) -> PopulationFitnessCalculator:
    if application == Application.BLACK_JACK:
        if not isinstance(parameters[0], int):
            raise InvalidParameterException("Please specify how much total winnings is the goal.")
        if not isinstance(parameters[1], int):
            raise InvalidParameterException("Please specify how many rounds will be given to each player")
        return PopulationFitnessCalculatorBlackJack(target_fitness=parameters[0], number_of_rounds=parameters[1])
    else:
        raise InvalidApplicationException("{} is not a valid choice".format(str(application)))
