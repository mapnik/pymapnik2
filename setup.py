import os
import re
import sys
from setuptools import setup, find_packages, extension

reflags = re.X|re.S|re.U
# we do not have the mapnik.utils module installed yet
# just load it with exec
mapnik_utils = {}
exec open('src/mapnik/utils.py').read() in mapnik_utils
read = mapnik_utils['read']
get_compilation_flags = mapnik_utils['get_compilation_flags']
summary = mapnik_utils['summary']

README = read(('README.rst',))
CHANGELOG = read(('CHANGES.rst',))
long_description = '\n'.join([README, CHANGELOG])+'\n'

sources_dir = os.path.abspath('cpp')
agg_sources_dir = os.path.join(
    os.path.abspath('agg'), 'include')
files = [os.path.join('cpp', f)
         for f in os.listdir(sources_dir)
         if f.endswith('.cpp')]

compilation_flags = get_compilation_flags()

cf = ('%s %s' % (
    ' '.join(compilation_flags['includes']),
    os.environ.get('CFLAGS', ''),
)).replace('  ', '').strip()
cfp = cf.split()
cfpp = []
for idx, i in enumerate(cfp[:]):
    add = True
    if i.startswith('-I/'):
        if i.endswith('/bin'):
            add = False
        if i in cfpp:
            add = False
    if add:
        cfpp.append(i)
cf = ' '.join(cfpp)

ldf = ('%s %s' % (
    ' '.join(compilation_flags['extra_link_args']),
    os.environ.get('LDFLAGS', ''),
)).replace('  ', '').strip()
ldfp = ldf.split()
ldfpp = []
for idx, i in enumerate(ldfp[:]):
    add = True
    if i.startswith('-L/'):
        if i.endswith('/bin'):
            add = False
    if i.startswith('-L/') or i.startswith('-l'):
        if i in ldfpp:
            add = False
    if add:
        ldfpp.append(i)
ldf = ' '.join(ldfpp)
## filter rpath
# ldf = re.sub('-Wl,-rpath -Wl,[^ ]* ', '' , ldf, reflags)
# ldf = ldf.replace('  ', '').strip()

os.environ['LDFLAGS'] = os.environ['CFLAGS'] = ''

version = '2.2.0'
if 'MAPNIK_DEBUG' in os.environ:
    summary(compilation_flags)
    print "CFLAGS: %s\n" % cf
    print "LDFLAGS: %s\n" % ldf

install_requires=['setuptools',]
test_requires = ['nose']
setup(
    name='mapnik2',
    version = version,
    description="Python bindings for mapnik",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Mathieu Le Marec - Pasquet & the mapnik community',
    author_email='kiorky@cryptelium.net',
    url='http://pypi.python.org/pypi/mapnik',
    license='LGPL',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    extras_require={'tests': test_requires},
    ext_modules = [
        extension.Extension(
            "_mapnik", files,
            include_dirs=[sources_dir, agg_sources_dir],
            extra_compile_args = cf.split(),
            libraries = compilation_flags.get('libraries', []),
            extra_link_args = ldf.split(),
        ),
    ],
    install_requires=['setuptools'],
    test_suite = 'nose.collector',
    entry_points={},
)
