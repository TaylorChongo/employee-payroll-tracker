"""Payroll record creation and payslip formatting."""

from dataclasses import dataclass

from .employee import Employee
from .utils import calculate_salary


@dataclass(frozen=True)
class PayrollRecord:
    """Dictionary-friendly summary of one employee's payroll."""

    employee_id: str
    employee_name: str
    role: str
    gross_salary: float
    net_salary: float


def generate_payslip(employee: Employee) -> str:
    """Generate a readable payslip using polymorphic salary calculation."""
    net_salary = employee.calculate_salary()
    # Reverse the tax calculation to display gross pay from the net result.
    gross_salary = calculate_salary(net_salary / (1 - employee.tax), 0)
    return (
        f"Employee: {employee.name}\n"
        f"ID: {employee.employee_id}\n"
        f"Role: {employee.role}\n"
        f"Gross salary: ${gross_salary:,.2f}\n"
        f"Tax rate: {employee.tax:.0%}\n"
        f"Net salary: ${net_salary:,.2f}"
    )


def build_payroll_records(employees: list[Employee]) -> dict[str, PayrollRecord]:
    """Build a mapping from employee IDs to payroll records."""
    records: dict[str, PayrollRecord] = {}
    for employee in employees:
        # IDs are the dictionary keys, so duplicates would silently overwrite data.
        if employee.employee_id in records:
            raise ValueError(f"duplicate employee ID: {employee.employee_id}")
        net_salary = employee.calculate_salary()
        # Each employee subclass computes net pay differently, but shares this tax model.
        gross_salary = net_salary / (1 - employee.tax)
        records[employee.employee_id] = PayrollRecord(
            employee.employee_id,
            employee.name,
            employee.role,
            gross_salary,
            net_salary,
        )
    return records
