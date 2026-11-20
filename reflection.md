# Lab 5: Static Code Analysis — Reflection Answers

## 1. What is static code analysis, and why is it important?

Static code analysis inspects source code without running it. It catches
possible bugs, security weaknesses and style violations early, which keeps code
cleaner and easier to maintain.

## 2. What are the differences between Pylint, Bandit, and Flake8?

Pylint looks for code-quality problems and likely logic errors. Bandit scans
for common security vulnerabilities in Python code. Flake8 checks that the
formatting follows the PEP 8 style guide.

## 3. What challenges did you face while fixing the issues?

Some warnings only made sense once I understood what the code was doing. I also
had to make sure each fix left the program's behaviour unchanged, so I reran
the analysis tools after every round to confirm the warnings were gone.

## 4. How does static code analysis improve software quality?

It lets developers find problems early, tighten security, keep a consistent
coding style and write code that is easier to read and maintain. Running
several tools together covers a wider range of issues than any single one.

_Reflection reviewed and finalised._
