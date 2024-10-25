format:
	uvx ruff check --fix .
	uvx ruff format .

lint:
	uvx ruff check .
	uvx ruff format --check .

test:
	uvx pytest -ra tests/ -sv --cov=cartesia/ --log-cli-level=INFO
