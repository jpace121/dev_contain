#!/usr/bin/env bash
set -ex

mkdir -p /tmp/dev_contain_build/dev-contain
cp -r ./* /tmp/dev_contain_build/dev-contain

pushd .
cd /tmp/dev_contain_build/dev-contain

debuild -us -uc -b

popd
