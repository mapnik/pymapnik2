from setuptools import setup, find_packages
import os

version = '0.7_r2271'

def read(rnames):
    setupdir =  os.path.dirname( os.path.abspath(__file__))
    return open(
        os.path.join(setupdir, *rnames)
    ).read()

README =read((os.path.dirname(__file__),'README.txt'))
INSTALL =read((os.path.dirname(__file__),'docs', 'INSTALL.txt'))
CHANGELOG  = read((os.path.dirname(__file__), 'docs', 'HISTORY.txt'))
tdt = """
Tests & docs
==============
"""
TESTS  = '%s' % (
    '\n'
)
long_description = '\n'.join([README,
                              INSTALL,
                              CHANGELOG])+'\n'
setup(
    name='mapnik',
    version=version,
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
    namespace_packages=['mapnik', ],
    include_package_data=True,
    zip_safe=False,
    extras_require={'test': ['ipython', 'zope.testing', 'lxml', 'zope.testbrowser', ]},
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    install_requires=[
        'setuptools',
        'pycairo',
    ],
    entry_points={
        'paste.app_factory': ['cgwb_app=collective.generic.webbuilder.webserver:wsgi_app_factory',],
        'console_scripts': ['cgwb=collective.generic.webbuilder.webserver:main',],
        'paste.paster_create_template': [
        ],
    },
)

