"""
Created on Sun Aug  2 20:37:24 2020

@author: soussi
"""
import logging
import math
from typing import Any, Dict, List

from mortgage_simulator.utils import add_color

logger = logging.getLogger(__name__)

TAX_DEDUCTION_RATE = 0.3


class Mortgage:
    """
    Mortgage simulator class
    """

    def __init__(self, property_value: float, downpayment: float, yearly_income: float, rate: float = 0.0115) -> None:
        """
        Mortgage simulator constructor
        :param property_value:
        :param downpayment:
        :param yearly_income:
        :param rate:
        """
        self.rate = rate / (100.0 if rate > 1.0 else 1.0)
        self.property_value = property_value
        self.yearly_income = yearly_income
        self.downpayment = downpayment

        self.check_loan_to_value_limit()

    @property
    def _loan(self) -> float:
        return self.property_value - self.downpayment

    @property
    def _loan_to_value_ratio(self) -> float:
        return self._loan / self.property_value

    @property
    def _loan_to_val_amort_rate(self) -> float:
        """
        amortization rate based on loan to value
        :return:
        """
        if self._loan_to_value_ratio < 0:
            raise ValueError("Negative loan to value ratio " f"{self._loan_to_value_ratio:.2f}")
        if self._loan_to_value_ratio < 0.5:
            amort_rate = 0.0
        elif self._loan_to_value_ratio < 0.7:
            amort_rate = 0.01
        elif self._loan_to_value_ratio < 0.85:
            amort_rate = 0.02
        else:
            amort_rate = 0.02

        logger.debug(f"Loan to value ration {self._loan_to_value_ratio} requires minimum amortization {amort_rate}")
        return amort_rate

    @property
    def _r(self) -> float:
        return self.rate / 12.0

    @property
    def apy(self) -> float:
        return (1 + self.rate / 12.0) ** 12 - 1.0

    @property
    def apr(self) -> float:
        return self.rate

    @property
    def loan_to_income_ratio(self) -> float:
        return self._loan / self.yearly_income

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

        logger.debug(f"Loan to income ration {self.loan_to_income_ratio} requires minimum amortization {amort_rate}")
        return amort_rate

    @property
    def min_amort_rate(self) -> float:
        amort_rate = self._loan_to_val_amort_rate + self.income_debt_amort_rate
        logger.debug(f"Minimum amortization rate is: {amort_rate} ")
        return amort_rate

    @property
    def monthly_interest(self) -> float:
        return self._loan * self._r

    @property
    def minimum_amortization(self) -> float:
        return self._loan * self.min_amort_rate / 12.0

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

    @property
    def tax_deduction(self) -> float:
        return self.monthly_interest * TAX_DEDUCTION_RATE

    def amort_rate(self, monthly_payment: float) -> float:
        return self.amortization(monthly_payment) / self._loan * 12.0

    def check_loan_to_value_limit(self) -> None:
        if self._loan_to_value_ratio > 0.85:
            logger.warning("Your loan to value ratio is too large:" f" {self._loan / self.property_value:.2f} > 0.85")

    def term_m(self, monthly_payment: float) -> float:
        """
        mortgage term in months
        :param monthly_payment:
        :return:
        """
        if monthly_payment <= self._loan * self._r:
            raise ValueError(
                f"Monthly payment {monthly_payment} needs to be above monthly interest {self._loan * self._r}"
            )
        loan_term = (math.log(monthly_payment / self._r) - math.log(monthly_payment / self._r - self._loan)) / math.log(
            1 + self._r
        )
        return loan_term

    def term_y(self, monthly_payment: float) -> float:
        return self.term_m(monthly_payment) / 12.0

    def monthly_payment(self, term_y: float) -> float:
        term_m = term_y * 12
        return self._r * self._loan / (1 - (1 + self._r) ** (-term_m))

    def total_payment(self, monthly_payment: float) -> float:
        return monthly_payment * self.term_m(monthly_payment)

    def total_interest(self, monthly_payment: float) -> float:
        return self.total_payment(monthly_payment) - self._loan

    def interest_to_principal(self, monthly_payment: float) -> float:
        return self.total_interest(monthly_payment) / self._loan

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

    def get_payment_schedule(self, monthly_payment: int, period_months: int) -> Dict[str, List[Any]]:
        """

        :param monthly_payment:
        :param period_months:
        :return:
        """
        schedule: Dict[str, List[float]] = {
            "year": [0],
            "month": [0],
            "debt ratio": [self._loan / self.property_value],
            "month interest": [0],
            "month amortization": [0],
            "remaining loan": [self._loan],
            "total paid": [self.downpayment],
            "total interest paid": [0],
            "total amortized": [self.downpayment],
            "total tax return": [0],
        }
        loan_term = math.ceil(self.term_m(monthly_payment))
        if period_months < 0 or period_months > loan_term:
            period_months = loan_term

        for m in range(1, period_months + 1):
            month_interest = schedule["remaining loan"][-1] * self._r
            month_amortization = monthly_payment - month_interest
            schedule["year"].append((m - 1) // 12 + 1)
            schedule["month"].append(m)
            schedule["month interest"].append(month_interest)
            schedule["month amortization"].append(month_amortization)
            schedule["total paid"].append(schedule["total paid"][-1] + monthly_payment)
            schedule["total interest paid"].append(schedule["total interest paid"][-1] + month_interest)
            schedule["total amortized"].append(schedule["total amortized"][-1] + month_amortization)
            schedule["total tax return"].append(schedule["total tax return"][-1] + month_interest * TAX_DEDUCTION_RATE)
            schedule["remaining loan"].append(schedule["remaining loan"][-1] - month_amortization)
            schedule["debt ratio"].append(schedule["remaining loan"][-1] / self.property_value)

        return schedule

    def _get_simulation_data(
        self, monthly_payment: float, amortization: float, amortization_rate: float, term: float, title: str
    ) -> List[str]:
        """"""
        data = [
            title,
            f"{int(self.property_value):,} sek",
            f"{int(self.downpayment):,} sek",
            f"{int(self._loan):,} sek",
            f"{100 * self.rate:.2f} %",
            f"{self._loan_to_value_ratio * 100:.1f} %",
            f"{self.loan_to_income_ratio:.2f}",
            f"{100 * self.min_amort_rate:.2f} %",
            f"{int(self.minimum_amortization):,} sek",
            f"{int(self.minimum_monthly_payment):,} sek",
            f"{self.maximum_term_y:.1f} Y",
            add_color("monthly_payment", f"{int(monthly_payment):,} sek"),
            f"{int(self.monthly_interest):,} sek",
            f"{int(self.tax_deduction):,} sek",
            f"{int(self.monthly_interest - self.tax_deduction):,} sek",
            f"{int(amortization):,} sek",
            f"{100 * amortization_rate:.2f} %",
            f"{term:.1f} Years",
            f"{int(self._loan):,} sek",
            f"{int(self.total_interest(monthly_payment)):,} sek",
            f"{int(self.total_payment(monthly_payment)):,} sek",
            f"{100 * self.interest_to_principal(monthly_payment):.2f} %",
            f"{100 * self.apy:.2f} %",
            f"{100 * self.apr:.2f} %",
        ]

        return data
