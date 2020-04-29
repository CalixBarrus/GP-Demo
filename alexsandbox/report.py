import typing
import csv
from gp_demo.gp_framework import *
from gp_demo.PopulationManager import PopulationManager, PopulationReport


def generate_csv(csv_name: str, herd_reports: List[PopulationReport]) -> None:
    with open(csv_name, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(PopulationReport.headers())
        for report in herd_reports:
            csv_writer.writerow(report.to_list())
