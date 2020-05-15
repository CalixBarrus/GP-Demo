"""
Mitosis is splitting DNA strands and mutating them
"""
from operator import itemgetter
from gp_framework.population_manager import *
from gp_framework.bytegenotype import ByteGenotype


class SimpleManager(PopulationManager):
    def produce_offspring(self, population: List[ByteGenotype]) -> Tuple[List[ByteGenotype], List[ByteGenotype]]:
        judged_population = self.calculate_population_fitness(population)
        fittest_individual_tuple = max(judged_population, key=itemgetter(1))
        fitness: float = fittest_individual_tuple[1]
        children = []

        for _ in range(len(population)):
            child: ByteGenotype = fittest_individual_tuple[0]
            child.mutate((1.0 - fitness) * .0001)
            children.append(child)

        return [fittest_individual_tuple[0]], children

    def select_next_generation(self, parents: List[ByteGenotype], children: List[ByteGenotype]) -> List[ByteGenotype]:
        self._newest_report = self.make_LifecycleReport(children)
        return children


class TruncationManager(PopulationManager):
    def produce_offspring(self, population: List[ByteGenotype]) -> Tuple[List[ByteGenotype], List[ByteGenotype]]:
        children = []
        for genotype in population:
            child = genotype
            child.mutate(.0001)
            children.append(child)
        return population, children

    def select_next_generation(self, parents: List[ByteGenotype], children: List[ByteGenotype]) -> List[ByteGenotype]:
        all_genotypes = self.calculate_population_fitness(parents + children)
        all_genotypes.sort(key=lambda e: e[1], reverse=True)
        half_way = int(len(all_genotypes) / 2)
        new_population = [g[0] for g in all_genotypes[0:half_way]]
        self._newest_report = self.make_LifecycleReport(new_population)
        return new_population


class BruteForce(PopulationManager):
    def __init__(self, population: List[ByteGenotype], fitness_calculator: FitnessCalculator, name: str = "Brute Force Manager"):
        super().__init__(population, fitness_calculator, name)
        judged_population = self.calculate_population_fitness(population)
        judged_population.sort(key=lambda e: e[1], reverse=True)
        self._best_genotype = judged_population[0][0]
        self._best_fitness = -1

    def produce_offspring(self, population: List[ByteGenotype]) -> Tuple[List[ByteGenotype], List[ByteGenotype]]:
        children = ByteGenotype.generate_random_population(20, len(self._best_genotype))
        return [self._best_genotype], children

    def select_next_generation(self, parents: List[ByteGenotype], children: List[ByteGenotype]) -> List[ByteGenotype]:
        combined_pop_with_fitness = self.calculate_population_fitness(parents + children)
        combined_pop_with_fitness.sort(key=lambda elem: elem[1], reverse=True)
        self._best_genotype = combined_pop_with_fitness[0][0]
        self._best_fitness = combined_pop_with_fitness[0][1]
        # this could just be a list with just the fittest individual since that's what'll be output anyways
        self._newest_report = self.make_LifecycleReport([elem[0] for elem in combined_pop_with_fitness])
        return []
