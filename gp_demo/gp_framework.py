from enum import Enum
from random import randrange, random
from typing import List
import abc

from gp_demo import config


# How to represent Genotype as list of bits? Just have it as an integer and
# find a way to interact with the bits?
# Maybe use a bytearray and bytes?

class Genotype:

    def __init__(self, array_of_bytes: bytearray):
        """
        Initialize an instance of Genotype
        :param array_of_bytes: The underlying representation of the genotype. For some
                application, each byte can represent an ascii character
        """
        self._array_of_bytes = array_of_bytes

    def __getitem__(self, item):
        return self._array_of_bytes[item]

    def __len__(self):
        return len(self._array_of_bytes)

    def mutate(self, mutation_factor: float) -> None:
        """
        :param mutation_factor: the probability of having a 1 at any given index in the bitmask should be in [0.0, 1.0]
        """
        # newbyte = byte ^ (xor) mask -> this will flip the bits that are on in the mask.

        result = []
        for byte in self._array_of_bytes:

            # Create a mask for each byte
            bitmask = 0
            if random() < mutation_factor:
                bitmask += 1
            for i in range(7):
                bitmask = bitmask << 1
                if random() < mutation_factor:
                    bitmask += 1

            result.append(byte ^ bitmask)

        # Convert list of bytes to type bytes
        self._array_of_bytes = result

    @staticmethod
    def _normalize_ascii_value(value: int) -> int:
        if 65 <= value <= 122:
            return value
        value = (abs(value) % (122 - 65)) + 65
        return value

    def to_string(self) -> str:
        """
        :return: A string of the indicated length  consisting of each byte converted
        to an ASCII character
        """
        result = ""

        for i in range(len(self)):
            # Ignore the first bit in each byte (ASCII characters are 7 bits)
            ascii_value = Genotype._normalize_ascii_value(self[i])
            result += chr(ascii_value)

        return result

    def to_parameters(self, arguments):
        """
        Turn genome into an array of parameters between 0 and 1 to be plugged into
        some application.

        :param arguments: Array; the first argument should be an int determining the
        number of parameters.
        :return: An array of floats between 0 and 1
        """
        parameters = []

        index_of_genome = 0
        for i in range(arguments[0]):
            # Each parameter will consume 8 bytes, though the last 1 or 1 1/2 will
            # be lost to rounding. If the entire genome is used before finishing
            # the parameters, the function will circle around to the beginning of
            # the genome.
            parameter_to_add = "0x0."
            for j in range(8):
                if index_of_genome == len(self):
                    index_of_genome = 0
                parameter_to_add += str(hex(self[index_of_genome]))[2:]
                index_of_genome += 1
            parameter_to_add += "p0"
            # parameter_to_add should be a string "0x0.****************p0"
            parameters.append(float.fromhex(parameter_to_add))

        return parameters


def generate_random_genotype(size_of_genotype: int) -> Genotype:
    """
    Factory method to randomly generate an instance of Genotype. For some
    application, each byte can represent an ascii character.

    :param size_of_genotype: Desired length of the returned Genotype
    :return: Randomly generated Genotype
    """

    array = bytearray()
    for byte in range(size_of_genotype):
        # Generate byte, plug mask into each bit
        new_byte = randrange(2)
        for bit in range(7):
            new_byte = new_byte << 1
            if 1 == randrange(2):
                new_byte += 1

        array.append(new_byte)

    return Genotype(array)


def generate_random_population(size_of_population, size_of_genotype) -> List[Genotype]:
    """

    :param size_of_population: length of list to return
    :param size_of_genotype: size of each genotype
    :return: list of Genotypes
    """
    population = []
    for i in range(size_of_population):
        population.append(generate_random_genotype(size_of_genotype))
    return population


class FitnessCalculator(abc.ABC):

    @abc.abstractmethod
    def calculate_fitness(self, phenotype, application_arguments: List[any]) -> int:
        pass


class Application(Enum):
    STRING_MATCH = 0


class FitnessCalculatorStringMatch(FitnessCalculator):
    def calculate_fitness(self, phenotype: str, application_arguments: List[any]) -> int:
        """

        :param phenotype: the phenotype to calculate the fitness of
        :param application_arguments: the first element is the desired string
        :return: the fitness of phenotype
        """
        # Assume that the phenotype is a string of the same length as the target_string
        if application_arguments is not None:
            target_string = application_arguments[0]
        else:
            target_string = "hello world"

        if len(target_string) != len(phenotype):
            return 0

        fitness = 0
        for i in range(len(phenotype)):
            distance = abs(ord(target_string[i]) - ord(phenotype[i]))
            fitness += 127 - distance
        return fitness


class InvalidApplicationException(Exception):
    pass


def create_FitnessCalculator(application: Application) -> FitnessCalculator:
    if application == Application.STRING_MATCH:
        return FitnessCalculatorStringMatch()
    else:
        raise InvalidApplicationException

# mutate

# crossover
