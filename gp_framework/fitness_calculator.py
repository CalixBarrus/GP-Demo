import math
from enum import Enum
from typing import List
from abc import ABC, abstractmethod
from gp_framework.genotype import Genotype
import sim


class Application(Enum):
    STRING_MATCH = 0
    PRIMES = 1


class Phenotype(Enum):
    STRING = "string"
    PARAMETERS = "parameters"


class PhenotypeConverter(ABC):
    @abstractmethod
    def convert(self, genotype: Genotype) -> any:
        """
        Convert the given genotype to it's corresponding phenotype corresponding
        to the arguments passed on construction
        :param genotype:
        :return: Phenotype to be determined by concrete implementation.
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
        :param phenotype: the phenotype to calculate the fitness of
        :return: the fitness of phenotype, a float between 0 and 1
        """
        pass


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
        if not isinstance(phenotype, str): input()
        # print(phenotype)
        return self.calculate_fitness_of_string(phenotype)


class InvalidApplicationException(Exception):
    pass


class InvalidParameterException(Exception):
    pass


class StringPhenotypeConverter(PhenotypeConverter):
    def __init__(self, str_length: int):
        self._str_length = str_length

    def convert(self, genotype: Genotype):
        """
        Convert a genotype to a string of ASCII characters

        :param genotype:
        :return: A string of the indicated length  consisting of each byte converted
         to an ASCII character
        """
        if len(genotype) < self._str_length:
            raise InvalidParameterException("Given genotype must be at least as "
                                            "long as the string being generated")

        result = ""

        for i in range(self._str_length):
            # Ignore the first bit in each byte (ASCII characters are 7 bits)
            ascii_value = StringPhenotypeConverter._normalize_ascii_value(genotype[i])
            result += chr(ascii_value)

        return result

    @staticmethod
    def _normalize_ascii_value(value: int) -> int:
        # This can always be tweaked later if the target string is to include
        # some symbol outside the range [65, 122].
        """if 32 <= value <= 126:
            return value
        value = (abs(value) % (126 - 32)) + 32"""
        return value


class ParametersPhenotypeConverter(PhenotypeConverter):
    def __init__(self, number_of_parameters):
        self._number_of_parameters = number_of_parameters

    def convert(self, genotype: Genotype):
        """
        Turn genome into an array of parameters between 0 and 1 to be plugged into
        some application.

        :param genotype: The Genotype to convert
        :return: An array of floats between 0 and 1
        """
        parameters = []

        index_of_genome = 0
        for i in range(self._number_of_parameters):
            # Each parameter will consume 8 bytes, though the last 1 or 1 1/2 will
            # be lost to rounding. If the entire genome is used before finishing
            # the parameters, the function will circle around to the beginning of
            # the genome.
            parameter_to_add = "0x0."
            for j in range(8):
                if index_of_genome == len(genotype):
                    index_of_genome = 0
                parameter_to_add += str(hex(genotype[index_of_genome]))[2:]
                index_of_genome += 1
            parameter_to_add += "p0"
            # parameter_to_add should be a string "0x0.****************p0"
            parameters.append(float.fromhex(parameter_to_add))

        return parameters


class PrimeNumberGenerator:
    def __init__(self, w: int, x: int, w_delta: int, x_delta: int):
        self._w = w
        self._x = x
        self._w_delta = w_delta
        self._x_delta = x_delta
        self._list_of_primes = [2]

    def _add_to_list_of_primes(self):
        prime = self._list_of_primes[-1] * self._w + self._x
        self._list_of_primes.append((abs(prime) % 10_000) + 2)
        self._update_constants()

    def _update_constants(self):
        self._w += self._w_delta
        self._x += self._x_delta

    def make_list(self, size):
        for _ in range(size):
            self._add_to_list_of_primes()

    def __str__(self):
        return "w = {}; x = {}; w_delta = {}; x_delta = {}".format(
            self._w, self._x, self._w_delta, self._x_delta)

    @property
    def list_of_primes(self):
        return self._list_of_primes


class PrimeNumberPhenotypeConverter(PhenotypeConverter):
    def convert(self, genotype: Genotype) -> PrimeNumberGenerator:
        # assign each of these values based on the provided Genotype
        w: int
        x: int
        w_delta: int
        x_delta: int

        new_bytes = []
        i = 0
        while len(new_bytes) < 16:  # 16 because we need 4 bytes for each of the desired ints
            new_bytes.append(genotype[i % len(genotype)])
            i += 1

        w = self._to_int(new_bytes[:4])
        x = self._to_int(new_bytes[4:8])
        w_delta = self._to_int(new_bytes[8:12])
        x_delta = self._to_int(new_bytes[12:16])
        return PrimeNumberGenerator(w, x, w_delta, x_delta)

    @staticmethod
    def _to_int(bytes_) -> int:
        return int.from_bytes(bytes_, byteorder="little", signed=True)


class FitnessCalculatorPrimes(FitnessCalculator):
    def __init__(self, target_num_primes: int, phenotype_converter: PrimeNumberPhenotypeConverter,
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
        prime_number_generator: PrimeNumberGenerator = self._converter.convert(genotype)
        prime_number_generator.make_list(self._length_of_list_of_primes)
        set_of_primes = {x for x in prime_number_generator.list_of_primes}
        fitness = 0
        for num in set_of_primes:
            if self._is_prime(num):
                fitness += 1
        return fitness


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
        return FitnessCalculatorPrimes(target_num_primes, PrimeNumberPhenotypeConverter(), parameters)
    else:
        raise InvalidParameterException
