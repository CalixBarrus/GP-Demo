from operator import itemgetter
from gp_framework.population_manager import *

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


