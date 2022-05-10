.DEFAULT_GOAL := help

SRC_DIR := src/call_throttle
PKG_DEPS := requirements.txt

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

install: $(PKG_DEPS)  ## Install build dependencies
	python -m pip install --upgrade -r $(PKG_DEPS)

build: $(SRC_DIR)  ## Build package
	python -m build

upload: dist  ## Upload package to PyPI
	python3 -m twine upload $(ARGS) dist/*

clean:  ## Clean project tree
	rm -rf build 2> /dev/null
	find . -type d \( -name '__pycache__' -o -name '*.egg-info' \) -exec rm -rf {} \; 2> /dev/null

.PHONY: help install build upload clean
