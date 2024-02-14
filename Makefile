install:
	pip install -e .

autoformat:
	black cartesia/
	isort --atomic cartesia/
	docformatter --in-place --recursive --black cartesia/

lint:
	isort -c cartesia/
	black cartesia/ --check
	flake8 cartesia/