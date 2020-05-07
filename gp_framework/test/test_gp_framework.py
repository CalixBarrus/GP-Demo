from gp_framework import fitness_calculator

# Using Test Framework pytest

# TODO: Many of the random generation function should theoretically produce an
# even distribution of values between some min and max. How can we test for this.

def test_generate_random_genotype_single_byte_range():
    # Stress test to ensure generate_random_genotype() throws no errors

    # May print if desired to verify appropriate spread of integers between 0 and 255
    PRINTING = True
    for i in range(200):
        result = fitness_calculator.generate_random_genotype(1)
        if PRINTING:
            print(result[0])


def test__convert_to_parameters():
    genotype = fitness_calculator.generate_random_genotype(64)
    arguments = [3]
    print()
    print(fitness_calculator._convert_to_parameters(genotype, arguments))


def test__convert_to_string():
    genotype = fitness_calculator.generate_random_genotype(64)
    arguments = [11]
    print()
    print(fitness_calculator._convert_to_string(genotype, arguments))


def test_mutatate_genotype():
    # Should be able to observe infrequent bit flips in the genome
    PRINTING = True
    genotype = bytes([0b00000000, 0b00000000, 0b00000000, 0b11111111, 0b11111111, 0b11111111])
    mutation_factor = .1

    if PRINTING:
        print()
        print(genotype.hex())
    for i in range(25):
        genotype = fitness_calculator.mutate_genotype(genotype, mutation_factor)
        if PRINTING:
            print(genotype.hex())


def test__string_match_fitness():
    phenotype = "hello world"
    target_string = "hello world"
    perfect_fitness = fitness_calculator._string_match_fitness(phenotype, [target_string])
    print()
    print(perfect_fitness)

    phenotype = "hello worlc"
    fitness = fitness_calculator._string_match_fitness(phenotype, [target_string])
    print(fitness)
    assert fitness == perfect_fitness - 1

    phenotype = "hello wormd"
    fitness = fitness_calculator._string_match_fitness(phenotype, [target_string])
    print(fitness)
    assert fitness == perfect_fitness - 1

    phenotype = "           "
    fitness = fitness_calculator._string_match_fitness(phenotype, [target_string])
    print(fitness)