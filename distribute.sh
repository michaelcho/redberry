#!/usr/bin/env bash

###########
# A script to distribute this package to PyPi
###########

VERSION=(`cat VERSION`)
echo "Prepping to distribute $VERSION..."

rm dist/*
python setup.py sdist bdist_wheel
git tag v$VERSION
git push --tags
twine upload dist/*
