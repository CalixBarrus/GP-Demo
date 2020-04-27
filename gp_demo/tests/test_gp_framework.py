from gp_demo import gp_framework

# Using Test Framework pytest


def test_generate_random_genotype_single_byte_range():
    # Stress test to ensure generate_random_genotype() throws no errors

    # May print if desired to verify appropriate spread of integers between 0 and 255
    PRINTING = True
    for i in range(200):
        result = gp_framework.generate_random_genotype(1)
        if PRINTING:
            print(result[0])


def test__convert_to_parameters():
    genotype = gp_framework.generate_random_genotype(64)
    arguments = [3]
    print(gp_framework._convert_to_parameters(genotype, arguments))


def test__convert_to_string():
    genotype = gp_framework.generate_random_genotype(64)
    arguments = [11]
    print()
    print(gp_framework._convert_to_string(genotype, arguments))


def test_mutatate_genotype():
    # Should be able to observe infrequent bit flips in the genome
    PRINTING = True
    genotype = bytes([0b00000000, 0b00000000, 0b00000000, 0b11111111, 0b11111111, 0b11111111])
    mutation_factor = .1

    if PRINTING:
        print()
        print(genotype.hex())
    for i in range(25):
        genotype = gp_framework.mutate_genotype(genotype, mutation_factor)
        if PRINTING:
            print(genotype.hex())


def test__string_match_fitness():
    phenotype = "hello world"
    target_string = "hello world"
    fitness = gp_framework._string_match_fitness(phenotype, [target_string])
    print()
    print(fitness)