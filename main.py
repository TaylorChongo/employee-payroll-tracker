"""Command-line demonstration for the employee payroll tracker."""

from payroll_tracker import (
    ContractEmployee,
    FullTimeEmployee,
    Intern,
    build_payroll_records,
    generate_payslip,
)


def main() -> None:
    """Process a list of employees and print their payroll report."""
    employees = [
        FullTimeEmployee("E001", "Ada Lovelace", 72_000, bonus=500),
        ContractEmployee("E002", "Grace Hopper", 75, hours_worked=160),
        Intern("E003", "Alan Turing", 1_200, tax=0),
    ]
    records = build_payroll_records(employees)

    print("EMPLOYEE PAYROLL REPORT")
    print("=" * 24)
    employee_ids = list(records)
    index = 0
    while index < len(employee_ids):
        # Use the ID list to look up each record while keeping the loop index explicit.
        record = records[employee_ids[index]]
        print(
            # Commas and the .2f specifier keep salary output readable and consistent.
            f"{record.employee_id} | {record.employee_name} | "
            f"{record.role} | Net: ${record.net_salary:,.2f}"
        )
        index += 1

    print("\nPAYSLIPS")
    print("=" * 8)
    for employee in employees:
        print(generate_payslip(employee))
        print("-" * 24)


if __name__ == "__main__":
    main()
