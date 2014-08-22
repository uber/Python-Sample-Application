.PHONY: bootstrap clean lint test
.DEFAULT_GOAL := test

test: clean lint
	@py.test -s test/

lint:
	@flake8 .

clean:
	@find . -type f -name '*.pyc' -delete

bootstrap:
	@pip install -r requirements.txt
	@pip install -r requirements-test.txt
	@python setup.py develop
