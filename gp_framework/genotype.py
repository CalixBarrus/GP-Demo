from abc import ABC, abstractmethod

class Genotype(ABC):
    @abstractmethod
    def mutate(self, mutation_factor: float):
        pass

    @abstractmethod
    def make_mutated_copy(self, mutation_factor: float):
        pass

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def __ne__(self, other):
        pass

    @abstractmethod
    def __hash__(self):
        pass
