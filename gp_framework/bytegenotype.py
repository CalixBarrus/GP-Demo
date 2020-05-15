from gp_framework.genotype import Genotype
from random import randrange, random


class ByteGenotype(Genotype):
    def __init__(self, array_of_bytes: bytearray):
        """
        Initialize an instance of Genotype
        The hashcode is set here because the hashcode must remain unchanged once an object is in a set.
        :param array_of_bytes: The underlying representation of the genotype. For some
                application, each byte can represent an ascii character
        """
        self._array_of_bytes = array_of_bytes
        hashcode = 0
        for byte in array_of_bytes:
            hashcode += byte
        self._hashcode = hashcode

    def __getitem__(self, item):
        return self._array_of_bytes[item]

    def __len__(self):
        return len(self._array_of_bytes)

    def _mutate_bytearray(self, mutation_factor) -> bytearray:
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
        return bytearray(result)

    def mutate(self, mutation_factor: float) -> None:
        self._array_of_bytes = self._mutate_bytearray(mutation_factor)

    def make_mutated_copy(self, mutation_factor):
        return ByteGenotype(self._mutate_bytearray(mutation_factor))

    def __eq__(self, other):
        if not isinstance(other, ByteGenotype):
            return False
        return self._array_of_bytes == other._array_of_bytes

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return self._hashcode

    @staticmethod
    def generate_random_genotype(genotype_size: int):
        """
        Factory method to randomly generate an instance of Genotype. For some
        application, each byte can represent an ascii character.
        :param genotype_size: Desired length of the returned Genotype
        :return: Randomly generated Genotype
        """

        array = bytearray()
        for byte in range(genotype_size):
            # Generate byte, plug mask into each bit
            new_byte = randrange(2)
            for bit in range(7):
                new_byte = new_byte << 1
                if 1 == randrange(2):
                    new_byte += 1

            array.append(new_byte)

        return ByteGenotype(array)

    @staticmethod
    def generate_random_population(population_size, genotype_size):
        """
        Convenience method to generate a list of random genotypes
        :param population_size: length of list to return
        :param genotype_size: size of each genotype
        :return: list of Genotypes
        """

        return [ByteGenotype.generate_random_genotype(genotype_size) for _ in range(population_size)]
