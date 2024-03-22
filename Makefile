install:
	pip install -e .

install-dev:
	pip install -e .[dev]


autoformat:
	black .
	isort --atomic .
	docformatter --in-place --recursive --black .

lint:
	isort -c .
	black . --check
	flake8 .

test:
	pytest -ra tests/ --ignore=tests/integration --cov=src/