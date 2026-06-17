
## Project Overview

Django Google SSO is a pluggable Django app that adds Google OAuth 2.0 authentication to Django admin and custom pages. It handles the full OAuth flow (PKCE, token exchange, user info retrieval), auto-creates users, manages permissions, and supports Django's Sites framework for multi-tenant setups.

## Architecture

The package is structured around three dataclass-based components:

- **`GoogleAuth`** (`main.py`): Manages the OAuth 2.0 flow — client config, token exchange, user info retrieval. Settings are resolved lazily via `get_sso_value()`, which supports both static values and callables that receive the `request`.
- **`UserHelper`** (`main.py`): Handles user lookup, creation, and updates. Wraps `get_or_create`, permission checks (staff/superuser lists), and `GoogleSSOUser` metadata persistence.
- **`GoogleSSOSettings`** (`conf.py`): PEP 562 module-level `__getattr__` pattern for lazy settings resolution. Each setting is a property that reads from `django.conf.settings` at access time, avoiding import-time coupling.

The OAuth flow in `views.py`: `start_login` -> Google consent -> `callback` (token fetch -> validate -> pre_create hook -> get_or_create_user -> pre_login hook -> login).

## Key Patterns

- **Callable settings**: Most `GOOGLE_SSO_*` settings accept either a static value or a callable `(request) -> value`, resolved at runtime via `GoogleAuth.get_sso_value()`. This supports multi-site configuration using `django.contrib.sites`.
- **Hook system**: Three hooks (`pre_validate`, `pre_create`, `pre_login`) let users inject custom logic without subclassing or monkey-patching. Hooks are configured via dotted Python path strings and dynamically imported at runtime.
- **Dataclass composition**: Both `GoogleAuth` and `UserHelper` are `@dataclass` classes holding `request` context, composed together in views rather than using inheritance.
- **Lazy config**: `conf.py` never accesses `django.conf.settings` at module import time — only when a property is accessed via `__getattr__`, preventing `AppRegistryNotReady` errors.

## Commands

```bash
make install        # Install deps + pre-commit hooks
make lint           # Run pre-commit (black, flake8, isort)
make tests          # Run full pytest suite
make test <path>    # Run a single test, e.g.: make test megalus/tests/test_base_views.py::test_health_check
make update         # Update dependencies and pre-commit hooks
```

## Testing Conventions

- To run tests, use `make tests` to run all tests or `make test <test_path>` to run a single test.
- If you need to run using pytest command directly, set `STELA_ENV=test`
- Tests are always syncronous (no `async` tests) and should avoid external API calls (mock them instead). Use `pytest-mock` for mocking.
- When resolving tests, always resolve warnings too.

## Lint and Formatting

- Check lint using command `make lint`.
- The command `make lint` runs `pre-commit run --all` under the hood.
- This means when `ruff` and `bandit` runs, they will try to fix the issues automatically.
- When checking for lint, if the first `make lint` returns errors, run the command again before making any manual changes.


## Code Style

- Python 3.13, Django 6.0, Ruff for deps.
- Always use type hints. Use `TypedDict` for dicts with 5+ keys. Use `Enum`/`Literal` for fixed values. Use `X | None` not `Optional[X]`.
- Google-style docstrings for functions/classes >7 lines.
- f-strings, double quotes, triple quotes for multi-line.
- Prefer dataclasses over regular classes.
- Always use English in code, comments, tests, commits, and docs. If non-English content is needed, put it in a separate file and use `gettext` for translation.

## Commit Messages

One-line, semantic prefix based on changed files:
- `feat:` — changes in `django-google-sso/` and `docs/`
- `refactor:` — changes in `django-google-sso/` without test changes
- `ci:` — changes only in `.github/`, or `pyproject.toml`
- `chore:` — changes outside `django-google-sso/` and `example_google_app/`
- `docs:` — changes only in `docs/` or `README.md`
