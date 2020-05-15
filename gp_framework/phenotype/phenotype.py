from enum import Enum
from abc import ABC, abstractmethod

from gp_framework.bytegenotype import ByteGenotype


class Phenotype(Enum):
    STRING = "string"
    PARAMETERS = "parameters"


class PhenotypeConverter(ABC):
    @abstractmethod
    def convert(self, genotype: ByteGenotype) -> any:
        """
        Convert the given genotype to it's corresponding phenotype corresponding
        to the arguments passed on construction
        :param genotype:
        :return: Phenotype to be determined by concrete implementation.
        """
        pass


class ParametersPhenotypeConverter(PhenotypeConverter):
    def __init__(self, number_of_parameters):
        self._number_of_parameters = number_of_parameters

    def convert(self, genotype: ByteGenotype):
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
