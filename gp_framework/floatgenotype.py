from gp_framework.genotype import Genotype
from typing import List
import numpy as np


class FloatGenotype(Genotype):
    def __init__(self, floats: List[float]):
        self._floats = floats
        self._hashcode = None

    def _mutate_floats(self, mutation_factor: float) -> List[float]:
        return [f + np.random.uniform(-mutation_factor, mutation_factor, 1)[0] for f in self._floats]

    def mutate(self, mutation_factor: float):
        self._floats = self._mutate_floats(mutation_factor)

    def make_mutated_copy(self, mutation_factor):
        return FloatGenotype(self._mutate_floats(mutation_factor))

    def __getitem__(self, item):
        return self._floats[item]

    def __len__(self):
        return len(self._floats)

    def __eq__(self, other):
        if not isinstance(other, FloatGenotype):
            return False
        return self._floats == other._floats

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        if self._hashcode is None:
            self._hashcode = int(sum(self._floats) * 10)
        return self._hashcode

    @staticmethod
    def generate_random_genotype(genotype_size: int, lower_bound: float, upper_bound: float):
        floats = [np.random.uniform(lower_bound, upper_bound, 1)[0] for _ in range(genotype_size)]
        return FloatGenotype(floats)

    @staticmethod
    def generate_random_population(population_size: int, genotype_size: int, lower_bound: float, upper_bound: float):
        return [FloatGenotype.generate_random_genotype(genotype_size, lower_bound, upper_bound)
                for _ in range(population_size)]
