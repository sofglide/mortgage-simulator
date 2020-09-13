"""Console script for mortgage_simulator."""
import click

from .mortgage import Mortgage
from .simulation_report import SimulationReport
from .utils import normalize_rate

DEFAULT_DOWN_PAYMENT = 1000000
DEFAULT_INTEREST_RATE = 0.0150
DEFAULT_MORTGAGE_TERM_IN_YEARS = 25
DEFAULT_MONTHLY_INCOME = 40000
DEFAULT_MONTHLY_PAYMENT = 10000


def get_minimum_monthly_amortization(principal, amortization_rate):
    return amortization_rate / 12 * principal


def get_monthly_starting_interest(principal, interest):
    return interest / 12 * principal


@click.group()
def loan():
    pass


@loan.command(name="minimum_payment", help="calculate minimum required payment given amortization rate")
@click.option("-p", "--principal", type=int, required=True, help="principal")
@click.option("-a", "--amortization_rate", type=float, required=True, help="amortization rate")
@click.option(
    "-i",
    "--interest_rate",
    type=float,
    default=DEFAULT_INTEREST_RATE,
    show_default=True,
    help="interest rate",
)
def get_minimum_monthly_payment(principal, interest_rate, amortization_rate) -> None:
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


@loan.command("simulate", help="simulate mortgate given its parameters")
@click.option("-v", "--property_value", type=int, required=True, help="property value")
@click.option("-d", "--down_payment", type=int, default=DEFAULT_DOWN_PAYMENT, show_default=True, help="down payment")
@click.option(
    "-r",
    "--interest_rate",
    type=float,
    default=DEFAULT_INTEREST_RATE,
    show_default=True,
    help="interest rate",
)
@click.option(
    "-t",
    "--mortgage_term",
    type=int,
    default=DEFAULT_MORTGAGE_TERM_IN_YEARS,
    show_default=True,
    help="mortgage term in years",
)
@click.option(
    "-i",
    "--monthly_income",
    type=int,
    default=DEFAULT_MONTHLY_INCOME,
    show_default=True,
    help="monthly income",
)
@click.option(
    "-p",
    "--monthly_payment",
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

    simulations = SimulationReport()
    mutuo = Mortgage(
        value=property_value,
        downpayment=down_payment,
        income=yearly_income,
        rate=interest_rate,
    )

    simulation_by_payment = mutuo.simulate_by_payment(monthly_payment, title="monthly payment simulation")
    simulations.add_simulation(simulation_by_payment)

    simulation_by_minimum_payment = mutuo.simulate_by_payment(
        mutuo.minimum_monthly_payment, title="minimum payment simulation"
    )
    simulations.add_simulation(simulation_by_minimum_payment)

    simulation_by_term = mutuo.simulate_by_term(mortgage_term, title=f"term {mortgage_term:.1f} Y")
    simulations.add_simulation(simulation_by_term)

    click.echo(simulations.get_report())


if __name__ == "__main__":
    loan()
