

all: flake doc cov


flake: rdbtools3 tests
	pyflakes3 rdbtools3 tests
	pep8 rdbtools3 tests


cov:
	true


.PHONY: all flake
