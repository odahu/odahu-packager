SHELL := /bin/bash

-include .env
include packagers/docker/Makefile

.DEFAULT_GOAL := help

## install-vulnerabilities-checker: Install the vulnerabilities-checker
install-vulnerabilities-checker:
	./scripts/install-git-secrets-hook.sh install_binaries

## check-vulnerabilities: Сheck vulnerabilities in the source code
check-vulnerabilities:
	./scripts/install-git-secrets-hook.sh install_hooks
	git secrets --scan -r


## docker-build: Build docker image
docker-build-base:
	docker build -t odahu/odahu-flow-packager-base:${BUILD_TAG} -f containers/docker-packager-base/Dockerfile .

## docker-push-api: Push docker image
docker-push-base:
	docker tag odahu/odahu-flow-packager-base:${BUILD_TAG} ${DOCKER_REGISTRY}/odahu/odahu-flow-packager-base:${TAG}
	docker push ${DOCKER_REGISTRY}/odahu/odahu-flow-packager-base:${TAG}

## help: Show the help message
help: Makefile
	@echo "Choose a command run in "$(PROJECTNAME)":"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo
