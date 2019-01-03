.PHONY: poc
poc:
	./docs/poc/poc.sh

.PHONY: test
test:
	python3 -m unittest

