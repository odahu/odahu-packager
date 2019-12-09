SHELL := /bin/bash
BUILD_TAG=latest
PIP_EXTRA_INDEX_URL=

-include .env
.EXPORT_ALL_VARIABLES:

## docker-build-docker-packager: Build docker packager docker image
docker-build-docker-packager:
	docker build --build-arg PIP_EXTRA_INDEX_URL=${PIP_EXTRA_INDEX_URL} -t odahu/odahu-flow-packagers:${BUILD_TAG} -f containers/docker-packager/Dockerfile .

## install-docker-packer: Instasll docker packer dependencies
install-docker-packer:
	cd packagers/docker && \
		pip3 install ${BUILD_PARAMS} -e .

## install-docker-packer-tests: Instasll docker packer test dependencies
install-docker-packer-tests:
	cd packagers/docker && pip install -e ".[testing]"

## lint-docker-packer: Start linting of docker packer
lint-docker-packer:
	pylint --ignore resources packagers/docker/odahuflow
	pylint packagers/docker/tests

## test-docker-packer: Start unit tests of docker packer
test-docker-packer:
	cd packagers/docker && pytest tests

## helm-delete-docker-packager: Delete docker packager helm release
helm-delete-docker-packager:
	helm delete --purge odahu-flow-packagers || true

## helm-install-docker-packager: Install docker packager helm chart
helm-install-docker-packager: helm-delete-docker-packager
	helm install helms/odahu-flow-packagers --name odahu-flow-packagers --namespace odahuflow --debug -f helms/values.yaml --atomic --wait --timeout 120
