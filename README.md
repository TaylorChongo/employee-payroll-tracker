# Employee Payroll Tracker

This project implements the lab specification with Python 3.11+ and Poetry.
It has been verified with Python 3.14.8.
It demonstrates lists, dictionaries, arithmetic, conditionals, loops,
functions, inheritance, encapsulation, polymorphism, properties, validation,
and a small command-line report.

## Project structure

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

## Setup with Poetry

Install Poetry if it is not already available, then run:

```text
poetry install
poetry run python main.py
poetry run pytest
```

The project-local `poetry.toml` sets `virtualenvs.in-project = true`, so Poetry
creates and manages the virtual environment in `.venv` inside this project.
Use `poetry run ...` to execute commands in that environment without
activating it manually. The project has no production dependencies; `pytest`
is a development dependency.

To confirm the interpreter selected by Poetry:

```text
poetry run python --version
```

The expected output for the verified environment is `Python 3.14.8`.

## Payroll rules

The specification does not prescribe numeric business rules, so this example
uses explicit, easy-to-check rules:

- Full-time: annual salary divided by 12, plus the bonus; default tax is 20%.
- Contract: hourly salary multiplied by monthly hours, plus the bonus; default
  tax is 15%.
- Intern: monthly stipend plus the bonus; default tax is 20%.

Tax rates are decimals between `0` and `1`. For example, `0.2` means 20%.
These rules can be changed in the employee subclasses without changing the
reporting code.

## Design notes

`Employee` is an abstract base class. Each subclass overrides
`calculate_salary()`, so `generate_payslip()` can work with any employee
without checking its concrete type. This is polymorphism.

Salary, bonus, and tax are exposed through `@property` methods backed by
private attributes. Their setters reject invalid values, keeping payroll data
valid when it is created or updated.

The application stores employees in a list and creates a dictionary keyed by
employee ID for fast payroll lookup. The report uses a `while` loop to walk
through the dictionary keys and a `for` loop to generate individual payslips.

`calculate_salary()`, `apply_tax()`, and `generate_payslip()` are separated
into reusable modules. The `PayrollRecord` dataclass provides a stable,
readable data structure for report data.

## Debugging in VS Code

1. Open this folder in VS Code.
2. Run `poetry install` in the integrated terminal.
3. Set a breakpoint in `payroll_tracker/employee.py` inside one of the
   `calculate_salary()` methods.
4. Start `main.py` with the Python debugger.
5. Inspect `employee.salary`, `employee.bonus`, `employee.tax`, and the
   `monthly_gross` or `net_salary` local value.
6. Use Step Over to observe that the same method call dispatches to different
   subclass implementations.

The IDE screenshot or video requested by the assignment must be captured from
your own debugging session.

## Expected report

Running `poetry run python main.py` prints a report containing the three
employee roles, their net salaries, and a detailed payslip for each employee.
