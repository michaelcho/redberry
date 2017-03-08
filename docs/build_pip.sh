#!/usr/bin/env bash

version=`cat VERSION`
echo "Building v$version..."

rm dist/*
python setup.py sdist
python setup.py bdist_wheel

twine upload dist/*
git tag v$version
git push --tags

echo "Build complete!"
