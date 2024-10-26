format:
	uvx ruff check --fix .
	uvx ruff format .

lint:
	uvx ruff check .
	uvx ruff format --check .

test:
	uv run pytest -ra tests/ -sv --cov=cartesia/ --log-cli-level=INFO

bump:
	@if [ "$(filter $(MAKECMDGOALS),major minor patch pre_l pre_n)" = "" ]; then \
		echo "Error: Please specify a valid bump type (major|minor|patch|pre_l|pre_n)"; \
		exit 1; \
	fi
	uvx bump-my-version bump $(filter major minor patch pre_l pre_n,$(MAKECMDGOALS)) cartesia/version.py pyproject.toml

major minor patch pre_l pre_n:
	@:
