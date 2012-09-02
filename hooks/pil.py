#add minitage libraries to search pathes
import os
import re
import platform
HAS_WINDOWS = (('windows' in platform.system().lower()
                or ('cygwin' in platform.system().lower())))

ref = re.M|re.I|re.U
def pil(options,buildout):
    cwd = os.getcwd()
    os.chdir(
        options['compile-directory']
    )
    ccwd = os.getcwd()
    # make a .libs folder containing symlink to dyn libs
    # to link  with
    libs = os.path.join(ccwd, 'libs')
    libdir = '/usr'
    # this will support multiarch users like ubuntu64 ones
    # to link and comppile PIL
    # it is not harmful for other archs
    # as we wont do any broken symlink
    if not HAS_WINDOWS:
        os.
        libdirt = '/usr/lib/x86_64-linux-gnu'
        if os.path.isdir(libdirt):
            for needed in ['libz.so',
                           'libjpeg.so',
                           'libfreetype.so',]:




            libdir = libdirt
    locations = {
        'freetype': buildout.get('freetype', {}).get(
            'location', libdir
        ),
        'jpeg': buildout.get('libjpeg', {}).get (
            'location', libdir
        ),
        'tiff': buildout.get('libtiff', {}).get(
            'location', libdir
        ),
        'zlib': buildout.get('zlib', {}).get(
            'location', libdir
        ),
    }
    st = open('setup.py').read()
    locations['include'] = '/usr/include'
    pregex = [
        ("^(FREETYPE_ROOT.*)$",
         "FREETYPE_ROOT='%(freetype)s' , '%(include)s'"% (
             locations),
        ("^(TIFF_ROOT.*)$",
         "TIFF_ROOT='%(tiff)s', '%(include)s'"%locations),
        ("^(JPEG_ROOT.*)$",
         "JPEG_ROOT='%(jpeg)s', '%(include)s'"%locations),
        ("^(ZLIB_ROOT.*)$",
         "ZLIB_ROOT='%(zlib)s', '%(include)s'"%locations),
    ]
    for p, rep in pregex:
        r= re.compile(p, ref)
        st = r.sub(rep, st)
    open('setup.py', 'w').write(st)
    os.chdir(cwd)
