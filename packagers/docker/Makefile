SHELL := /bin/bash
BUILD_TAG=latest

.EXPORT_ALL_VARIABLES:

## docker-build-docker-packager: Build docker packager docker image
docker-build-docker-packager:
	docker build -t odahu/odahuflow-docker-packager:${BUILD_TAG} -f containers/docker-packager/Dockerfile .

## install-docker-packer: Instasll docker packer dependencies
install-docker-packer:
	cd packagers/docker && \
		rm -rf build dist *.egg-info && \
		pip3 install ${BUILD_PARAMS} -e . && \
		python setup.py sdist && \
		python setup.py bdist_wheel

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
	helm delete --purge odahuflow-docker-packager || true

## helm-install-docker-packager: Install docker packager helm chart
helm-install-docker-packager: helm-delete-docker-packager
	helm install helms/odahuflow-docker-packager --name odahuflow-docker-packager --namespace odahuflow --debug -f helms/values.yaml --atomic --wait --timeout 120
