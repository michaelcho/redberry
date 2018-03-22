#!/usr/bin/env bash

###########
# A script to distribute this package to PyPi
###########

VERSION=(`cat VERSION`)

# Assumes we are bumping from 0.0.1.3 to 0.0.1.4
VERSION_STRING=(`cat VERSION | sed 's/\(.*\)\..*/\1/'`)     # eg 0.0.1
MINOR_VERSION=(`cat VERSION | cut -d "." -f4`)              # eg 3
NEXT_MINOR_VERSION=$((MINOR_VERSION+1))                     # eg 4
NEXT_VERSION="$VERSION_STRING.$NEXT_MINOR_VERSION"          # eg 0.0.1.4

echo "======"
echo "Prepping to distribute $VERSION..."

rm dist/*
python setup.py sdist bdist_wheel
git tag v$VERSION
git push --tags
twine upload dist/*

echo "======"
echo "Bumping from $VERSION to $NEXT_VERSION ...."

git push origin :dev/$VERSION
git checkout -b dev/$NEXT_VERSION
git branch -D dev/$VERSION
echo "$NEXT_VERSION" > VERSION
echo -e "__v$NEXT_VERSION - TBC__  \n... add notes here ...\n\n$(cat CHANGELOG.md)" > CHANGELOG.md
git commit -am "start $NEXT_VERSION"
git push

echo "Complete!"
