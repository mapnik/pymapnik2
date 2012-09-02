import os
import sys
from setuptools import setup, find_packages, extension

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
# BBB: needed for non standard pyairo.h to be found
cf = ' '.join(compilation_flags['includes'])
ldf = ' '.join(compilation_flags['extra_link_args'])
os.environ['CFLAGS'] = cf
os.environ['LDFLAGS'] = ldf

# pycairo does not play well with setuptools
# the user may install it himself
#for lib in compilation_flags['extra_link_args']:
#    if 'cairo' in lib:
#        dep = 'pycairo'
#        if sys.version_info[0] < 3:
#            dep = 'py2cairo'
#        install_requires.append(dep)
#        break

version = '2.1.0.2.dev0'
if 'MAPNIK_DEBUG' in os.environ:
    summary(compilation_flags)
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
            extra_compile_args = compilation_flags.get('includes', []),
            libraries = compilation_flags.get('libraries', []),
            extra_link_args = compilation_flags.get('extra_link_args', []),
        ),
    ],
    install_requires=['setuptools'],
    test_suite = 'nose.collector',
    entry_points={},
)
