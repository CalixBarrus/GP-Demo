from gp_framework.bytegenotype import ByteGenotype
from gp_framework.phenotype.phenotype import PhenotypeConverter


class NumberGenerator:
    def __init__(self, w: int, x: int, w_delta: int, x_delta: int):
        self._w = w
        self._x = x
        self._w_delta = w_delta
        self._x_delta = x_delta
        self._list_of_numbers = [2]

    def _add_to_list_of_primes(self):
        prime = self._list_of_numbers[-1] * self._w + self._x
        self._list_of_numbers.append((abs(prime) % 10_000) + 2)
        self._update_constants()

    def _update_constants(self):
        self._w += self._w_delta
        self._x += self._x_delta

    def make_list(self, size):
        for _ in range(size):
            self._add_to_list_of_primes()

    def __str__(self):
        return "w = {}; x = {}; w_delta = {}; x_delta = {}".format(
            self._w, self._x, self._w_delta, self._x_delta)

    @property
    def list_of_numbers(self):
        return self._list_of_numbers


class NumberGeneratorPhenotypeConverter(PhenotypeConverter):
    def convert(self, genotype: ByteGenotype) -> NumberGenerator:
        # assign each of these values based on the provided Genotype
        w: int
        x: int
        w_delta: int
        x_delta: int

        new_bytes = []
        i = 0
        while len(new_bytes) < 16:  # 16 because we need 4 bytes for each of the desired ints
            new_bytes.append(genotype[i % len(genotype)])
            i += 1

        w = self._to_int(new_bytes[:4])
        x = self._to_int(new_bytes[4:8])
        w_delta = self._to_int(new_bytes[8:12])
        x_delta = self._to_int(new_bytes[12:16])
        return NumberGenerator(w, x, w_delta, x_delta)

    @staticmethod
    def _to_int(bytes_) -> int:
        return int.from_bytes(bytes_, byteorder="little", signed=True)
