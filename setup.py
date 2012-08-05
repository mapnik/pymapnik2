import os
import sys

from setuptools import setup, find_packages, extension

# we do not have the module installed yet.
mapnik_utils = {}
exec open('src/mapnik/utils.py').read() in mapnik_utils
read = mapnik_utils['read']
get_compilation_flags = mapnik_utils['get_compilation_flags']

README = read(('README.rst',))
CHANGELOG = read(('CHANGES.rst',))
long_description = '\n'.join([README, CHANGELOG])+'\n'

compilation_flags = get_compilation_flags()
sources_dir = os.path.abspath('cpp')
agg_sources_dir = os.path.join(os.path.abspath('agg'), 'include')
files = [os.path.join('cpp', f)
         for f in os.listdir(sources_dir)
         if f.endswith('.cpp')]

install_requires=['setuptools',]
test_requires = ['nose']
for lib in compilation_flags['extra_link_args']:
    if 'cairo' in lib:
        dep = 'pycairo'
        if sys.version_info[0] < 3:
            dep = 'py2cairo'
        install_requires.append(dep)
        break

version = '2.0.1.3'
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
