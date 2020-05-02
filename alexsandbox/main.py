from operator import itemgetter
import time

from gp_framework.evolutionary_optimizer import EvolutionaryOptimizer
from gp_framework.genotype import generate_random_population
from gp_framework.phenotype_converter import create_PhenotypeConverter, Phenotype
from gp_framework.population_manager import *
from gp_framework import report as rep
from gp_framework.fitness_calculator import FitnessCalculatorStringMatch


class SimpleManager(PopulationManager):
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        fittest_individual_tuple = max(judged_population, key=itemgetter(1))
        fitness: float = fittest_individual_tuple[1]
        children = []

        for _ in range(len(population)):
            child: Genotype = fittest_individual_tuple[0]
            child.mutate((1.0 - fitness) * .0001)
            children.append(child)

        return [fittest_individual_tuple[0]], children

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        self._newest_report = self.make_LifecycleReport(children)
        return children


class TruncationManager(PopulationManager):
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        children = []
        for genotype in population:
            child = genotype
            child.mutate(.001)
            children.append(child)
        return population, children

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        all_genotypes = self.calculate_population_fitness(parents + children)
        all_genotypes.sort(key=lambda e: e[1], reverse=True)
        half_way = int(len(all_genotypes) / 2)
        return [g[0] for g in all_genotypes[0:half_way]]


def main():
    string_to_find = "hello world"
    phenotype_converter = create_PhenotypeConverter(Phenotype.STRING, [len(string_to_find)])
    fitness_calculator: FitnessCalculator = FitnessCalculatorStringMatch([string_to_find])
    population = generate_random_population(20, len(string_to_find))

    simple_manager = SimpleManager(population, phenotype_converter, fitness_calculator, "simple_manager")
    truncation_manager = TruncationManager(population, phenotype_converter, fitness_calculator, "truncation_manager")
    managers = [simple_manager, truncation_manager]

    optimizer = EvolutionaryOptimizer(managers)
    name_to_reports = optimizer.run_many_lifecycles(10_000)
    rep.generate_many_reports(LifecycleReport.header(), name_to_reports, {}, 4)


main()
