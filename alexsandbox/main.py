from operator import itemgetter
from random import choice, randint

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
            child.mutate(.0001)
            children.append(child)
        return population, children

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        all_genotypes = self.calculate_population_fitness(parents + children)
        all_genotypes.sort(key=lambda e: e[1], reverse=True)
        half_way = int(len(all_genotypes) / 2)
        new_population = [g[0] for g in all_genotypes[0:half_way]]
        self._newest_report = self.make_LifecycleReport(new_population)
        return new_population


class MeiosisManager(PopulationManager):
    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True) # it's still in tuple form
        fittest_individual: Genotype = judged_population[0][0]
        # other_parent: Genotype = judged_population[int(len(judged_population)/2)][0]

        children = []
        children_per_parent = 2

        for genotype in population:
            children.append(self.breed([genotype, fittest_individual]))
            # children += MeiosisManager.breed_children([fittest_individual, genotype], children_per_parent)

        """selected_children = []
        for i in range(len(population)):
            selected_children.append(children[i * children_per_parent + randint(0, children_per_parent-1)])
"""
        return population, children

    @staticmethod
    def breed_children(parents: List[Genotype], num_children: int) -> List[Genotype]:
        children = []
        for i in range(num_children):
            children.append(MeiosisManager.breed(parents))
        return children

    @staticmethod
    def breed(parents: List[Genotype]) -> Genotype:
        """
        Randomly select bits of the parent Genotypes to create a new child Genotype
        :param parents: A list of all the possible parents for the child Genotype
        """
        child_byte_array = bytearray()
        for i in range(len(parents[0])):
            parent = choice(parents)
            child_byte_array.append(parent[i])
        child = Genotype(child_byte_array)
        child.mutate(.001)
        return child

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        self._newest_report = self.make_LifecycleReport(children)
        return children


def main():
    string_to_find = "hello world"
    phenotype_converter = create_PhenotypeConverter(Phenotype.STRING, [len(string_to_find)])
    fitness_calculator: FitnessCalculator = FitnessCalculatorStringMatch([string_to_find])
    population = generate_random_population(20, len(string_to_find))

    simple_manager = SimpleManager(population, phenotype_converter, fitness_calculator, "simple_manager")
    truncation_manager = TruncationManager(population, phenotype_converter, fitness_calculator, "truncation_manager")
    meiosis_manager = MeiosisManager(population, phenotype_converter, fitness_calculator, "meiosis_manager")
    managers = [meiosis_manager]

    optimizer = EvolutionaryOptimizer(managers)
    name_to_reports = optimizer.run_many_lifecycles(10_000)
    rep.generate_many_reports(LifecycleReport.header(), name_to_reports, {}, 4)


main()
