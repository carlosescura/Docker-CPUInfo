EXPOSED_PORT := 8080
BUILD_TAG :=  cpu-info-test

.PHONY: help
help:
	@echo "make (build|run|run-daemon) [BUILD_TAG=] [EXPOSED_PORT=]"
	@echo "		e.g. make build BUILD_TAG=`echo $(BUILD_TAG)`"
	@echo " "

.PHONY: build 
build:
	docker build -t ${BUILD_TAG} .

.PHONY: run
run:
	docker run -p ${EXPOSED_PORT}:8080 ${BUILD_TAG}

.PHONY: run-daemon
run-daemon:
	docker run -d -p ${EXPOSED_PORT}:8080 ${BUILD_TAG}
