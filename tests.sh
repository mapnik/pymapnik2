#!/usr/bin/env bash
cd $(dirname $0)
./bin/nosetests $@ 2>&1 
# vim:set et sts=4 ts=4 tw=80:
