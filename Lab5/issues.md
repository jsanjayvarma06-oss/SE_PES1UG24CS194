# Issues Found — shuttle_system.py

Pylint score: 6.25/10 before → 10.00/10 after. Bandit: 2 issues → 0. Flake8: 10 issues → 0.

| # | Issue | Type | Tool / Code | Line(s) | Description | Fix Approach |
|---|-------|------|-------------|---------|-------------|--------------|
| 1 | Bare `except: pass` | Bug / Security (High) | Bandit B110, Pylint W0702, Flake8 E722 | 29-30 | Silently swallowed errors, hiding the TypeError caused by `"full"` being stored as a passenger count | Removed try/except; `average_load()` returns `None` for empty/unknown routes and the caller checks it |
| 2 | No input validation | Logic bug (High, not flagged by tools) | Manual | 11-14, 48-52 | `-6` and `"full"` were accepted; R2 trips became `[4, -6]` and R3 data was corrupted | Validate type and range (0–MAX_CAPACITY) in `add_trip_log`; reject bad trips with a clear message |
| 3 | KeyError crash on removed/unknown route | Logic bug (High, not flagged by tools) | Manual | 57-58 | `average_load("R3")` after `remove_route("R3")` crashed; typing an unknown route (e.g. P3) also crashed | Membership checks before lookup; `remove_route` uses `dict.pop(key, None)` |
| 4 | Mutable default argument | Bug (Medium) | Pylint W0102 | 11 | `logs=[]` is shared across every call, so logs leak between callers | Default to `None` and create a new list inside the function |
| 5 | Insecure random generator | Security (Low) | Bandit B311 | 35 | `random.choice` is not cryptographically secure | Replaced with `secrets.choice` |
| 6 | Files opened without `with` / encoding | Bug (Medium) | Pylint R1732, W1514 | 39, 42 | File handles could leak (second file was never closed); platform-dependent encoding | `with open(..., encoding="utf-8")` plus `json.dump` / `json.load` |
| 7 | `global` statement | Design (Medium) | Pylint W0603 | 38 | Reassigning a global from inside a function | Mutate the dict with `clear()` / `update()`; parameter renamed from `file` to `path` |
| 8 | Bad name and unused argument | Style | Pylint C0103, W0613 | 33 | camelCase `assignDriver`; `route_id` never used | Renamed to `assign_driver()` and removed the unused parameter |
| 9 | Old `%` string formatting | Style | Pylint C0209, Flake8 E501 | 13 | `%`-formatting, and the line was 82 characters long | Replaced with an f-string under 79 characters |
| 10 | Missing docstrings | Style | Pylint C0114, C0116 | 1, 11, 16, 19, 23, 33, 37, 45 | Module and functions had no documentation | Added module and function docstrings |
| 11 | Blank lines between definitions | Style | Flake8 E302, E305 | 11-45, 60 | Only one blank line between top-level functions | Two blank lines before every top-level definition |
| 12 | Code runs on import | Design | Manual | 60 | `main()` executed whenever the module was imported | Wrapped in `if __name__ == "__main__":` |
