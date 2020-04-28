from random import randrange, random

from gp_demo import config


# We are representing genotype using the bytes type. For reference: https://docs.python.org/3/library/stdtypes.html#bytes
# Is there a better option?
def generate_random_genotype(number_of_bytes):
    """
    Randomly generates a bytes object to represent a given genotype. For some
    application, each byte can represent an ascii character.

    :param number_of_bytes: Desired length of the returned bytes object
    :return: Randomly generated object of type bytes
    """

    # For now, Genotype is represented as a static array of bytes, a "bytes" object. What would be
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


# TODO: Code each conversion function with default values of representation_arguments
# TODO: Enforce factory design method with some kind of interface
# TODO: If the framework gets big enough, we should probably move concrete implementations into separate files.
def convert_to_phenotype(genotype, representation, representation_arguments):
    """
    Function that converts a genotype to the desired representation. The
    conversion to a new representation must be coded in below. The number and
    type of arguments depends on the desired representation.

    :param genotype: Must be of type bytes
    :param representation: Valid inputs are "string", "parameters"
    :param representation_arguments:
        "parameters": representation_arguments[0] is the desired number of parameters
        "string": representation_arguments[0] is the length of the desired string.
    :return:
        "string": A string of the specified length
        "parameters": An list of floats between 0 and 1. The length of the
        list is as specified.
    """

    switcher = {
        "string": _convert_to_string,
        "parameters": _convert_to_parameters,
    }

    # TODO: Find a good way to have the switcher throw an invalid argument exception on the default case
    func = switcher.get(representation, lambda: 0)
    return func(genotype, representation_arguments)


def _convert_to_string(genotype, arguments):
    """
    Private method called by convert_to_phenotype.
    Convert genome into a string of the specified length.

    :param genotype: An immutable array of bytes of some predetermined length
    :param arguments: List; arguments[0] should be an int specifying the string
    length.
    :return: A string of the indicated length consisting of each byte converted
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
    Private method called by convert_to_phenotype.
    Convert genome into an list of parameters between 0 and 1 to be plugged into
    some application.

    :param genotype: bytes object.
    :param arguments: List; the first argument should be an int determining the
    number of parameters.
    :return: An list of floats between 0 and 1
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
            # Each byte will print as 0x**, the splice will take those two
            # hexadecimal digit.
            parameter_to_add += str(hex(genotype[index_of_genome]))[2:]
            index_of_genome += 1
        parameter_to_add += "p0"
        # parameter_to_add should be a string "0x0.****************p0"
        parameters.append(float.fromhex(parameter_to_add))

    return parameters


def mutate_genotype(genotype, mutation_factor):
    """
    Flips some bits of the given genotype

    :param genotype: Object of type bytes
    :param mutation_factor: Float; The probability that each bit will flip
    :return: Modified copy of genotype where some bits may have flipped.
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
            if random() < mutation_factor:
                bitmask += 1

        result.append(byte ^ bitmask)

    # Convert list of bytes to type bytes
    return bytes(result)


def generate_random_population(size_of_population, number_of_bytes):
    """
    Generates a random population of genotypes. Each genotype is represented as
    bytes.

    :param size_of_population: int; Number of bytes objects to create
    :param number_of_bytes: Length of each bytes object or length of each genotype
    :return: List of bytes objects.
    """
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
        "String Match": string of same length as the target string.
    :param application: Valid strings include: "String Match"
    :param application_arguments:
        "String Match": arguments[0] should be the target string.
    :return: Returns some positive integer based on the implementation of the
    fitness function. This integer is guaranteed to be higher when closer to the
    desired behavior, and lower when the phenotype is further from the desired
    behavior.
    """
    switcher = {
        "String Match": _string_match_fitness,
    }

    # TODO: Find a good way to have the switcher throw an exception on the default case
    func = switcher.get(application, lambda: 0)
    return func(phenotype, application_arguments)


def _string_match_fitness(phenotype, arguments):
    """
    Measures proximity of a given phenotype (a string) to the target string.

    :param phenotype: string of same length as the target string
    :param arguments: arguments[0] is the target string
    :return: Returns an int. This int will be higher the closer the phenotype is
    to the target string. This value maxes out at approximately 127 * n where
    n is the length of the strings.
    """

    # TODO: Throw exception when string lengths do not match
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


def select_parents(population):
    """
    Select a group from the population based on the fitness of the individuals.
    TODO: Implement this using the factory method

    :return:
    """
    pass


def reproduce(parent):
    """
    Returns a mutated copy of the parent
    TODO: Implement this using the factory method

    :return:
    """
    pass


def select_survivors(population):
    """
    Select a group of individuals to go on to the next generation.
    TODO: Implement this using the factory method

    :param population:
    :return:
    """
    pass


def run_simulation():
    # TODO: As part of implementing run_simulation, we may want to shuffle all the other conversion, fitness functions, etc. into their own modules.
    # TODO: Make some kind of config class to pass paramaters to the simulation. The config can include things like genome size, selection methods, reproduction methods, fitness, phenotype representation, etc.
    # generate population

    # for some number of generations or until some convergence condition is met
        # select parents from original population
        # reproduce with those parents
        # select survivors from original population and offspring
    # Print results; alternatively, store data from the whole process somehow
    pass
