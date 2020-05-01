from operator import itemgetter
import time

from gp_framework.genotype import generate_random_population
from gp_framework.phenotype_converter import create_PhenotypeConverter, Phenotype
from gp_framework.population_manager import *
from gp_framework import report as rep
from gp_framework.fitness_calculator import FitnessCalculatorStringMatch


class MyManager(PopulationManager):

    def produce_offspring(self, population: List[Genotype]) -> Tuple[List[Genotype], List[Genotype]]:
        judged_population, _ = self.calculate_population_fitness(population)
        fittest_individual_tuple = max(judged_population, key=itemgetter(1))
        fitness: float = fittest_individual_tuple[1]
        children = []

        for _ in range(len(population)):
            child: Genotype = fittest_individual_tuple[0]
            child.mutate((1.0 - fitness) * .01)
            children.append(child)

        return [fittest_individual_tuple[0]], children

    def select_next_generation(self, parents: List[Genotype], children: List[Genotype]) -> List[Genotype]:
        next_generation = children[0:len(children)] + parents[0:len(parents)]
        _, report = self.calculate_population_fitness(next_generation)
        self._newest_report = report
        return next_generation


def main():
    string_to_find = "hello world"
    phenotypeConverter = create_PhenotypeConverter(Phenotype.STRING, [len(string_to_find)])
    fitness_calculator: FitnessCalculator = FitnessCalculatorStringMatch([string_to_find])

    manager3 = MyManager(generate_random_population(3, len(string_to_find)), phenotypeConverter, fitness_calculator)
    manager10 = MyManager(generate_random_population(10, len(string_to_find)), phenotypeConverter, fitness_calculator)

    reports3 = run_selection_process(manager3, 10_000, "M = 3 test")
    reports10 = run_selection_process(manager10, 10_000, "M = 10 test")

    rep.generate_csv("M3.csv", LifecycleReport.header(), [report.to_list() for report in reports3])
    rep.generate_csv("M10.csv", LifecycleReport.header(), [report.to_list() for report in reports10])

    rep.generate_plot_from_csv("M3.csv", 10, "M3")
    rep.generate_plot_from_csv("M10.csv", 10, "M10")


def run_selection_process(manager: PopulationManager, iterations: int, name: str = None) -> List[LifecycleReport]:
    if name is not None:
        print("Began {} at {}.".format(name, time.asctime(time.localtime(time.time()))))

    i = 0
    reports = []
    while i < iterations and (len(reports) == 0 or not reports[len(reports) - 1].solution_found):
        reports.append(manager.lifecycle())
        if i % 250 == 0: print(i)
        i += 1

    if name is not None:
        print("Finished {} ({} iterations) at {}.".format(name, iterations, time.asctime(time.localtime(time.time()))))
        print()

    return reports


main()
