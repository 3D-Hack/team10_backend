PROJECT = $(shell pwd | rev | cut -d '/' -f 1 | rev)
FUNCTION = $(PROJECT)
REGION = us-west-1
TIMESTAMP=$(shell date +%s)
SHORT_COMMIT=$(shell git rev-parse --short HEAD)
VERSIONED_PACKAGE=${PROJECT}_${TIMESTAMP}_${SHORT_COMMIT}.zip

all: build clean

.PHONY: clean build

clean:
	rm -rf build

build: clean
	mkdir -p build/site-packages
	zip -r artefacts/$(VERSIONED_PACKAGE) main.py
	python3 -m venv build/$(FUNCTION)
	. build/$(FUNCTION)/bin/activate; \
	pip3 install  -r requirements.txt; \
	cp -r $$VIRTUAL_ENV/lib/python3.9/site-packages/ build/site-packages
	cd build/site-packages; zip -g -r ../../artefacts/$(VERSIONED_PACKAGE) . -x "*__pycache__*"
