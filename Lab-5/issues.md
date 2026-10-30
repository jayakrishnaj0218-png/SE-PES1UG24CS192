# Lab 5 - Static Code Analysis

## Issues Identified and Fixes

| No. | Tool | Issue identified | Severity | Fix implemented |
|---|---|---|---|---|
| 1 | Bandit | B301: Unsafe use of pickle.load for restoring orders | Medium | Replaced pickle serialization with JSON backup and restore. |
| 2 | Bandit | B403: Use of the pickle module | Low | Removed the pickle import and used JSON instead. |
| 3 | Bandit | B110: try/except block silently suppressing errors | Low | Removed the silent exception handling and used explicit validation. |
| 4 | Pylint | Mutable default argument order_history=[] | Warning | Removed the mutable default and stored order history in the system instance. |
| 5 | Pylint | Global variables and global statements | Warning | Encapsulated orders, menu, and order ID inside FoodDeliverySystem. |
| 6 | Pylint | Missing module, function, and method docstrings | Convention | Added documentation strings throughout the program. |
| 7 | Pylint | Broad exception handling and file operations without encoding | Warning | Used specific exceptions, context managers, and UTF-8 encoding. |
| 8 | Pylint | Naming convention violations and old string formatting | Convention | Renamed printQueue to print_queue and used f-strings. |
| 9 | Flake8 | E302, E305, E501, and E722 formatting violations | Style | Corrected spacing, line lengths, and exception syntax. |
| 10 | Functional testing | Invalid order statuses and unknown menu items were accepted | Functional | Added order validation and status validation. |
| 11 | Functional testing | Empty customer names and empty orders were accepted | Functional | Added input validation before creating orders. |

## Final Analysis Results

- Bandit: No security issues identified after fixes.
- Pylint: 10.00/10.
- Flake8: No formatting violations.

## Conclusion

Static code analysis helped identify security risks, code-quality problems, and formatting violations. The fixes improved the security, readability, maintainability, and input validation of the food delivery system.
