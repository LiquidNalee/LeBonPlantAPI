SHELL = /bin/bash


include build.env
export

GIT_HASH = $(shell git rev-parse --short HEAD)
GIT_BRANCH = $(shell git rev-parse --abbrev-ref HEAD | sed 's|^.*\/||g')

DEV_TAG = $(APP_VERSION)-$(GIT_BRANCH)

BUILD_ID = $(APP_VERSION)-$(GIT_HASH)
FINAL_APP_VERSION = $(BUILD_ID)
IMAGE_TAG = $(APP_VERSION)
USER_UID_USER_GID_BUILD_ARGS = --build-arg USER_UID=$(shell id -u $$USER) --build-arg USER_GID=$(shell id -g $$USER)

DOCKER_IMAGE_TEST = $(APP_NAME):$(IMAGE_TAG)-test
DOCKER_IMAGE_PROD = $(APP_NAME):$(IMAGE_TAG)

.DEFAULT_GOAL := all

## help: Display list of commands (from gazr.io)
.PHONY: help
help: Makefile
	@sed -n 's|^##||p' $< | column -t -s ':' | sed -e 's|^| |'

## all: Run all targets
.PHONY: all
all: init format style complexity test build

## version: Prints the version as x.y.z-commitHash
.PHONY: version
version:
	@printf "%s-%s" "$(APP_VERSION)" "$(GIT_HASH)"

## dev-version: Prints the version as ~ x.y.z-branchName
.PHONY: dev-version
dev-version:
	@printf "$(DEV_TAG)"

## init: Bootstrap your application. e.g. fetch some data files, make some API calls, request user input etc...
.PHONY: init
init:
	docker build --pull \
		--rm -t $(DOCKER_IMAGE_TEST) $(DOCKER_BUILD_CONTEXT) \
		-f Dockerfile \
		--target test \
		--build-arg APP_VERSION=$(FINAL_APP_VERSION) \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--build-arg USER=$(APP_NAME) \
		--build-arg APP_NAME=$(APP_NAME) \
		--build-arg BUILD_ID=$(BUILD_ID) \
		$(USER_UID_USER_GID_BUILD_ARGS) \
		&& docker tag  $(DOCKER_IMAGE_TEST) $(APP_NAME):latest

## style: Check lint, code styling rules. e.g. pylint, phpcs, eslint, style (java) etc ...
.PHONY: style
style:
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm -T --no-deps \
		app bash -c "mypy $(APP_NAME) tests"
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm -T --no-deps \
		app bash -c "flake8 $(APP_NAME) tests"
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm -T --no-deps \
	 	app bash -c "black --check ."

 ## Cyclomatic complexity (McCabe) and maintainability check
.PHONY: complexity
complexity:
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm -T --no-deps \
		app bash -c \
		"radon cc -s -n B $(APP_NAME) | tee /tmp/cc.txt && if [ -s /tmp/cc.txt ]; then exit 1; fi"

	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm -T --no-deps \
		app bash -c \
		"radon mi -n B $(APP_NAME) | tee /tmp/mi.txt && if [ -s /tmp/mi.txt ]; then exit 1; fi"

## format: Format code. e.g Prettier (js), format (golang)
.PHONY: format
format:
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm -T --no-deps \
	    	app bash -c "isort $(APP_NAME) tests; black ."

## test: Shortcut to launch all the test tasks (unit, functional and integration).
.PHONY: test
test:
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm \
		app bash -c "PGHOST=db PGUSER=${APP_NAME} PGDATABASE=${APP_NAME}_test PGPASSWORD=${APP_NAME}_pass PYTHONPATH=. ./wait-for-postgres.sh db pytest -Werror -s --cov . --cov-report term-missing --cov-report xml --junitxml=junit-coverage.xml --cov-config .coveragerc tests"

## test: Shortcut to launch all the test tasks (unit, functional and integration).
.PHONY: test-dev
test-dev:
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml run --rm \
		app bash -c "PGHOST=db PGUSER=${APP_NAME} PGDATABASE=${APP_NAME}_test PGPASSWORD=${APP_NAME}_pass PYTHONPATH=. ./wait-for-postgres.sh db pytest -Werror -s tests"

## build: Build the application.
.PHONY: build
build: ## Builds the docker image associated with the project
	docker build \
		--rm -t $(DOCKER_IMAGE_PROD) $(DOCKER_BUILD_CONTEXT) \
		-f Dockerfile \
		--target prod \
		--build-arg PYTHON_VERSION=$(PYTHON_VERSION) \
		--build-arg USER=$(APP_NAME) \
		--build-arg APP_NAME=$(APP_NAME) \
		--build-arg APP_VERSION=$(FINAL_APP_VERSION) \
		--build-arg BUILD_ID=$(BUILD_ID) \
		$(USER_UID_USER_GID_BUILD_ARGS)

## run: Locally run the application, e.g. node index.js, python -m myapp, go run myapp etc ...
.PHONY: run
run:
	-docker-compose -p $(APP_NAME) -f ./docker-compose.yml run $(DOCKER_COMPOSE_EXTRA_ENV) --service-ports app  # the dash ignore error code when CTRL-C is pressed

.PHONY: shell
shell:
	docker-compose -p $(APP_NAME) -f ./docker-compose.yml run $(DOCKER_COMPOSE_EXTRA_ENV) --rm app bash

.PHONY: shell-test
shell-test:
	docker-compose -p $(APP_NAME) -f ./docker-compose-dev.yml run $(DOCKER_COMPOSE_EXTRA_ENV) --rm app bash

## clean: Remove temporary files and docker images
.PHONY: clean
clean:
	## clean local files
	find . -type f -name "*.log" -exec rm {} + || true
	rm -rf coverage.xml junit-coverage.xml
	docker-compose -p $(APP_NAME)-dev -f docker-compose-dev.yml down -v --remove-orphans
	docker-compose -p $(APP_NAME) -f docker-compose.yml down -v --remove-orphans || true
	docker image prune -af --filter label=BUILD_ID=$(BUILD_ID) || true
