import pytest

from payroll_tracker import ContractEmployee, FullTimeEmployee, Intern, build_payroll_records
from payroll_tracker.utils import apply_tax, calculate_salary


def test_full_time_salary_uses_annual_salary_and_bonus() -> None:
    employee = FullTimeEmployee("E1", "Ada", 72_000, bonus=500, tax=0.2)
    assert employee.calculate_salary() == pytest.approx(5_200)


def test_contract_salary_uses_hourly_rate_and_hours() -> None:
    employee = ContractEmployee("E2", "Grace", 75, 160, tax=0.15)
    assert employee.calculate_salary() == pytest.approx(10_200)


def test_intern_salary_is_a_monthly_stipend() -> None:
    employee = Intern("E3", "Alan", 1_200, tax=0)
    assert employee.calculate_salary() == pytest.approx(1_200)


def test_properties_reject_invalid_values() -> None:
    with pytest.raises(ValueError):
        FullTimeEmployee("E1", "Ada", 0)
    with pytest.raises(ValueError):
        FullTimeEmployee("E1", "Ada", 100, bonus=-1)
    with pytest.raises(ValueError):
        FullTimeEmployee("E1", "Ada", 100, tax=1.1)


def test_utility_functions_validate_and_calculate() -> None:
    assert calculate_salary(100, 25) == 125
    assert apply_tax(100, 0.2) == 80


def test_payroll_records_are_mapped_by_employee_id() -> None:
    records = build_payroll_records([Intern("E1", "Alan", 1_200, tax=0)])
    assert records["E1"].net_salary == 1_200


def test_duplicate_employee_ids_are_rejected() -> None:
    employees = [Intern("E1", "Alan", 1_200), Intern("E1", "Grace", 1_300)]
    with pytest.raises(ValueError, match="duplicate employee ID"):
        build_payroll_records(employees)
