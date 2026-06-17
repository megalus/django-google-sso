update:
	@uv lock --upgrade && uv run pre-commit autoupdate

install:
	@uv sync --active --dev
	@uv run --active pre-commit install -f

lint:
	@uv run --active pre-commit run --all

tests:
	@PYTHONPATH=. STELA_ENV=test uv run --active pytest -v -x -p no:warnings --cov-report term-missing --cov=.

test:
	@if [ "$(filter-out $@,$(MAKECMDGOALS))" = "" ]; then \
		echo "Usage: make test <path_to_test>. Example: make test django_google_sso/tests/test_conf.py::test_conf_from_settings"; \
		exit 1; \
	fi
	@echo "${BLUE}Running test: $(filter-out $@,$(MAKECMDGOALS))...${NC}"
	@PYTHONPATH=. STELA_ENV=test uv run --active pytest -v -x -p no:warnings --cov-report term-missing --cov=. $(filter-out $@,$(MAKECMDGOALS))
	@echo "${GREEN}Test completed.${NC}"

# Prevent make from treating the argument as a target
%:
	@:
