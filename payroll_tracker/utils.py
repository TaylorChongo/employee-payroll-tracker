"""Small reusable payroll functions."""


def calculate_salary(base_salary: float, bonus: float = 0.0) -> float:
    """Combine a base amount and bonus into gross pay."""
    if base_salary < 0 or bonus < 0:
        raise ValueError("base_salary and bonus must not be negative")
    return base_salary + bonus


def apply_tax(gross_salary: float, tax_rate: float) -> float:
    """Return net pay after applying a decimal tax rate."""
    if gross_salary < 0:
        raise ValueError("gross_salary must not be negative")
    if not 0 <= tax_rate <= 1:
        raise ValueError("tax_rate must be between 0 and 1")
    # A 20% tax leaves 80% of gross pay, represented here as 1 - 0.20.
    return gross_salary * (1 - tax_rate)
