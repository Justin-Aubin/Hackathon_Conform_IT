SHELL := /bin/bash

.DEFAUL_GOAL := help

.PHONY: bootstrap
bootstrap: ## Bootstrap the project in the virtual environment.
	@pipenv install --dev
	@pipenv update

.PHONY: clean
clean: ## Delete all intermediates and cached files.
	@rm --recursive --force *.egg-info build
	@find . -name '*.pyc' -type f -delete
	@find . -name '*.pyo' -type f -delete
	@find . -name '__pycache__' -type d -empty -delete
	@rm --recursive --force .pytest_cache
	@rm -f .coverage

.PHONY: help
help: ## Print the help and exit.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[96mmake %-20s\033[0m %s\n", $$1, $$2}'

.PHONY: mrproper
mrproper: clean ## Delete all generated files.
	@rm --recursive --force dist

.PHONY: precommit
precommit:
	@pipenv run pre-commit install
	@pipenv run pre-commit run

.PHONY: quality
quality: test precommit ## Run quality checks.
	@pipenv check
	@make test
	@pipenv run precommit

.PHONY: run
run: ## Run the project.
	@pipenv run python hackathon_it_concept/main.py

.PHONY: test
test:
	@pipenv run pytest
