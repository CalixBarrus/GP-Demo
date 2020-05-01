from random import randrange, random
from typing import List
from abc import ABC, abstractmethod


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
