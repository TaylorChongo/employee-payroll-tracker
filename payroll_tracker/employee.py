"""Employee hierarchy and role-specific salary calculations."""

from abc import ABC, abstractmethod

from .utils import apply_tax


class Employee(ABC):
    """Common interface and validated payroll data for every employee."""

    def __init__(
        self,
        employee_id: str,
        name: str,
        salary: float,
        bonus: float = 0.0,
        tax: float = 0.2,
    ) -> None:
        if not employee_id.strip():
            raise ValueError("employee_id must not be empty")
        if not name.strip():
            raise ValueError("name must not be empty")
        self.employee_id = employee_id
        self.name = name
        self.salary = salary
        self.bonus = bonus
        self.tax = tax

    @property
    def salary(self) -> float:
        """Return the positive base salary or rate."""
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        if value <= 0:
            raise ValueError("salary must be greater than 0")
        self._salary = float(value)

    @property
    def bonus(self) -> float:
        """Return the non-negative bonus."""
        return self._bonus

    @bonus.setter
    def bonus(self, value: float) -> None:
        if value < 0:
            raise ValueError("bonus must not be negative")
        self._bonus = float(value)

    @property
    def tax(self) -> float:
        """Return the tax rate as a decimal between 0 and 1."""
        return self._tax

    @tax.setter
    def tax(self, value: float) -> None:
        if not 0 <= value <= 1:
            raise ValueError("tax must be between 0 and 1")
        self._tax = float(value)

    @property
    @abstractmethod
    def role(self) -> str:
        """Return the employee's display role."""

    @abstractmethod
    def calculate_salary(self) -> float:
        """Return this employee's net pay for the payroll period."""

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(employee_id={self.employee_id!r}, "
            f"name={self.name!r}, salary={self.salary!r})"
        )


class FullTimeEmployee(Employee):
    """Full-time employee whose salary is an annual amount."""

    @property
    def role(self) -> str:
        return "Full-time"

    def calculate_salary(self) -> float:
        # Annual salary is converted to a monthly amount before the bonus is added.
        monthly_gross = self.salary / 12 + self.bonus
        return apply_tax(monthly_gross, self.tax)


class ContractEmployee(Employee):
    """Contractor paid from an hourly rate and monthly hours."""

    def __init__(
        self,
        employee_id: str,
        name: str,
        salary: float,
        hours_worked: float,
        bonus: float = 0.0,
        tax: float = 0.15,
    ) -> None:
        super().__init__(employee_id, name, salary, bonus, tax)
        if hours_worked < 0:
            raise ValueError("hours_worked must not be negative")
        self.hours_worked = float(hours_worked)

    @property
    def role(self) -> str:
        return "Contract"

    def calculate_salary(self) -> float:
        # Contractors use salary as an hourly rate, so hours determine gross pay.
        monthly_gross = self.salary * self.hours_worked + self.bonus
        return apply_tax(monthly_gross, self.tax)


class Intern(Employee):
    """Intern paid a fixed monthly stipend."""

    @property
    def role(self) -> str:
        return "Intern"

    def calculate_salary(self) -> float:
        # Unlike the other employee types, an intern's salary is already monthly.
        return apply_tax(self.salary + self.bonus, self.tax)
