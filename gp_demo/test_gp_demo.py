# DEPRECATED

from gp_demo import gp_framework
from gp_demo.demo import calculateFitness

# from gp-demo.gp_demo import calculate_fitness


def test_mutation_demo():
    assert 2 == 2


def test_crossover_demo():
    assert 1 == 1


def test_simple_calculate_fitness():
    assert calculateFitness("a", "a") == 52


def test_bits_and_bytes():
    print(gp_framework.generateRandomGenotype(2))