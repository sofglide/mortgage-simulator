"""
report generation
"""
from typing import List

from terminaltables import DoubleTable

from mortgage_simulator.utils import add_color

ROW_INDEX = [
    "Simulation type",
    "Property value",
    "Down payment",
    "Loan",
    "Interest rate",
    "Loan to value ratio",
    "Loan to income ratio",
    "Minimum amortization rate",
    "Minimum monthly payment",
    "Maximum term",
    "Monthly payment",
    "Interest payment",
    "Amortization",
    "Amortization rate",
    "Term",
    "Total principal payments",
    "Total interest payments",
    "Total payments",
    "Interest to principal",
    "APY",
    "APR",
]


class SimulationReport:
    """
    Simulation report generator
    """

    def __init__(self):
        self.columns = {add_color(row): [] for row in ROW_INDEX}
        self.size = 0

    def add_simulation(self, data: List[str]):
        """
        Add simulation to report
        :param data:
        :return:
        """
        self.size = self.size + 1
        for i, row in enumerate(ROW_INDEX):
            self.columns[add_color(row)].append(add_color(row, data[i]))

    def get_report(self) -> str:
        """
        Get report
        :return:
        """
        simulation_list = [[key] + value for key, value in self.columns.items()]
        report_table = DoubleTable(simulation_list)

        for i in range(1, self.size + 1):
            report_table.justify_columns[i] = "right"

        return report_table.table
