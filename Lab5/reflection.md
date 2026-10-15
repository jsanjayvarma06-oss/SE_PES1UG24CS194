# Reflection

**1. Which issues were the easiest to fix, and which were the hardest? Why?**
Style issues (blank lines, f-strings, docstrings, snake_case names) were the easiest because each warning points to an exact line and the fix is mechanical. The hardest was the bare `except: pass` in `underused_routes()`. When I replaced it with specific exceptions, the program printed "Could not compute load for R3: unsupported operand type(s) for +: 'int' and 'str'", which showed the except block had been hiding a real data bug: the string "full" was stored as a passenger count. Fixing it properly meant adding input validation and making `average_load()` handle empty routes, not just changing the except line.

**2. Did the static analysis tools report any false positives? If so, describe one example.**
Bandit's B311 warning on `random.choice` is effectively a false positive here: picking a shuttle driver has no security impact, so a non-cryptographic generator is acceptable. I still switched to `secrets.choice` because it costs nothing, though `# nosec B311` with a justification would also be reasonable. The opposite also happened: the tools missed real bugs. None of them flagged that -6 and "full" were accepted as passenger counts, or the KeyError crash when looking up R3 after it was removed. I only found those by running the program.

**3. How would you integrate static analysis tools into your actual software development workflow?**
Locally, I would run Flake8 and Pylint through a pre-commit hook so issues are caught before each commit, and enable them in VS Code for instant feedback. In CI (e.g. GitHub Actions), I would run Pylint with `--fail-under=9.5`, Flake8, and Bandit on every push and pull request, and block merges if any fail. Rules would live in a shared config file (`.pylintrc` / `setup.cfg`) so the whole team uses the same standards.

**4. What tangible improvements did you observe in code quality, readability, or potential robustness after applying the fixes?**
The Pylint score went from 6.25/10 to 10.00/10, Bandit went from 2 issues to 0, and Flake8 from 10 issues to 0. The program no longer crashes on a removed route or an unknown route typed by the user; it rejects invalid trips like -6 and "full" with a clear message instead of silently corrupting averages. Each call to `add_trip_log` now gets its own log list, files are always closed, and the global reassignment is gone. Docstrings, f-strings and consistent naming make the code much easier to read and maintain.
