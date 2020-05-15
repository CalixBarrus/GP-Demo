from gp_framework.evolutionary_optimizer import EvolutionaryOptimizer
from gp_framework.bytegenotype import ByteGenotype
from gp_framework import report as rep, meiosis, mitosis
from gp_framework.population_manager import *
from gp_framework.fitness_calculator import make_FitnessCalculator, Application
from gp_framework.phenotype.blackjack import PlayerParameters
from math import ceil, sqrt


def is_prime(x: int) -> bool:
    for i in range(2, ceil(sqrt(x))):
        if x % i == 0:
            return False
    return True


def main():
    # string_to_find = "hello world"
    # number_of_primes = 50
    # size_of_primes_genotype = 16
    black_jack_genotype_length = PlayerParameters.number_of_parameters() * 4  # 4 bytes per float
    fitness_calculator = make_FitnessCalculator(Application.BLACK_JACK, [1000, 20])
    population = ByteGenotype.generate_random_population(20, black_jack_genotype_length)

    simple_manager = mitosis.SimpleManager(population, fitness_calculator, "simple_mitosis_manager")
    truncation_manager = mitosis.TruncationManager(population, fitness_calculator, "truncation_manager")
    brute_force_manager = mitosis.BruteForce(population, fitness_calculator, "brute_force_manager")
    simple_meiosis_manager = meiosis.SimpleManager(population, fitness_calculator, "simple_meiosis_manager")
    multiple_children_manager = meiosis.MultipleChildrenManager(population, fitness_calculator, "multiple_children_manager")
    diversity_manager = meiosis.DiversityManager(population, fitness_calculator, "diversity_manager")
    tournament_manager = meiosis.TournamentManager(population, fitness_calculator, "tournament_manager")
    managers = [simple_meiosis_manager, multiple_children_manager, diversity_manager, brute_force_manager]

    optimizer = EvolutionaryOptimizer(managers, True)
    name_to_reports = optimizer.run_many_lifecycles(5000)
    rep.generate_many_reports(LifecycleReport.header(), name_to_reports, {}, 1)
    solutions: List[Tuple[str, any]] =\
        [(elem[0], fitness_calculator.converter.convert(elem[1][-1].solution)) for elem in name_to_reports.items()]

    print("Found solutions:")
    for elem in solutions:
        print("From", elem[0])
        print("Generated word:", elem[1])


main()
