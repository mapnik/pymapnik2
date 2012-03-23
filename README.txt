==========================
Introduction
==========================

.. contents::


Official mapnik bindings repackaged in the distutils way to facilitate deployments.

Credits
=========

Companies
----------------
|makinacom|_

* `Planet Makina Corpus <http://www.makina-corpus.org>`_
* `Contact us <mailto:python@makina-corpus.org>`_

.. |makinacom| image:: http://depot.makina-corpus.org/public/logo.gif
.. _makinacom:  http://www.makina-corpus.com

Authors
---------------

Contributors
---------------

    - kiorky <kiorky@cryptelium.net>

Installation
======================================
Prerequisites
-------------------

Don't forget that you can play with LDFLAGS/CFLAGS/LD_LIBRARY_PATH dto indicate non standart locations for the following requirements if it applies.

You will have to have the includes and libraries for

    - The new mapnik-config utility to be in your $PATH
    - Boost_python linked to your python interpreter
      If it is not installed in standart envionments, you ll have to handle the CFLAGS/LDFLAGS to find it, or use minitage ;)
    - cairo / cairomm (optionnal but enabled if you compiled mapnik with cairo support)
    - mapnik2
    - The current python interpreter

Easy_install with or without virtualenv
---------------------------------------------
* Say where to find mapnik-config by settings correctly your PATH environment variable
* When you're reading this you have probably already run
  ``easy_install mapnik2``. Find out how to install setuptools
  (and EasyInstall) here:
  http://peak.telecommunity.com/DevCenter/EasyInstall

::

        virtualenv --no-site-packages test
        source test/bin/activate
        easy_install mapnik2

If your boost python installation is not in a standart place, just set the [LD_LIBRARY_PATH, LDFLAGS, CFLAGS] to find it.


Buildout
----------
Some developers use buildout_ to ease deployments.
* Say where to find mapnik-config by settings correctly your PATH environment variable
* Add ``mapnik`` to the list of eggs to install, e.g.
::

    [buildout]
    parts = somepart

    [somepart]
    recipe = minitage.recipe.scripts
    ...
    # (options like include dirs)
    ...
    eggs =
        ...
        mapnik2

* Re-run buildout, e.g. with::

    $ ./bin/buildout

You can read the buildout installation shipped with this egg for inspiration.

Minitage
--------------
Some developers use minitage_ to ease deployments (a layer upon buildout).
Indeed, it takes care a lot of things like those boring compilation flags.
As an example, to work on this egg in development mode, you can boostrap it by doing this::
::

    easy_install -U virtualenv
    virtualenv --no-site-packages --distribute ~/minitage
    mkdir ~/minitage/others

    source ~/minitage/bin/activate

Install minitage, if you haven't yet :
::

    easy_install -U minitage.core

Initialize it (**mandatory**) :
::

    minimerge -s

To install the minilay for the mapnik2 egg development you can do
::
    
    cd  ~/minitage/others
    git clone https://github.com/mapnik/pymapnik2.git mapnik-egg
    ln -fs ~/minitage/others/mapnik-egg/minilays/mapnik-egg/  ~/minitage/minilays/mapnik-egg 
    minimerge -av mapnik-egg
    

Enjoy your installation
::

    cd ~/minitage/others/mapnik-egg
    ./bin/mypy
    >>> import mapnik2

.. _minitage: http://www.minitage.org
.. _buildout: http://buildout.org
.. _pythonproducts: http://plone.org/products/pythonproducts
