PYFLAKES ?= pyflakes3
PEP8 ?= pep8
NOSE ?= nosetests3

all: flake cov


flake: rdbtools3 tests
	$(PYFLAKES) rdbtools3 tests
	$(PEP8) rdbtools3 tests


cov: rdbtools3 tests
	$(NOSE) --with-coverage --cover-package=rdbtools3 \
		--cover-html --cover-html-dir=htmlcov

test: rdbtools3 tests
	$(NOSE) -v


doc: docs/*
	make -C docs html


.PHONY: all flake
