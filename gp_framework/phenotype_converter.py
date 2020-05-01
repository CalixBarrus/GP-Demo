from abc import ABC, abstractmethod
from typing import List
from gp_framework.genotype import Genotype
from enum import Enum


class PhenotypeConverter(ABC):
    def __init__(self, arguments: List[any]):
        self.arguments = arguments

    @abstractmethod
    def convert(self, genotype: Genotype):
        """
        Convert the given genotype to it's corresponding phenotype corresponding
        to the arguments passed on construction
        :param genotype:
        :return: Phenotype to be determined by concrete implementation.
        """
        pass


class StringPhenotypeConverter(PhenotypeConverter):
    def __init__(self, arguments: List[any]):
        super().__init__(arguments)
        if arguments is None or not isinstance(arguments[0], int):
            raise InvalidArgumentException

    def convert(self, genotype: Genotype):
        """
        Convert a genotype to a string of ASCII characters

        :param genotype:
        :return: A string of the indicated length  consisting of each byte converted
         to an ASCII character
        """
        if len(genotype) < self.arguments[0]:
            raise InvalidArgumentException("Given genotype must be at least as "
                                           "long as the string being generated")

        result = ""

        for i in range(self.arguments[0]):
            # Ignore the first bit in each byte (ASCII characters are 7 bits)
            ascii_value = StringPhenotypeConverter._normalize_ascii_value(genotype[i])
            result += chr(ascii_value)

        return result

    @staticmethod
    def _normalize_ascii_value(value: int) -> int:
        # This can always be tweaked later if the target string is to include
        # some symbol outside the range [65, 122].
        if 65 <= value <= 122:
            return value
        value = (abs(value) % (122 - 65)) + 65
        return value


class ParametersPhenotypeConverter(PhenotypeConverter):
    def __init__(self, arguments: List[any]):
        super().__init__(arguments)
        if arguments == None or not isinstance(arguments[0], int):
            raise InvalidArgumentException

    def convert(self, genotype: Genotype):
        """
        Turn genome into an array of parameters between 0 and 1 to be plugged into
        some application.

        :param genotype: The Genotype to convert
        :return: An array of floats between 0 and 1
        """
        parameters = []

        index_of_genome = 0
        for i in range(self.arguments[0]):
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


class InvalidApplicationException(Exception):
    pass


class InvalidArgumentException(Exception):
    pass


class Phenotype(Enum):
    STRING = "string"
    PARAMETERS = "parameters"


def create_PhenotypeConverter(desired_phenotype: Phenotype, phenotype_parameters: List[any]) -> PhenotypeConverter:
    if desired_phenotype == Phenotype.STRING:
        return StringPhenotypeConverter(phenotype_parameters)
    elif desired_phenotype == Phenotype.PARAMETERS:
        return ParametersPhenotypeConverter(phenotype_parameters)
    else:
        raise InvalidArgumentException


class Application(Enum):
    STRING_MATCH = 0
