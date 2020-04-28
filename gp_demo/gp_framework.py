from random import randrange, random

from gp_demo import config


# How to represent Genotype as list of bits? Just have it as an integer and
# find a way to interact with the bits?
# Maybe use a bytearray and bytes?


def generate_random_genotype(number_of_bytes):
    """
    Randomly generates a bytes object to represent a given genotype. For some
    application, each byte can represent an ascii character.

    :param number_of_bytes: Desired length of the returned bytes object
    :return: Randomly generated bytes object
    """

    # For now, Genotype is represented as a static array of bytes. What would be
    # some other good representations?

    array = bytearray()
    for byte in range(number_of_bytes):
        # Generate byte, plug mask into each bit
        new_byte = randrange(2)
        for bit in range(7):
            new_byte = new_byte << 1
            if 1 == randrange(2):
                new_byte += 1

        array.append(new_byte)

    return bytes(array)


# TODO: Code each conversion function to accept empty or null representation_arguments with some default value
# TODO: Ask: Is this a valid implementation of the factory design method?
def convert_to_phenotype(genotype, representation, representation_arguments):
    """
    Function that converts a genotype to the desired representation. The
    conversion to a new representation must be coded in below. The number and
    type of arguments depends on the desired representation.

    :param genotype:
    :param representation: Valid inputs are "string", "parameters"
    :param representation_arguments: If representation is a number of parameters, arguments has
    the number of parameters. If representation is a string, arguments has the
    length of the string.
    :return: An array of real doubles from 0 to 1, or String of ASCII characters
    """

    switcher = {
        "string": _convert_to_string,
        "parameters": _convert_to_parameters,
    }

    # TODO: Find a good way to have the switcher throw an exception on the default case
    func = switcher.get(representation, lambda: 0)
    return func(genotype, representation_arguments)


def _convert_to_string(genotype, arguments):
    """
    Private method called by convert_to_phenotype.
    :param genotype: An immutable array of bytes of some predetermined length
    :param arguments: Array; The first argument should be an int for the string
    length.
    :return: A string of the indicated length  consisting of each byte converted
    to an ASCII character
    """
    result = ""

    for i in range(arguments[0]):
        # Ignore the first bit in each byte (ASCII characters are 7 bits)
        ascii_value = genotype[i]
        if ascii_value >= 128:
            ascii_value -= 128
        result += chr(ascii_value)

    return result


def _convert_to_parameters(genotype, arguments):
    """
    Turn genome into an array of parameters between 0 and 1 to be plugged into
    some application.

    :param genotype: Array of bytes
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
            if (index_of_genome == len(genotype)):
                index_of_genome = 0
            parameter_to_add += str(hex(genotype[index_of_genome]))[2:]
            index_of_genome += 1
        parameter_to_add += "p0"
        # parameter_to_add should be a string "0x0.****************p0"
        parameters.append(float.fromhex(parameter_to_add))

    return parameters


def mutate_genotype(genotype, mutation_factor):
    """

    :param genotype:
    :param mutation_factor:
    :return:
    """
    # newbyte = byte ^ (xor) mask -> this will flip the bits that are on in the mask.
    result = []
    for byte in genotype:

        # Create a mask for each byte
        bitmask = 0
        if (random() < mutation_factor):
            bitmask += 1
        for i in range(7):
            bitmask = bitmask << 1
            if (random() < mutation_factor):
                bitmask += 1

        result.append(byte ^ bitmask)

    # Convert list of bytes to type bytes
    return bytes(result)


def generate_random_population(size_of_population, number_of_bytes):
    population = []
    for i in range(size_of_population):
        population.append(generate_random_genotype(number_of_bytes))
    return population

# Maybe make other calculate fitness that takes genotype and representation, and
# calls convert_to_phenotype?
def calculateFitness(phenotype, application, application_arguments):
    """
    * Important: Phenotype must match the given application TODO: Check for this

    :param phenotype:
    :param application:
    :param application_arguments:
    :return:
    """
    switcher = {
        "String Match": _string_match_fitness,
    }

    # TODO: Find a good way to have the switcher throw an exception on the default case
    func = switcher.get(application, lambda: 0)
    return func(phenotype, application_arguments)


def _string_match_fitness(phenotype, arguments):
    """

    :param phenotype:
    :param arguments:
    :return:
    """
    # Assume that the phenotype is a string of the same length as the target_string
    if arguments != None:
        target_string = arguments[0]
    else:
        target_string = "hello world"

    if len(target_string) != len(phenotype):
        return 0

    fitness = 0
    for i in range(len(phenotype)):
        distance = abs(ord(target_string[i]) - ord(phenotype[i]))
        fitness += 127 - distance
    return fitness

# mutate

# crossover
