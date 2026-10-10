# Employee Payroll Tracker: Implementation Flow

This document explains how the employee payroll tracker works, file by file
and step by step. The project demonstrates Python fundamentals together with
object-oriented programming concepts such as abstraction, inheritance,
encapsulation, polymorphism, properties, validation, lists, dictionaries,
loops, and dataclasses.

## 1. Project structure

```text
employee-payroll-tracker/
├── main.py
├── pyproject.toml
├── payroll_tracker/
│   ├── __init__.py
│   ├── employee.py
│   ├── payroll.py
│   └── utils.py
└── tests/
    └── test_payroll.py
```

Each file has one main responsibility:

- `main.py` runs the demonstration program.
- `employee.py` defines employees and their role-specific salary rules.
- `utils.py` contains small reusable calculation functions.
- `payroll.py` creates report records and formatted payslips.
- `__init__.py` defines the public package interface.
- `test_payroll.py` checks the important calculations and validation rules.
- `pyproject.toml` defines the package, Python version, and development tools.

## 2. The complete execution flow

When the command below is executed:

```text
poetry run python main.py
```

the flow is:

1. Python loads `main.py`.
2. The imports from `payroll_tracker` are resolved through
   `payroll_tracker/__init__.py`.
3. `main()` creates three different employee objects.
4. Each object validates its input while it is being constructed.
5. `build_payroll_records()` calculates payroll for every employee and stores
   the results in a dictionary keyed by employee ID.
6. `main()` prints a summary report by reading the dictionary.
7. `main()` generates and prints one payslip per employee.
8. The call to `main()` is protected by the
   `if __name__ == "__main__":` guard, so importing `main.py` does not
   automatically run the report.

The important design choice is that the reporting code does not need to know
whether an employee is full-time, a contractor, or an intern. It calls
`employee.calculate_salary()`, and Python selects the correct subclass method
automatically. This is polymorphism.

## 3. `main.py`: the application entry point

The import block brings the public classes and functions into the script:

```python
from payroll_tracker import (
    ContractEmployee,
    FullTimeEmployee,
    Intern,
    build_payroll_records,
    generate_payslip,
)
```

These names are available because they are re-exported by `__init__.py`.
Consequently, `main.py` does not need to know the internal locations of the
classes.

### Creating the employees

`main()` builds a list containing three objects:

```python
employees = [
    FullTimeEmployee("E001", "Ada Lovelace", 72_000, bonus=500),
    ContractEmployee("E002", "Grace Hopper", 75, hours_worked=160),
    Intern("E003", "Alan Turing", 1_200, tax=0),
]
```

The list is useful because it preserves the order in which the employees
should appear in the demonstration. The objects have different concrete
types, but they all share the `Employee` interface.

The numeric literal `72_000` is the same value as `72000`; the underscore
simply makes a large number easier to read.

Each constructor validates values:

- Ada has an annual salary of `72,000`, a bonus of `500`, and the default 20%
  tax.
- Grace has an hourly rate of `75`, 160 monthly hours, and the default 15%
  contractor tax.
- Alan has a monthly stipend of `1,200` and explicitly uses zero tax.

### Building records

```python
records = build_payroll_records(employees)
```

This function returns a dictionary like:

```text
{
    "E001": PayrollRecord(...),
    "E002": PayrollRecord(...),
    "E003": PayrollRecord(...),
}
```

Using employee IDs as dictionary keys makes it fast and direct to find a
record by ID. The function also rejects duplicate IDs instead of silently
overwriting one employee with another.

### Printing the summary

The program first prints a heading and then walks through the dictionary keys
with a `while` loop:

```python
employee_ids = list(records)
index = 0
while index < len(employee_ids):
    record = records[employee_ids[index]]
    ...
    index += 1
```

`list(records)` creates a list of dictionary keys. The integer `index` starts
at zero and moves forward after each iteration. The loop ends when `index`
reaches the number of IDs.

The formatted string prints:

- employee ID,
- employee name,
- role,
- net salary.

The format `:,.2f` adds thousands separators and always displays two decimal
places. For example, `5200` is displayed as `$5,200.00`.

### Printing payslips

The second loop is a `for` loop:

```python
for employee in employees:
    print(generate_payslip(employee))
    print("-" * 24)
```

For every employee, `generate_payslip()` returns a multiline string. The
separator makes the output easier to read.

## 4. `employee.py`: the employee hierarchy

### Imports and the abstract base class

```python
from abc import ABC, abstractmethod
from .utils import apply_tax
```

`ABC` allows `Employee` to be an abstract base class. `abstractmethod` marks
methods that every concrete employee type must implement. The relative import
`.utils` means “load `utils.py` from this same package.”

### The shared `Employee` constructor

`Employee.__init__()` stores the values common to all employees:

- `employee_id`
- `name`
- `salary`
- `bonus`
- `tax`

It first checks that the ID and name are not blank:

```python
if not employee_id.strip():
    raise ValueError("employee_id must not be empty")
```

`strip()` removes whitespace from the beginning and end. An empty string or a
string containing only spaces is rejected. `raise ValueError(...)` stops
construction and clearly tells the caller that the supplied value is invalid.

The constructor assigns `salary`, `bonus`, and `tax` through properties. That
is important: assigning `self.salary = salary` invokes the salary setter,
which performs validation before storing the value.

### Properties and encapsulation

The public property `salary` is backed by `_salary`:

```python
@property
def salary(self) -> float:
    return self._salary

@salary.setter
def salary(self, value: float) -> None:
    if value <= 0:
        raise ValueError("salary must be greater than 0")
    self._salary = float(value)
```

The same pattern is used for `bonus` and `tax`.

This provides controlled access:

- salary must be greater than zero;
- bonus cannot be negative;
- tax must be between `0` and `1`.

The values are converted to `float` so calculations use a consistent numeric
type. The leading underscore indicates that `_salary`, `_bonus`, and `_tax`
are internal storage attributes. Callers should use `employee.salary`,
`employee.bonus`, and `employee.tax`.

### Abstract members

`role` and `calculate_salary()` are abstract:

```python
@property
@abstractmethod
def role(self) -> str:
    ...

@abstractmethod
def calculate_salary(self) -> float:
    ...
```

This defines the contract for every employee subclass:

- it must provide a display role;
- it must provide its own salary calculation.

Because `Employee` has abstract members, it cannot be instantiated directly.
That prevents creating an employee with no meaningful salary rule.

### String representations

`__str__()` returns a human-readable form such as:

```text
Ada Lovelace (Full-time)
```

`__repr__()` returns a developer-oriented form containing the concrete class,
ID, name, and salary. These methods help when printing or debugging objects.

## 5. Role-specific salary calculations

### Full-time employees

`FullTimeEmployee` treats `salary` as an annual salary:

```python
monthly_gross = self.salary / 12 + self.bonus
return apply_tax(monthly_gross, self.tax)
```

For Ada:

```text
72,000 / 12 + 500 = 6,500 gross
6,500 * (1 - 0.20) = 5,200 net
```

### Contract employees

`ContractEmployee` adds `hours_worked` to the shared employee data. Its
constructor calls the parent constructor first:

```python
super().__init__(employee_id, name, salary, bonus, tax)
```

`super()` reuses the common validation instead of duplicating it.
`hours_worked` has its own validation and cannot be negative.

The calculation treats `salary` as an hourly rate:

```python
monthly_gross = self.salary * self.hours_worked + self.bonus
return apply_tax(monthly_gross, self.tax)
```

For Grace:

```text
75 * 160 = 12,000 gross
12,000 * (1 - 0.15) = 10,200 net
```

### Interns

`Intern` treats `salary` as a fixed monthly stipend:

```python
return apply_tax(self.salary + self.bonus, self.tax)
```

For Alan:

```text
1,200 + 0 bonus = 1,200 gross
1,200 * (1 - 0) = 1,200 net
```

All three methods have the same name, `calculate_salary()`, but the formulas
are different. This is method overriding and is the core of polymorphism.

## 6. `utils.py`: reusable calculations

### `calculate_salary()`

```python
def calculate_salary(base_salary: float, bonus: float = 0.0) -> float:
```

This function adds a base amount and a bonus. The bonus defaults to zero, so
callers can omit it when there is no bonus.

It rejects negative inputs because negative pay values do not make sense in
this model:

```python
if base_salary < 0 or bonus < 0:
    raise ValueError(...)
```

### `apply_tax()`

```python
return gross_salary * (1 - tax_rate)
```

The tax rate is represented as a decimal:

- `0.20` means 20%;
- `0.15` means 15%;
- `0` means no tax.

For gross pay of `100` and a tax rate of `0.20`, the result is `80`.
The function validates both the gross amount and the tax-rate range before
calculating.

Keeping these operations in a utility module avoids duplicating the same tax
logic in multiple classes.

## 7. `payroll.py`: records and payslips

### `PayrollRecord`

```python
@dataclass(frozen=True)
class PayrollRecord:
```

A dataclass automatically supplies useful methods such as an initializer and
a readable representation. The fields describe the data needed by the report:

- employee ID,
- employee name,
- role,
- gross salary,
- net salary.

`frozen=True` makes each record immutable after creation. This prevents report
data from being accidentally changed after payroll has been calculated.

### `build_payroll_records()`

The function creates an empty dictionary and processes employees one at a
time:

```python
records: dict[str, PayrollRecord] = {}
for employee in employees:
    ...
```

The duplicate check runs before inserting:

```python
if employee.employee_id in records:
    raise ValueError(...)
```

Then it calculates net pay through the employee object:

```python
net_salary = employee.calculate_salary()
```

This call is polymorphic. The actual method selected depends on the object's
runtime type.

Gross pay is reconstructed from net pay for the report:

```python
gross_salary = net_salary / (1 - employee.tax)
```

This reverses the tax formula:

```text
net = gross * (1 - tax)
gross = net / (1 - tax)
```

The function creates a `PayrollRecord` and stores it under the employee ID.
Finally, it returns the completed dictionary.

### `generate_payslip()`

This function follows the same calculation path but formats the result as
text. It calls `employee.calculate_salary()` without checking the concrete
class. It also calculates gross pay and includes the tax rate formatted as a
percentage:

```python
f"Tax rate: {employee.tax:.0%}"
```

For example, `0.2` becomes `20%`. The function returns one string containing
the employee details, gross pay, tax rate, and net pay.

## 8. `__init__.py`: the package interface

`__init__.py` imports selected names from the internal modules and lists them
in `__all__`.

This gives callers a simple public API:

```python
from payroll_tracker import Intern, build_payroll_records
```

Without this file, callers would need to import directly from
`payroll_tracker.employee` or `payroll_tracker.payroll`. The package interface
keeps the internal file organization separate from the way the application
uses the package.

## 9. Tests and what they prove

The tests use `pytest` and cover the main behavior:

1. Full-time salary uses annual salary divided by 12 and includes the bonus.
2. Contract salary uses hourly rate multiplied by hours worked.
3. Intern salary uses the monthly stipend.
4. Invalid salary, bonus, and tax values raise `ValueError`.
5. Utility functions calculate additions and tax correctly.
6. Payroll records are accessible by employee ID.
7. Duplicate employee IDs are rejected.

`pytest.approx()` is used for calculated decimal values. This is safer than
requiring exact floating-point equality in every case.

To run the tests:

```text
poetry run pytest
```

## 10. Configuration in `pyproject.toml`

The project requires Python 3.11 or newer:

```toml
requires-python = ">=3.11"
```

There are no production dependencies. `pytest` is listed as a development
dependency because it is needed only for testing:

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.0"
```

The Poetry package configuration tells Poetry to include the
`payroll_tracker` package when the project is installed.

## 11. Final mental model

The simplest way to remember the architecture is:

```text
main.py
  -> creates Employee subclasses
  -> build_payroll_records()
       -> employee.calculate_salary()
            -> subclass-specific formula
            -> apply_tax()
       -> PayrollRecord
  -> prints records
  -> generate_payslip()
       -> employee.calculate_salary()
       -> formats the result
```

The data flows from validated employee objects to calculated payroll values,
then into immutable report records or formatted payslip text. The employee
hierarchy owns the business rules, while `main.py` is responsible only for
assembling data and displaying the results.
