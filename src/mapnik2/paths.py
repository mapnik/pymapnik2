import os
from mapnik_utils import mapnik_config, which

inputpluginspath = None
fontscollectionpath = None
mapniklibpath = None
mapnik_config_executable = None

if not mapnik_config_executable:
    mapnik_config_executable = which('mapnik-config')

if not inputpluginspath:
    inputpluginspath = mapnik_config(['--plugins'])

if not fontscollectionpath:
    fontscollectionpath = mapnik_config(['--fonts'])

if not mapniklibpath:
    mapniklibpath = os.path.join(mapnik_config(['--prefix']), 'lib64')
    if not os.path.exists(mapniklibpath):
        mapniklibpath = os.path.join(mapnik_config(['--prefix']), 'lib')
        if not os.path.exists(mapniklibpath):
            mapniklibpath = os.path.dirname(inputpluginspath)
            if not os.path.exists(mapniklibpath):
                raise Exception('Cant find mapnik lib dir path!')

