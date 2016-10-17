#!/usr/bin/env sh

find tests/* -type d -exec python3 -m unittest discover -s {} -p '*_tests.py' \;