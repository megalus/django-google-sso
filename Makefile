update:
	@poetry update && poetry run pre-commit autoupdate

install:
	@poetry install
	@poetry run pre-commit install -f

lint:
	@poetry run pre-commit run --all

tests:
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=.

test:
	@if [ "$(filter-out $@,$(MAKECMDGOALS))" = "" ]; then \
		echo "Usage: make test <path_to_test>. Example: make test megalus/tests.py::test_health_check"; \
		exit 1; \
	fi
	@echo "${BLUE}Running test: $(filter-out $@,$(MAKECMDGOALS))...${NC}"
	@poetry run pytest -v -x -p no:warnings --cov-report term-missing --cov=. $(filter-out $@,$(MAKECMDGOALS))
	@echo "${GREEN}Test completed.${NC}"

# Prevent make from treating the argument as a target
%:
	@:
