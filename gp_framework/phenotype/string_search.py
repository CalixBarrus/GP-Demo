from gp_framework.phenotype.phenotype import PhenotypeConverter
from gp_framework.genotype import Genotype
from gp_framework.exception import InvalidParameterException


class StringPhenotypeConverter(PhenotypeConverter):
    def __init__(self, str_length: int):
        self._str_length = str_length

    def convert(self, genotype: Genotype):
        """
        Convert a genotype to a string of ASCII characters

        :param genotype:
        :return: A string of the indicated length  consisting of each byte converted
         to an ASCII character
        """
        if len(genotype) < self._str_length:
            raise InvalidParameterException("Given genotype must be at least as "
                                            "long as the string being generated")

        result = ""

        for i in range(self._str_length):
            ascii_value = genotype[i]
            result += chr(ascii_value)

        return result
