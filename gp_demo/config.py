from gp_demo.FitnessCalculator import Application


class Config:
    def __init__(self, bit_string_length: int, size_of_genotype: int, application: Application):
        self._bit_string_length = bit_string_length
        self._size_of_genotype = size_of_genotype
        self._application = application

    @property
    def bit_string_length(self) -> int:
        return self._bit_string_length

    @property
    def size_of_genotype(self) -> int:
        return self._size_of_genotype

    @property
    def application(self) -> Application:
        return self._application
