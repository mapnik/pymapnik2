import os

from setuptools import setup, find_packages, extension

# we do not have the module installed yet.
mapnik_utils = {}
exec open('src/mapnik_utils.py').read() in mapnik_utils
read = mapnik_utils['read']
get_compilation_flags = mapnik_utils['get_compilation_flags']

README = read(('README.txt',))
INSTALL = read(('docs', 'INSTALL.txt'))
RELEASE = read(('docs', 'RELEASE.txt'))
CHANGELOG  = read(('docs', 'HISTORY.txt'))
long_description = '\n'.join([README, INSTALL,  RELEASE, CHANGELOG])+'\n'

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
        install_requires.append('pycairo')
        break

setup(
    name='mapnik',
    version= '0.7_r2271',
    description="Python bindings for mapnik",
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='',
    author='Mathieu Pasquet',
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
            "_mapnik2", files,
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
