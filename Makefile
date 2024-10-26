format:
	uvx ruff check --fix .
	uvx ruff format .

lint:
	uvx ruff check .
	uvx ruff format --check .

test:
	uv run pytest -ra tests/ -sv --cov=cartesia/ --log-cli-level=INFO

bump:  # Use as `make bump version=<version>`
	uv run -m bumpversion $(version)
