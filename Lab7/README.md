# Lab 7 — Fuzzing for Input Validation Bugs

**Student:** J Jayakrishna  
**SRN:** PES1UG24CS192  
**Course:** Software Engineering Lab

## Objective
Use Hypothesis property-based fuzzing to discover edge cases in three input-processing functions, harden the application, and rerun the tests.

## Functions
1. `parse_int_list(value)`: validates and parses comma-separated integers.
2. `calculate_average(values)`: validates a non-empty iterable of finite numeric values.
3. `normalize_username(value)`: validates and normalizes ASCII usernames.

## Installation
```bash
python -m pip install hypothesis pytest
```

## Required workflow
Run these commands from this directory.

1. Run the processor demonstration:
   ```bash
   python processor.py
   ``
2. Run the property tests:
   ```bash
   python -m pytest -v test_processor.py
   ```
3. The handout asks for an initial failing-test screenshot before fixing the application. The current `processor.py` is the hardened version, so use the prior starter code supplied by your instructor (if provided) for that initial stage. Do not label the passing test run as a failing run.
4. Run the fixed processor:
   ```bash
   python processor.py
   ``
5. Rerun the tests and capture the passing output:
   ```bash
   python -m pytest -v test_processor.py
   ```

## What the tests check
- Round-trip correctness for valid parsed integer lists.
- Safe rejection of malformed text and non-string input.
- Average bounds, empty-input handling, numeric validation, and non-finite values.
- Username length, allowed characters, ASCII restriction, first-character rule, and whitespace normalization.

## Submission evidence
The handout requires a PDF containing screenshots of:
- Initial processor execution.
- Failing tests against the original buggy starter program.
- Fixed processor execution.
- Passing tests against the fixed program.

Capture genuine terminal screenshots on the computer used to execute the commands. The repository includes source and test files; the PDF evidence should not contain fabricated terminal output.
