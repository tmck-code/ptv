.PHONY: poc
poc:
	./docs/poc/poc.sh

.PHONY: test
test:
	python3 -m unittest

.PHONY: build
build:
	docker build -f ops/Dockerfile -t ptv .

.PHONY: shell
shell:
	docker run -e PTV_USER_ID -e PTV_API_KEY -it ptv bash

