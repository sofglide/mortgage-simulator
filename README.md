# Mortgage simulator
> The mortgage simulator is a loan simulation program which follows Swedish rules

## Installation

Create the environment with `make env-create` then activate it with `source .venv/bin/activate`

Build the package with `make build`

Install the package with `pip install dist/mortgage_simulator-0.1.0.tar.gz`

## Usage example
* for a simulation by monthly payment and by mortgage term
  ```python
   mortgage_simulator simulate -v <HOUSE VALUE> -d <DOWN PAYMENT> -r <INTEREST RATE> -t <MORTGATE TERM IN YEARS> -i <INCOME> -p <MONTHLY PAYMENT>
  ```
* for the minimum monthly payment given a minimum amortization rate
  ```python
   mortgage_simulator minimum_payment -p <LOAN AMOUNT> -a <AMORTIZATION RATE> -i <INTEREST RATE>
  ```
