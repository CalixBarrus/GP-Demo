# How to represent Genotype as list of bits? Just have it as an integer and
# find a way to interact with the bits?
# Maybe use a bytearray and bytes?
from random import randrange, random
from typing import List, Collection
from abc import ABC, abstractmethod


class Genotype:

    def __init__(self, array_of_bytes: bytearray):
        """
        Initialize an instance of Genotype
        :param array_of_bytes: The underlying representation of the genotype. For some
                application, each byte can represent an ascii character
        :param phenotype_converter: An object that converts this Genotype into the appropriate phenotype
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


class PhenotypeConverter(ABC):
    """
    Converts a Genotype to a phenotype
    """

    @abstractmethod
    def convert(self, genotype: Genotype) -> any:
        pass


class StringPhenotypeConverter(PhenotypeConverter):
    @staticmethod
    def _normalize_ascii_value(value: int) -> int:
        if 65 <= value <= 122:
            return value
        value = (abs(value) % (122 - 65)) + 65
        return value

    def convert(self, genotype, parameters: List[any] = None) -> str:
        """
        :return: A string of the indicated length  consisting of each byte converted
        to an ASCII character
        """
        result = ""

        for i in range(len(genotype)):
            # Ignore the first bit in each byte (ASCII characters are 7 bits)
            ascii_value = StringPhenotypeConverter._normalize_ascii_value(genotype[i])
            result += chr(ascii_value)

        return result


class ParametersPhenotypeConverter(PhenotypeConverter):
    def __init__(self, number_of_parameters: int):
        """
        Turn genome into an array of parameters between 0 and 1 to be plugged into
        some application.
        :param number_of_parameters: An int determining the number of parameters
        """
        self._number_of_parameters = number_of_parameters

    def convert(self, genotype: Genotype) -> List[float]:
        """
        Turn genome into an array of parameters between 0 and 1 to be plugged into
        some application.

        :param genotype: Array; the first argument should be an int determining the
        number of parameters.
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
