install:
	@poetry install
	@poetry run pre-commit install -f

test:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=./django_google_sso

ci:
	@poetry run pytest --cov=./django_google_sso

format:
	@poetry run black .

pre-commit:
	@poetry run pre-commit run --all

#############################
# SONAR COMMANDS            #
#############################
bandit-report:
	bandit --exit-zero --ignore-nosec -s B101 -x **/tests/**,**/venv/** --format json --output ./bandit-report.json --recursive .

dep-check-report:
	dependency-check -s . --exclude "**/__pycache__/**" -f HTML -f JSON

flake8-report:
	flake8 --exit-zero --output-file=flake8-report.json .

# Let test fail here, we will check the report.
pytest-report:
	@rm -rf .coverage
	@pytest --cov=. --ignore=migrations --cov-report xml --junit-xml=pytest-report.xml || true

sonar: bandit-report flake8-report pytest-report
	true
