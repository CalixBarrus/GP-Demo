import time
from typing import List, Dict

from gp_framework.population_manager import PopulationManager, LifecycleReport


class EvolutionaryOptimizer:
    def __init__(self, managers: List[PopulationManager]):
        self._managers = managers

    @staticmethod
    def _run_lifecycles(manager: PopulationManager, max_iterations: int = -1) -> List[LifecycleReport]:
        print("Began {} at {}.".format(manager.name, _time()))

        i = 0
        reports = []
        while i < max_iterations and (len(reports) == 0 or not reports[len(reports) - 1].solution_found):
            reports.append(manager.lifecycle())
            if i % 250 == 0: print(i)
            i += 1

            print("Finished {} ({} iterations) at {}.".format(manager.name, i, _time()))
            print()

        return reports

    def run_lifecycles_for_all(self, max_iterations) -> Dict[str, List[LifecycleReport]]:
        manager_name_to_reports = {}
        for manager in self._managers:
            manager_name_to_reports[manager.name] = EvolutionaryOptimizer._run_lifecycles(manager, max_iterations)
        return manager_name_to_reports


def _time() -> str:
    return time.asctime(time.localtime(time.time()))
