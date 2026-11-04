# Lab 6 & 7 — Code and Branch Coverage

**Student:** J Jayakrishna  
**SRN:** PES1UG24CS192  
**Assigned application:** Blood Donation Screening

## Files

- `blood_donation_screening.py` — application module from the faculty-assigned repository.
- `CodeCoverageTest_blood_donation_screening.py` — tests for statement/line execution.
- `BranchCoverageTest_blood_donation_screening.py` — tests for decision outcomes.
- `requirements.txt` — dependencies.
- `code_coverage_report.txt` and `branch_coverage_report.txt` — locally generated coverage report output.

## Install

```bash
python -m pip install -r requirements.txt
```

## Code coverage

```bash
coverage erase
coverage run --source=blood_donation_screening -m pytest -q CodeCoverageTest_blood_donation_screening.py
coverage report -m
```

## Branch coverage

```bash
coverage erase
coverage run --branch --source=blood_donation_screening -m pytest -q BranchCoverageTest_blood_donation_screening.py
coverage report -m
```

## Locally verified results

- Code coverage suite: 17 tests passed; application line coverage 100% (45/45 statements).
- Branch coverage suite: 18 tests passed; branch coverage 100% (32/32 branches; 0 partial).

**Screenshot note:** The handout requires terminal screenshots. Run the commands above in a visible terminal and capture the results for submission; text reports are included here but are not substitutes for screenshots.
