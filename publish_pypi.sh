#!/bin/bash

.venv/bin/python setup.py sdist bdist_wheel
twine upload --skip-existing dist/*
