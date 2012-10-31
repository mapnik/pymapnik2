import sys

import re
import os
from subprocess import Popen, PIPE, CalledProcessError
from ctypes import CDLL




# backport to py<27
 
def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    'ls: non_existent_file: No such file or directory\n'
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = Popen(stdout=PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output)
    return output

         

def read(rnames):
    setupdir = os.getcwd()
    return open(
        os.path.join(setupdir, *rnames)
    ).read()

def exit(code):
    if code != 0:
        sys.exit(-1)

def which(program,
          environ=None,
          key = 'PATH',
          split = ':'):
    if not environ:
        environ = os.environ
    PATH=environ.get(key, '').split(split)
    for entry in PATH:
        fp = os.path.abspath(os.path.join(entry, program))
        if os.path.exists(fp):
            return fp
        if (sys.platform.startswith('win') or sys.platform.startswith('cyg'))  and os.path.exists(fp+'.exe'):
            return fp+'.exe'
    raise IOError('Program not found: %s in %s ' % (program, PATH))

def get_config_output(exe, args):
    cmd = which(exe)
    cmd = ' '.join([which(exe)]+args)
    ret = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    if ret.wait() != 0:
        raise Exception(
            '%s error: %s\n%s' % (
                cmd,
                ret.stdout.read(),
                ret.stderr.read(),
            )
        )
    return ret.stdout.read().strip()

def pkg_config(args):
    return get_config_output('pkg-config', args)
def mapnik_config(args):
    return get_config_output('mapnik-config', args)

def get_boost_flags():
    includes = []
    libraries = []
    # add ubuntu python version to search paths
    ver = sys.version[:3].replace('.', '')
    libraries_pretendants = {
        'boost_regex' :[
            'boost_regex',
            'boost_regex-mt',
        ],
        'boost_python': [
            "boost_python-gcc",
            "boost_python",
            "boost_python-mt",
            'boost_python-py%s' % ver,
            'boost_python-mt-py%s' % ver,
        ],
        'boost_thread': [
            "boost_thread",
            "boost_thread-mt",
        ],

    }
    if 'MAPNIK2_BOOST_PYTHON' in os.environ:
        libraries_pretendants['boost_python'] = [
            os.environ['MAPNIK2_BOOST_PYTHON'].split(':')
        ]
    if sys.platform == "win32" :
        libraries.extend(
            "boost_python-mgw",
        )
    else:

        for p in libraries_pretendants:
            prefix = 'lib'
            suffix = 'so'
            if sys.platform == 'cygwin':
                prefix = 'cyg'
            if sys.platform == 'darwin':
                suffix = 'dylib'
            elif os.name == 'nt':
                suffix = 'dll'
            pretendants = libraries_pretendants[p]
            while(True):
                try:
                    pr = pretendants.pop()
                    if ".%s"%suffix in pr:
                        pr = re.sub(".%s.*"%suffix, '', pr)
                    if pr.startswith(prefix):
                        pr = pr[len(prefix):]
                    dll = CDLL('%s%s.%s' % (prefix, pr, suffix))
                    libraries.append(pr)
                    break
                except OSError:
                    pass
                except IndexError:
                    raise Exception('Cant find boost_python lib!')
    return {'includes': includes, 'libraries': libraries}

def get_cairo_flags():
    macros = []
    libraries = []
    includes = []
    links = []
    try:
        cairo = pkg_config(['--modversion cairo'])
        HAS_CAIRO = True
        includes.append('-DHAVE_CAIRO')
        links.append(
            pkg_config(['--libs cairo'])
        )
        includes.append(
            pkg_config(['--cflags cairo'])
        )
    except:
       HAS_CAIRO = False
    if HAS_CAIRO:
        try:
            import cairo
            HAS_PYCAIRO = True
            links.append(
                pkg_config(['--libs pycairo'])
            )
            includes.append(
                pkg_config(['--cflags pycairo'])
            )
            includes.append('-DHAVE_PYCAIRO')
        except:
            HAS_PYCAIRO = False

    return {'macros': macros, 'extra_link_args': links,
            'includes': includes, 'libraries': libraries}


def add_multiarch_paths(flags):
    '''
    Find multiarchs specifics paths for Debian/Ubuntu.
    See https://wiki.ubuntu.com/MultiarchSpec
    Could be fixed in Scons and/or mapnik-utils
    '''
    try:
        arch = check_output(['dpkg-architecture', '-qDEB_HOST_MULTIARCH'])
        arch = arch[:-1] if arch.endswith('\n') else arch
        flags['includes'].append('-I/usr/lib/%s/sigc++-2.0/include' % arch)
    except:
        pass

def get_compilation_flags():
    compilation_flags = {
        'macros': [],
        'includes': [],
        'libraries': ['jpeg', 'png'],
        'extra_link_args': [],
    }
    bf = get_boost_flags()
    cf = get_cairo_flags()
    if not bf['libraries']:
        sys.stderr.write('Warning: libboost_python not found')
    compilation_flags['includes'].extend(
        mapnik_config(["--cflags"]).split())
    compilation_flags['extra_link_args'].extend(
        mapnik_config(["--libs"]).split())
    compilation_flags['macros'].extend(   cf['macros'])
    compilation_flags['includes'].extend( cf['includes'])
    compilation_flags['libraries'].extend(cf['libraries'])
    compilation_flags['extra_link_args'].extend(
        cf['extra_link_args'])
    compilation_flags['includes'].extend(bf['includes'])
    compilation_flags['libraries'].extend(bf['libraries'])
    if sys.platform.startswith("linux"):
        add_multiarch_paths(compilation_flags)
    for key in compilation_flags:
        for idx, i in enumerate(compilation_flags[key][:]):
            compilation_flags[key][idx] = (
                compilation_flags[key][idx].replace('\n', '')
            )
    return compilation_flags

def summary(compilation_flags=None):
    if not compilation_flags:
        compilation_flags = get_compilation_flags()
    print "*"*80
    print "pymapnik will be built with those flags:"
    print "-"*50
    print "INCLUDES: "
    print "\t"+" ".join(
        compilation_flags.get('includes', []))
    print "LIBRARIES: "
    print "\t-l"+" -l".join(
        compilation_flags.get('libraries', []))
    print "EXTRA LINK ARGS: "
    print "\t"+" ".join(
        compilation_flags.get('extra_link_args', []))
    print "-"*50
    try:
        import cairo
        print "PYCAIRO SUPPORT ENABLED"
    except:
        print ("PYCAIRO SUPPORT DISABLED"
               ", this is optional but you can"
               " install pycairo & rerun mapnik install")
    print "*"*80

