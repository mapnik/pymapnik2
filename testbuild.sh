#!/usr/bin/env bash


cd $(dirname $0)
export MAKEOPT="-j6"

rm -rf  build dist/ src/_mapnik.so src/mapnik2.egg-info/;
build() {
    bin/buildout setup ./setup.py bdist_egg 2>&1
}
build>build.log


