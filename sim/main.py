from gp_framework.evolutionary_optimizer import EvolutionaryOptimizer
from gp_framework.genotype import generate_random_population
from gp_framework import report as rep
from gp_framework.population_manager import *
from gp_framework.fitness_calculator import make_FitnessCalculator, Application
from sim import mitosis
from sim import meiosis


def main():
    string_to_find = "hello world"
    fitness_calculator = make_FitnessCalculator(Application.STRING_MATCH, ["hello world"])
    population = generate_random_population(20, len(string_to_find))

    simple_manager = mitosis.SimpleManager(population, fitness_calculator, "simple_mitosis_manager")
    truncation_manager = mitosis.TruncationManager(population, fitness_calculator, "truncation_manager")
    simple_meiosis_manager = meiosis.SimpleManager(population, fitness_calculator, "simple_meiosis_manager")
    multiple_children_manager = meiosis.MultipleChildrenManager(population, fitness_calculator, "multiple_children_manager")
    managers = [simple_meiosis_manager, multiple_children_manager]

    optimizer = EvolutionaryOptimizer(managers)
    name_to_reports = optimizer.run_many_lifecycles(200)
    rep.generate_many_reports(LifecycleReport.header(), name_to_reports, {}, 1)


main()
