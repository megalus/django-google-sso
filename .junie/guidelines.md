Project runs on a virtualenv inside WSL. Python interpreter can be found using command `poetry env info`.

Test runner is `pytest`. To run can use command `make tests` to run all or `make test <path>::<test>`, but you need docker to runs these commands. Without docker, activate the virtualenv and run `pytest -v` directly.

Always check code for the `django` versions defined in pyproject.toml.

Always use type hints in the code. Always use TypeDicts for dictionaries.

Always use dataclasses for objects.

Always add docstrings in functions with more than seven lines of code. Use Google style.

Linter packages are managed by [pre-commit library](https://github.com/pre-commit/pre-commit). Use `make lint` to check for linter and format errors.

The default python version for this project is 3.12.11.

When creating Javascript always use JQuery.

This is a public python library hosted in PyPI. All configuration is inside `pyproject.toml` file.

Use semantic versioning for commit messages. Create a one-line commit. Do not use "`".

Use `feat:` if commit creates new code in both ./django_google_sso and unit tests.

Use `fix:` if commit only changes the code inside ./django_google_sso.

Use `chore:` if commit changes files outside ./django_google_sso.

Use `ci:` if commit changes files only in pyproject.toml.

Use `docs:` if commit changes files only in ./docs or the README.

Use `refactor:` if commit changes files in ./django_google_sso but not in unit tests.

Use `BREAKING CHANGE:` if commit changes the minimum version of Python or Django in pyproject.toml.

Project versioning is done during GitHub actions `.github/publish.yml` workflow, using the [auto-changelog](https://github.com/KeNaCo/auto-changelog) library.

Always update the README at the root of the project.

README always contains [shields.io](https://shields.io/docs) badges for (when applicable): python versions, django versions, pypi version, license and build status.

Prefer use mermaid diagrams on docs.

Always use English on code, comments, docstrings and documentation.

The README always contains the minimal configuration for the library to work.

Always write the README for developers with no or low experience with Django, Google APIs and OAuth2, but be pragmatic and short. The README should be a quick start guide for developers to use the library.

The ./docs folder contains detailed instructions of how to use the library, including examples and diagrams. Reading order for the markdown files is located in mkdocs.yml at `nav` key. On these docs you can be very didactic.

The folder `example_google_app` contains a minimal Django app using the library. It can be used as a reference for the documentation. Use their own README.md and settings.py as a reference for how to use.
