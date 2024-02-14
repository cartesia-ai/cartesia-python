install:
	pip install -e .

autoformat:
	black src/ tests/
	isort --atomic src/ tests/
	docformatter --in-place --recursive --black src

lint:
	isort -c src/ tests/
	black src/ tests/ --check
	flake8 src/ tests/