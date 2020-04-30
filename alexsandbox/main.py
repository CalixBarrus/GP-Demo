from operator import itemgetter
import time
from gp_demo.gp_framework import *
from gp_demo.PopulationManager import *
from alexsandbox import report as rep


class MyManager(PopulationManager):

    def produce_offspring(self, population: List[Tuple[Genotype, int]]) -> List[Genotype]:
        children = []
        fittest_individual = max(population, key=itemgetter(1))[0]
        for _ in range(len(population)):
            child = fittest_individual
            child.mutate(.1)
            children.append(child)

        return children

    def select_next_generation(self, parents: List[Tuple[Genotype, int]], children: List[Genotype]) -> List[Genotype]:
        return children


def main():
    fitness_calculator = create_FitnessCalculator(Application.STRING_MATCH, ["asdf"])
    manager3 = MyManager(generate_random_population(3, 4), fitness_calculator)
    manager10 = MyManager(generate_random_population(10, 4), fitness_calculator)

    reports3 = run_selection_process(manager3, 10_000, "M = 3 test")
    reports10 = run_selection_process(manager10, 10_000, "M = 10 test")

    rep.generate_csv("M3.csv", PopulationReport.header(), [report.to_list() for report in reports3])
    rep.generate_csv("M10.csv", PopulationReport.header(), [report.to_list() for report in reports10])

    rep.generate_plot_from_csv("M3.csv", 10, False, "M3")
    rep.generate_plot_from_csv("M10.csv", 10, False, "M10")


def run_selection_process(manager: PopulationManager, iterations: int, name: str = None) -> List[PopulationReport]:
    if name is not None:
        print("Began {} at {}.".format(name, time.asctime(time.localtime(time.time()))))

    reports = []
    for _ in range(iterations):
        reports.append(manager.lifecycle())

    if name is not None:
        print("Finished {} ({} iterations) at {}.".format(name, iterations, time.asctime(time.localtime(time.time()))))

    return reports


main()
