

all: flake cov


flake: rdbtools3 tests
	pyflakes3 rdbtools3 tests
	pep8 rdbtools3 tests


cov: rdbtools3 tests
	nosetests3 --with-coverage --cover-package=rdbtools3 \
		--cover-html --cover-html-dir=htmlcov


.PHONY: all flake
