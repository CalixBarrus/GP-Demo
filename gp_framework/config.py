from gp_framework.fitness_calculator import Application


class Config:
    def __init__(self, bit_string_length: int, size_of_genotype: int, application: Application, show_plots: bool,
                 save_plots: bool):
        self._bit_string_length = bit_string_length
        self._size_of_genotype = size_of_genotype
        self._application = application
        self._show_plots = show_plots
        self._save_plots = save_plots

    @property
    def bit_string_length(self) -> int:
        return self._bit_string_length

    @property
    def size_of_genotype(self) -> int:
        return self._size_of_genotype

    @property
    def application(self) -> Application:
        return self._application

    @property
    def show_plots(self) -> bool:
        return self._show_plots

    @property
    def save_plots(self):
        return self._save_plots


CONFIG = Config(50, 11, Application.STRING_MATCH, True, True)
