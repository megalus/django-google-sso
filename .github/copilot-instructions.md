# Coding Guidelines
## Introduction
These are VS Code coding guidelines. For additional input please check the local file located at `.junie/guidelines.md`.

## Indentation
- Use four spaces for indentation. Do not use tabs.

## Localization
- Always use English in code, texts, tests, commits, docs and comments.
- If non english code is needed, put in a separate file and use `gettext` for translation.

## Code Style
- Follow PEP 8 guidelines for Python code style.
- Use `pre-commit run --all` for code formatting.
- Unless otherwise specified in pyproject.toml, line length is 92 characters.

## Types
- Always use type hints in the code.
- Always use TypeDicts for dictionaries.
- Always use dataclasses for objects.
- Always use `Enum` for fixed values. For single fixed value prefer `Literal`.
- Always use `|` for optional values.

## Comments
- Use comments to explain complex code.
- Use docstrings for functions and classes with more than seven lines of code.
- Use Google style for docstrings.

## Strings
- Use `f-strings` for string formatting.
- Use triple quotes for multi-line strings.
- Use double quotes for strings.

## Style
- Use `black` for code formatting, via `pre-commit run -all` command.

## Testing
- Use `pytest` for testing.
- Use `pytest.mark.parametrize` to avoid code duplication.

## Commits
- Use semantic versioning for commit messages. Create a one-line commit.
- Use `feat:` if commit creates new code in both ./django_google_sso and unit tests.
- Use `fix:` if commit only changes the code inside ./django_google_sso.
- Use `chore:` if commit changes files outside ./django_google_sso.
- Use `ci:` if commit changes files only in pyproject.toml.
- Use `docs:` if commit changes files only in ./docs or the README.
- Use `refactor:` if commit changes files in ./django_google_sso but not in unit tests.
- Use `BREAKING CHANGE:` if commit changes the minimum version of Python in pyproject.toml.
