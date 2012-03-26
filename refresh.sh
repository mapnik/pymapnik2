#!/usr/bin/env bash
# Copyright (C) 2010, Mathieu PASQUET <mpa@makina-corpus.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the <ORGANIZATION> nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING INANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
frsync() {
    echo rsync $@
    rsync $@
} 
w="${1:-../../Source/mapnik}"
egg=$(dirname $0) 
cd $egg
# refresh code
rm -rf cpp;mkdir cpp
cp -vrf $w/bindings/python/*pp cpp/
frsync -a  ${w}/deps/agg/include/ agg/include/
# refresh tests
frsync -a  ${w}/tests/python_tests/ src/mapnik2/tests/python_tests/
for i in $(find src/mapnik2/tests/ -name '*.py');do
    #sed -re "s/\.\.\/data/\.\/data/g" -i $i
    sed -re "s/from utilities/from mapnik2.tests.python_tests.utilities/g" -i $i
done
# refresh test resources
frsync -a --delete  ${w}/tests/data/ src/mapnik2/tests/data/

# vim:set et sts=4 ts=4 tw=0:
