SHELL := /bin/bash
BUILD_TAG=latest
PIP_EXTRA_INDEX_URL=

-include .env

.DEFAULT_GOAL := help

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

## docker-build-docker-packager: Build docker packager docker image
docker-build-docker-packager:
	docker build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} -t odahu/odahu-flow-packagers:${BUILD_TAG} -f containers/docker-packager/Dockerfile .

## docker-push-docker-packager-base: Push docker image
docker-push-docker-packager:
	docker tag odahu/odahu-flow-packagers:${BUILD_TAG} ${DOCKER_REGISTRY}/odahu/odahu-flow-packagers:${TAG}
	docker push ${DOCKER_REGISTRY}/odahu/odahu-flow-packagers:${TAG}

## docker-build-docker-packager-base: Build docker packager base docker image
docker-build-docker-packager-base:
	docker build -t odahu/odahu-flow-docker-packager-base:${BUILD_TAG} -f containers/docker-packager-base/Dockerfile .

## docker-push-docker-packager-base: Push docker image
docker-push-docker-packager-base:
	docker tag odahu/odahu-flow-docker-packager-base:${BUILD_TAG} ${DOCKER_REGISTRY}/odahu/odahu-flow-packager-base:${TAG}
	docker push ${DOCKER_REGISTRY}/odahu/odahu-flow-packager-base:${TAG}

## install-docker-packer: Installs docker packer dependencies
install-docker-packer:
	cd packagers && \
		pip3 install ${BUILD_PARAMS} -e .

## install-docker-packer-tests: Instasll docker packer test dependencies
install-docker-packer-tests:
	cd packagers && pip install -e ".[testing]"

## lint-docker-packer: Start linting of docker packer
lint-docker-packer:
	pylint --ignore resources packagers/odahuflow
	pylint tests

## test-docker-packer: Start unit tests of docker packer
test-docker-packer: docker-build-docker-packager-base
	pytest tests

## helm-delete-docker-packager: Delete docker packager helm release
helm-delete-docker-packager:
	helm delete --purge odahu-flow-packagers || true

## helm-install-docker-packager: Install docker packager helm chart
helm-install-docker-packager: helm-delete-docker-packager
	helm install helms/odahu-flow-packagers --name odahu-flow-packagers --namespace odahuflow --debug -f helms/values.yaml --atomic --wait --timeout 120
