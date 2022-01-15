##############################################################################################
# PROJECT-SPECIFIC PARAMETERS                                                                #
##############################################################################################


PROJECT_NAME = mortgage_simulator
PYTHON ?= python3
SOURCE_FOLDER = mortgage_simulator

##############################################################################################
# ENVIRONMENT SETUP                                                                          #
##############################################################################################


.PHONY: env-create
env-create:
	$(PYTHON) -m venv .venv --prompt $(PROJECT_NAME)
	make env-update
	#
	# Don't forget to activate the environment before proceeding! You can run:
	# source .venv/bin/activate


.PHONY: env-update
env-update:
	bash -c "\
		. .venv/bin/activate; \
		which python; \
		which pip; \
		pip install --upgrade -r requirements.txt; \
		pip freeze; \
	"


.PHONY: env-delete
env-delete:
	rm -rf .venv


.PHONY: update
update:
	pip install --upgrade -r requirements.txt


##############################################################################################
# BUILD STEPS: LINTING, TESTING, COVERAGE, DOCS                                              #
##############################################################################################


.PHONY: build-all
build-all: clean lint docs build


.PHONY: clean
clean:
	rm -f .gitinfo
	rm -rf build dist *.egg-info
	find $(SOURCE_FOLDER) -name __pycache__ | xargs rm -rf
	find $(SOURCE_FOLDER) -name '*.pyc' -delete
	rm -rf reports .coverage
	rm -rf docs/build docs/source
	rm -rf .*cache


.PHONY: reformat
reformat:
	isort $(SOURCE_FOLDER) tests
	black $(SOURCE_FOLDER) tests


.PHONY: lint
lint:
	$(PYTHON) -m pycodestyle . --exclude '.venv,setup.py,docs/*'
	isort --check-only $(SOURCE_FOLDER) tests
	black --check $(SOURCE_FOLDER) tests
	pylint $(SOURCE_FOLDER)
	pylint --disable=missing-docstring,no-self-use tests
	mypy $(SOURCE_FOLDER)


.PHONY: test
test:
	$(PYTHON) -m pytest tests/


.PHONY: build
build:
	python setup.py --quiet sdist bdist_wheel


##############################################################################################
# VERSIONING                                                                                 #
##############################################################################################


.PHONY: version
version:
	python -c "import $(SOURCE_FOLDER); print($(SOURCE_FOLDER).__version__)"


.PHONY: bump-version-patch
bump-version-patch:
	# Note: You should only run this on a clean working copy
	#       If this operation succeeds, it will create a version-bumping commit
	bump2version patch --list
	git log --oneline -1


.PHONY: bump-version-minor
bump-version-minor:
	# Note: You should only run this on a clean working copy
	#       If this operation succeeds, it will create a version-bumping commit
	bump2version minor --list
	git log --oneline -1

.PHONY: bump-version-major
bump-version-major:
	# Note: You should only run this on a clean working copy
	#       If this operation succeeds, it will create a version-bumping commit
	bump2version major --list
	git log --oneline -1


