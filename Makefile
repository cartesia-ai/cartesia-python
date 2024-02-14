install:
	pip install -e .

autoformat:
	black .
	isort --atomic .
	docformatter --in-place --recursive --black .

lint:
	isort -c .
	black . --check
	flake8 .