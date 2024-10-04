install:
	pip install -e .

install-dev:
	pip install -e '.[dev]'
	pip install pytest pytest-cov

autoformat:
	isort --atomic .
	ruff format .

lint:
	isort -c .
	ruff check .
	ruff format --check .

test:
	pytest -ra tests/ -sv --cov=cartesia/ --log-cli-level=INFO
