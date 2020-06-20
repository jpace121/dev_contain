#!/usr/bin/env bash
set -x

# Build tar file
python3 setup.py sdist

# Make build root.
mkdir -p /tmp/rpm/BUILD
mkdir -p /tmp/rpm/RPMS
mkdir -p /tmp/rpm/SOURCES
mkdir -p /tmp/rpm/SPECS
mkdir -p /tmp/rpm/SRPMS

# Copy to sources.
cp dist/dev_contain-5.0.3.tar.gz /tmp/rpm/SOURCES/.
# Copy spec file
cp rpm/dev-contain.spec /tmp/rpm/SPECS/.

# Build.
rpmbuild --define '_topdir /tmp/rpm' -ba /tmp/rpm/SPECS/dev-contain.spec
