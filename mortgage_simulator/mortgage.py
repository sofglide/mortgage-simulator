"""
Created on Sun Aug  2 20:37:24 2020

@author: soussi
"""
import logging
import math
from typing import List

from terminaltables import DoubleTable

logger = logging.getLogger(__name__)


class Mortgage:
    """
    Mortgage simulator class
    """

    def __init__(self, value, downpayment: float, income: float, rate: float = 0.0115):
        """
        Mortgage simulator constructor
        :param value:
        :param downpayment:
        :param income:
        :param rate:
        """
        self.rate = rate / (100.0 if rate > 1.0 else 1.0)
        self.value = value
        self.income = income if income > 1000000 else income * 12
        self.downpayment = downpayment

        self.check_loan_to_value_limit()

    @property
    def loan(self) -> float:
        return self.value - self.downpayment

    @property
    def loan_to_value_ratio(self) -> float:
        return self.loan / self.value

    @property
    def loan_to_val_amort_rate(self) -> float:
        """
        amortization rate based on loan to value
        :return:
        """
        if self.loan_to_value_ratio < 0:
            raise ValueError("Negative loan to value ratio " f"{self.loan_to_value_ratio:.2f}")
        if self.loan_to_value_ratio < 0.5:
            amort_rate = 0.0
        elif self.loan_to_value_ratio < 0.7:
            amort_rate = 0.01
        elif self.loan_to_value_ratio < 0.85:
            amort_rate = 0.02
        else:
            amort_rate = 0.02

        return amort_rate

    @property
    def r(self):
        return self.rate / 12.0

    @property
    def apy(self):
        return (1 + self.rate / 12.0) ** 12 - 1.0

    @property
    def apr(self):
        return self.rate

    @property
    def loan_to_income_ratio(self) -> float:
        return self.loan / self.income

    @property
    def income_debt_amort_rate(self) -> float:
        """
        amortization rate based on income
        :return:
        """ ""
        if self.loan_to_income_ratio < 0:
            raise ValueError("Negative income to loan ratio" f"{self.loan_to_income_ratio:.2f}")
        if self.loan_to_income_ratio < 4.5:
            amort_rate = 0.0
        else:
            amort_rate = 0.01
        return amort_rate

    @property
    def min_amort_rate(self) -> float:
        return self.loan_to_val_amort_rate + self.income_debt_amort_rate

    @property
    def monthly_interest(self) -> float:
        return self.loan * self.r

    @property
    def minimum_amortization(self) -> float:
        return self.loan * self.min_amort_rate / 12.0

    @property
    def minimum_monthly_payment(self) -> float:
        return self.monthly_interest + self.minimum_amortization

    @property
    def maximum_term_m(self) -> float:
        return self.term_m(self.minimum_monthly_payment)

    @property
    def maximum_term_y(self) -> float:
        return self.term_y(self.minimum_monthly_payment)

    def amortization(self, monthly_payment: float) -> float:
        return monthly_payment - self.monthly_interest

    def amort_rate(self, monthly_payment: float) -> float:
        return self.amortization(monthly_payment) / self.loan * 12.0

    def check_loan_to_value_limit(self) -> None:
        if self.loan_to_value_ratio > 0.85:
            logger.warning("Your loan to value ratio is too large:" f" {self.loan / self.value:.2f} > 0.85")

    def term_m(self, monthly_payment: float) -> float:
        """
        mortgage term in months
        :param monthly_payment:
        :return:
        """
        loan_term = (math.log(monthly_payment / self.r) - math.log(monthly_payment / self.r - self.loan)) / math.log(
            1 + self.r
        )
        return loan_term

    def term_y(self, monthly_payment: float) -> float:
        return self.term_m(monthly_payment) / 12.0

    def monthly_payment(self, term_y: float) -> float:
        term_m = term_y * 12
        return self.r * self.loan / (1 - (1 + self.r) ** (-term_m))

    def total_payment(self, monthly_payment: float) -> float:
        return monthly_payment * self.term_m(monthly_payment)

    def total_interest(self, monthly_payment: float) -> float:
        return self.total_payment(monthly_payment) - self.loan

    def interest_to_principal(self, monthly_payment: float) -> float:
        return self.total_interest(monthly_payment) / self.loan

    def simulate_by_payment(self, monthly_payment: float = None, title: str = "") -> List[str]:
        """
        Simulation based on monthly payment
        :param monthly_payment:
        :param title:
        :return:
        """
        if monthly_payment is None:
            monthly_payment = self.minimum_monthly_payment
        if monthly_payment < self.minimum_monthly_payment:
            logger.warning(
                f"Monthly payment {int(monthly_payment):,} is below minimum {int(self.minimum_monthly_payment):,}"
            )
        amortization = self.amortization(monthly_payment)
        amortization_rate = self.amort_rate(monthly_payment)
        term = self.term_y(monthly_payment)

        return self._get_simulation_data(
            monthly_payment,
            amortization,
            amortization_rate,
            term,
            title=title,
        )

    def simulate_by_term(self, term: float = 20, title: str = "") -> List[str]:
        monthly_payment = self.monthly_payment(term)
        return self.simulate_by_payment(monthly_payment, title=title)

    def _get_simulation_data(
        self, monthly_payment: float, amortization: float, amortization_rate: float, term: float, title: str
    ) -> List[str]:
        """"""
        data = [
            title,
            f"{int(self.value):,} sek",
            f"{int(self.downpayment):,} sek",
            f"{int(self.loan):,} sek",
            f"{100 * self.rate:.2f} %",
            f"{self.loan_to_value_ratio * 100:.1f} %",
            f"{self.loan_to_income_ratio:.2f}",
            f"{100 * self.min_amort_rate:.2f} %",
            f"{int(self.minimum_monthly_payment):,} sek",
            f"{self.maximum_term_y:.1f} Y",
            f"{int(monthly_payment):,} sek",
            f"{int(self.monthly_interest):,} sek",
            f"{int(amortization):,} sek",
            f"{100 * amortization_rate:.2f} %",
            f"{term:.1f} Years",
            f"{int(self.loan):,} sek",
            f"{int(self.total_interest(monthly_payment)):,} sek",
            f"{int(self.total_payment(monthly_payment)):,} sek",
            f"{100 * self.interest_to_principal(monthly_payment):.2f} %",
            f"{100 * self.apy:.2f} %",
            f"{100 * self.apr:.2f} %",
        ]

        return data


def get_simulation_table(
    mortgage: Mortgage,
    monthly_payment: float,
    amortization: float,
    amortization_rate: float,
    term: float,
    title: str,
) -> str:
    """
    Mortgage info to print as table in terminal
    :param mortgage:
    :param monthly_payment:
    :param amortization:
    :param amortization_rate:
    :param term:
    :return:
    """
    mortgage_params = [
        ["Property value", f"{int(mortgage.value):,} sek"],
        ["Down payment", f"{int(mortgage.downpayment):,} sek"],
        ["Loan", f"{int(mortgage.loan):,} sek"],
        ["Interest rate", f"{100 * mortgage.rate:.2f} %"],
        ["Loan to value ratio", f"{mortgage.loan_to_value_ratio:.2f}"],
        ["Value to income ratio", f"{mortgage.loan_to_income_ratio:.2f}"],
        ["Minimum amortization rate", f"{100 * mortgage.min_amort_rate:.2f} %"],
        ["Minimum monthly payment", f"{int(mortgage.minimum_monthly_payment):,} sek"],
        ["Maximum term", f"{mortgage.maximum_term_y:.1f}"],
        ["Monthly payment", f"{int(monthly_payment):,} sek"],
        ["Interest payment", f"{int(mortgage.monthly_interest):,} sek"],
        ["Amortization", f"{int(amortization):,} sek"],
        ["Amortization rate", f"{100 * amortization_rate:.2f} %"],
        ["Term", f"{term:.1f} Years"],
        ["Total principal payments", f"{int(mortgage.loan):,} sek"],
        [
            "Total interest payments",
            f"{int(mortgage.total_interest(monthly_payment)):,} sek",
        ],
        ["Total payments", f"{int(mortgage.total_payment(monthly_payment)):,} sek"],
        [
            "Interest to principal",
            f"{100 * mortgage.interest_to_principal(monthly_payment):.2f} %",
        ],
        ["APY", f"{100 * mortgage.apy:.2f} %"],
        ["APR", f"{100 * mortgage.apr:.2f} %"],
    ]

    mortgage_table = DoubleTable(mortgage_params, title)
    mortgage_table.justify_columns[1] = "right"

    return mortgage_table.table
