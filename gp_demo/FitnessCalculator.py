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
        raise InvalidApplicationException


class InvalidApplicationException(Exception):
    pass


class InvalidArgumentException(Exception):
    pass

# The following three functions could be slapped into a factory design


"""
  def _convert_to_string(genotype):
    Private method called by convert_to_phenotype.
    Convert genome into a string of the specified length.

    :param genotype: An immutable array of bytes of some predetermined length
    :param arguments: List; arguments[0] should be an int specifying the string
    length.
    :return: A string of the indicated length consisting of each byte converted
    to an ASCII character

    result = ""

    for i in range(arguments[0]):
        # Ignore the first bit in each byte (ASCII characters are 7 bits)
        ascii_value = genotype[i]
        if ascii_value >= 128:
            ascii_value -= 128
        result += chr(ascii_value)
 """

"""
def _convert_to_parameters(genotype, arguments):
   
    Private method called by convert_to_phenotype.
    Convert genome into an list of parameters between 0 and 1 to be plugged into
    some application.

    :param genotype: bytes object.
    :param arguments: List; the first argument should be an int determining the
    number of parameters.
    :return: An list of floats between 0 and 1
   
    parameters = []

    index_of_genome = 0
    for i in range(arguments[0]):
        # Each parameter will consume 8 bytes, though the last 1 or 1 1/2 will
        # be lost to rounding. If the entire genome is used before finishing
        # the parameters, the function will circle around to the beginning of
        # the genome.
        parameter_to_add = "0x0."
        for j in range(8):
            if (index_of_genome == len(genotype)):
                index_of_genome = 0
            # Each byte will print as 0x**, the splice will take those two
            # hexadecimal digit.
            parameter_to_add += str(hex(genotype[index_of_genome]))[2:]
            index_of_genome += 1
        parameter_to_add += "p0"
        # parameter_to_add should be a string "0x0.****************p0"
        parameters.append(float.fromhex(parameter_to_add))

    return parameters
"""
"""
  // TODO: change genotype:bytes to genotype:Genotype
def mutate_genotype(genotype, mutation_factor):

    Flips some bits of the given genotype

    :param genotype: Object of type bytes
    :param mutation_factor: Float; The probability that each bit will flip
    :return: Modified copy of genotype where some bits may have flipped.

    # newbyte = byte ^ (xor) mask -> this will flip the bits that are on in the mask.
    result = []
    for byte in genotype:

        # Create a mask for each byte
        bitmask = 0
        if (random() < mutation_factor):
            bitmask += 1
        for i in range(7):
            bitmask = bitmask << 1
            if random() < mutation_factor:
                bitmask += 1

"""
