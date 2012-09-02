#!/usr/bin/env python
# -*- coding: utf-8 -*-
__docformat__ = 'restructuredtext en'

import os
import re

ref = re.M|re.I|re.U

from minitage.recipe.common.common import which

def pycairo(options,buildout):
    cwd = os.getcwd()
    if not os.path.isfile(options['configure']):
        options['configure'] = which(options['configure'])
    os.chdir(options['compile-directory'])
    os.environ['PYTHON']=  options['configure']
    os.environ['PYTHON_CONFIG'] = which((os.path.basename(options['configure'])
                                         + '-config'))
    os.environ['PYTHONARCHDIR'] = options['prefix']
    cmds = [
        '%s %s%s %s' % (
            options['configure'],
            options['prefix-option'],
            options['prefix'],
            options['configure-options']
        ),
        '%s waf %s' % (
            options['configure'], 'build'

        ),
        '%s waf %s' % (
            options['configure'], 'install'
        ),
    ]
    for cmd in cmds:
        print "Running %s"  % cmd
        ret = os.system(cmd)
        if ret != 0:
            raise Exception('%s did not run' % cmd)

    os.chdir(cwd)



# vim:set et sts=4 ts=4 tw=80:
