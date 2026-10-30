# Lab 5 - Reflection

## 1. What is the purpose of static code analysis?
Static code analysis examines source code without executing it. It helps identify potential bugs, security vulnerabilities, coding standard violations, and maintainability problems at an early stage.

## 2. What did you learn from Pylint, Bandit, and Flake8?
Pylint checks code quality, naming conventions, documentation, and possible programming errors. Bandit identifies common security vulnerabilities in Python code. Flake8 checks code style and formatting issues such as indentation, spacing, and line length.

## 3. What were the major issues identified and how were they fixed?
The original program used unsafe pickle deserialization, broad and silent exception handling, mutable default arguments, global variables, missing docstrings, and inconsistent formatting. I replaced pickle with JSON, improved exception handling, organized the code using a class, added documentation, and corrected formatting issues. I also added validation for customer names, menu items, and order statuses.

## 4. What did you learn from this lab?
I learned that static analysis tools help improve code security, readability, and maintainability. Using multiple tools provides different perspectives on code quality. Fixing issues early makes software more reliable and easier to maintain.
