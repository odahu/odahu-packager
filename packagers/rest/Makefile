SHELL := /bin/bash
BUILD_TAG=latest

.EXPORT_ALL_VARIABLES:

## docker-build-rest-packager: Build REST packager docker image
docker-build-rest-packager:
	docker build -t odahu/packager-rest:${BUILD_TAG} -f containers/rest/Dockerfile .

## install-rest-packer: Instasll rest packer dependencies
install-rest-packer:
	cd packagers/rest && \
		rm -rf build dist *.egg-info && \
		pip3 install ${BUILD_PARAMS} -e . && \
		python setup.py sdist && \
		python setup.py bdist_wheel

## install-rest-packer-tests: Instasll rest packer test dependencies
install-rest-packer-tests:
	cd packagers/rest && pip install -e ".[testing]"

## lint-rest-packer: Start linting of rest packer
lint-rest-packer:
	pylint --ignore resources packagers/rest/odahuflow
	pylint packagers/rest/tests

## test-rest-packer: Start unit tests of rest packer
test-rest-packer:
	cd packagers/rest && pytest tests

## helm-delete-rest-packager: Delete rest packager helm release
helm-delete-rest-packager:
	helm delete --purge odahuflow-rest-packager || true

## helm-install-rest-packager: Install rest packager helm chart
helm-install-rest-packager: helm-delete-rest-packager
	helm install helms/odahuflow-rest-packager --name odahuflow-rest-packager --namespace odahuflow --debug -f helms/values.yaml --atomic --wait --timeout 120
