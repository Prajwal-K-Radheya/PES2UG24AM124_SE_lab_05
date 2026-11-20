# Static Analysis Findings

The line numbers below point to the original `parcel_tracker.py`, as it was
when the analysis tools were first run (before any fixes).

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection risk | Security (Bandit, high) | 55 | `pingHub` builds a shell command by joining in the hub address and runs it with `shell=True`. | Give ping its arguments as a list, choose the count flag for the current platform, and keep shell execution off. |
| Insecure temporary-file creation | Security (Bandit, medium) | 50 | `tempfile.mktemp` only hands back a filename without creating the file safely, which opens a race condition. | Switch to `NamedTemporaryFile(delete=False)` and return the path it allocates. |
| Mutable default argument | Code quality (Pylint) | 11 | The default history list is created once and shared by every call to `bookParcel`. | Default the argument to `None` and build a new list inside the function. |
| Broad exception handler | Code quality (Pylint) | 37 | Catching `Exception` during tracking-id lookup can mask unexpected errors. | Catch only `KeyError`, the failure expected for a missing id. |
| Predictable delivery OTP | Security (Bandit, low) | 72 | `random.randint` is not meant for security-sensitive values. | Produce the OTP with `secrets.randbelow`. |
| Subprocess module flagged | Security (Bandit, low) | 2 | Bandit warns about importing `subprocess`, even though the ping helper needs it. | Keep the import, find the executable with `shutil.which`, pass the address as a single list item with `shell=False`, and add narrow suppressions for the generic subprocess warnings. |
| Non-snake-case identifiers | Code quality (Pylint) | 11-67 | Function names, parameters and local variables are written in camelCase. | Rename them to snake_case and update every call site. |
| Missing docstrings | Code quality (Pylint) | 1, 11, 20, 27, 34, 43, 48, 53, 58 | The module and its functions have no docstrings. | Add short docstrings to the module and each function. |
| Status comparison simplification | Code quality (Pylint) | 45 | Two separate equality checks can be written as one membership test. | Replace them with `status in (...)`. |
| Missing operator whitespace | Style (Flake8 E225) | 28 | There are no spaces around the assignment operator. | Put a space on each side of `=`. |
| Inline-comment spacing | Style (Flake8 E261) | 71 | The inline comment is not preceded by two spaces. | Add two spaces before the `#`. |
| Comma spacing | Style (Flake8 E231) | 74 | A comma in the function call is not followed by a space. | Insert a space after the comma. |
| Top-level blank lines | Style (Flake8 E305) | 75 | The module-level call comes right after a function without two blank lines. | Add two blank lines and wrap the demo in an `if __name__ == "__main__":` guard. |

_Note: all findings above were addressed in the final code._
