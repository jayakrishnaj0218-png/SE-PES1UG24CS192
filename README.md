# PES1UG24CS192 – Software Engineering Lab Submissions

This repository contains the Software Engineering lab work for SRN **PES1UG24CS192**.

## Contents

- **Lab 1** – Requirements, use-case specification, and diagrams
- **Lab 2** – Jira evidence and documentation
- **Lab 3** – Component diagram and written justification
- **Lab 4** – Balloon Pop game: bug fixes, scoring, lives, timer, and restart functionality
- **Lab 5** – Static Code Analysis using Pylint, Bandit, and Flake8
- **Lab 6/7 – Code and Branch Coverage** – Blood Donation Screening application with statement and branch coverage tests
- **Lab 7 – Fuzz Testing** – Hypothesis property-based tests and hardened input-processing functions

Each lab is organized in its own folder.

## Repository Structure

```text
SE-PES1UG24CS192/
├── Lab-1/
├── Lab-2/
├── Lab-3/
├── Lab-4/
├── Lab-5/
├── Lab-6-7-Code-and-Branch-Coverage/
│   ├── blood_donation_screening.py
│   ├── CodeCoverageTest_blood_donation_screening.py
│   ├── BranchCoverageTest_blood_donation_screening.py
│   └── coverage reports and evidence
└── Lab7/
    ├── processor.py
    ├── test_processor.py
    ├── requirements.txt
    └── README.md
```

## Lab 7 — Fuzz Testing

Open the [Lab7 folder](./Lab7) for the application, Hypothesis tests, dependencies, and execution instructions.

Install and run from inside `Lab7`:

```bash
python -m pip install -r requirements.txt
python processor.py
python -m pytest -v test_processor.py
```
