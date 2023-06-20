"""Console script for mortgage_simulator."""
import logging
import os

import click

from .mortgage import Mortgage
from .schedule_report import ScheduleReport
from .simulation_report import SimulationReport
from .utils import normalize_rate

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))

DEFAULT_DOWN_PAYMENT = 1000000
DEFAULT_INTEREST_RATE = 0.0150
DEFAULT_MORTGAGE_TERM_IN_YEARS = 25
DEFAULT_MONTHLY_INCOME = 40000
DEFAULT_MONTHLY_PAYMENT = 10000


def get_minimum_monthly_amortization(principal: float, amortization_rate: float) -> float:
    return amortization_rate / 12 * principal


def get_monthly_starting_interest(principal: float, interest: float) -> float:
    return interest / 12 * principal


@click.group()
def loan_simulation() -> None:
    pass


@loan_simulation.command(name="minimum-payment", help="calculate minimum required payment given amortization rate")
@click.option("-p", "--principal", type=int, required=True, help="principal")
@click.option("-a", "--amortization-rate", type=float, required=True, help="amortization rate")
@click.option(
    "-i",
    "--interest-rate",
    type=float,
    default=DEFAULT_INTEREST_RATE,
    show_default=True,
    help="interest rate",
)
def get_minimum_monthly_payment(principal: float, interest_rate: float, amortization_rate: float) -> None:
    """
    Calculate minimum payment
    :param principal:
    :param interest_rate:
    :param amortization_rate:
    :return:
    """
    amortization_rate = normalize_rate(amortization_rate)
    interest_rate = normalize_rate(interest_rate)
    amortization_payment = get_minimum_monthly_amortization(principal, amortization_rate)
    interest_payment = get_monthly_starting_interest(principal, interest_rate)
    payment = amortization_payment + interest_payment
    print(f"Minimum monthly payment: {payment:.0f} SEK")


@loan_simulation.command("simulate", help="simulate mortgage given its parameters")
@click.option("-v", "--property-value", type=int, required=True, help="property value")
@click.option("-d", "--down-payment", type=int, default=DEFAULT_DOWN_PAYMENT, show_default=True, help="down payment")
@click.option(
    "-r",
    "--interest-rate",
    type=float,
    default=DEFAULT_INTEREST_RATE,
    show_default=True,
    help="interest rate",
)
@click.option(
    "-t",
    "--mortgage-term",
    type=int,
    default=DEFAULT_MORTGAGE_TERM_IN_YEARS,
    show_default=True,
    help="mortgage term in years",
)
@click.option(
    "-i",
    "--monthly-income",
    type=int,
    default=DEFAULT_MONTHLY_INCOME,
    show_default=True,
    help="monthly income",
)
@click.option(
    "-p",
    "--monthly-payment",
    type=int,
    default=DEFAULT_MONTHLY_PAYMENT,
    show_default=True,
    help="monthly payment",
)
def simulate_mortgage(
    property_value: int,
    down_payment: int,
    interest_rate: float,
    mortgage_term: int,
    monthly_income: int,
    monthly_payment: int,
) -> None:
    """
    API
    :param property_value:
    :param down_payment:
    :param interest_rate:
    :param mortgage_term:
    :param monthly_income:
    :param monthly_payment:
    :return:
    """
    interest_rate = normalize_rate(interest_rate)
    yearly_income = monthly_income * 12

    loan = Mortgage(
        property_value=property_value,
        downpayment=down_payment,
        yearly_income=yearly_income,
        rate=interest_rate,
    )

    simulation_by_payment = loan.simulate_by_payment(monthly_payment, title="monthly payment")
    simulations = SimulationReport()
    simulations.add_simulation(simulation_by_payment)
    simulation_by_minimum_payment = loan.simulate_by_payment(loan.minimum_monthly_payment, title="minimum payment")
    simulations.add_simulation(simulation_by_minimum_payment)

    simulation_by_term = loan.simulate_by_term(mortgage_term, title=f"term {mortgage_term:.1f} Y")
    simulations.add_simulation(simulation_by_term)

    print(simulations.get_report())


@loan_simulation.command("schedule", help="compute installments schedule")
@click.option("-v", "--property-value", type=int, required=True, help="property value")
@click.option("-d", "--down-payment", type=int, default=DEFAULT_DOWN_PAYMENT, show_default=True, help="down payment")
@click.option(
    "-r",
    "--interest-rate",
    type=float,
    default=DEFAULT_INTEREST_RATE,
    show_default=True,
    help="interest rate",
)
@click.option(
    "-i",
    "--monthly-income",
    type=int,
    default=DEFAULT_MONTHLY_INCOME,
    show_default=True,
    help="monthly income",
)
@click.option(
    "-p",
    "--monthly-payment",
    type=int,
    default=DEFAULT_MONTHLY_PAYMENT,
    show_default=True,
    help="monthly payment",
)
@click.option(
    "-m",
    "--period-months",
    type=int,
    default=-1,
    show_default=True,
    help="number of months to simulate, set to -1 to simulate until total repayment",
)
def simulate_schedule(
    property_value: int,
    down_payment: int,
    interest_rate: float,
    monthly_income: int,
    monthly_payment: int,
    period_months: int,
) -> None:
    """
    Computes at the end of every month:
    - total paid
    - remaining loan
    - paid to value ratio
    - interest paid
    - amortization paid
    :param property_value:
    :param down_payment:
    :param interest_rate:
    :param monthly_income:
    :param monthly_payment:
    :param period_months:
    :return:
    """
    interest_rate = normalize_rate(interest_rate)
    yearly_income = monthly_income * 12

    loan = Mortgage(
        property_value=property_value,
        downpayment=down_payment,
        yearly_income=yearly_income,
        rate=interest_rate,
    )

    payment_schedule = loan.get_payment_schedule(monthly_payment, period_months)

    schedule = ScheduleReport(payment_schedule)
    schedule_report = schedule.get_report()
    print(schedule_report)


if __name__ == "__main__":
    loan_simulation()
