SHELL := /bin/bash

-include .env
include packagers/rest/Makefile

.DEFAULT_GOAL := help

## docker-build-resource-applier: Build resource applier docker image
docker-build-resource-applier:
	docker build -t odahuflow/resource-applier:${BUILD_TAG} -f containers/resource-applier/Dockerfile .

## install-vulnerabilities-checker: Install the vulnerabilities-checker
install-vulnerabilities-checker:
	./scripts/install-git-secrets-hook.sh install_binaries

## check-vulnerabilities: Сheck vulnerabilities in the source code
check-vulnerabilities:
	./scripts/install-git-secrets-hook.sh install_hooks
	git secrets --scan -r

## help: Show the help message
help: Makefile
	@echo "Choose a command run in "$(PROJECTNAME)":"
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sort | sed -e 's/\\$$//' | sed -e 's/##//'
	@echo
