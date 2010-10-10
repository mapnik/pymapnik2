import sys
import os
from subprocess import Popen, PIPE
from ctypes import CDLL

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
    raise IOError('Program not fond: %s in %s ' % (program, PATH))

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

def mapnik_config(args):
    return get_config_output('mapnik-config', args)

def get_boost_flags():
    includes = []
    libraries = []
    libraries_pretendants = {
        'boost_python': [
            "boost_python-gcc",
            "boost_python",
        ],
    }
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
            if 'win' in sys.platform:
                suffix = 'dll'
            pretendants = libraries_pretendants[p]
            while(len(pretendants)):
                try:
                    pr = pretendants.pop()
                    dll = CDLL('%s%s.%s' % (prefix, pr, suffix))
                    libraries.append(pr)
                    break
                except OSError:
                    pass
                except IndexError:
                  raise Exception('Cant find boost_python lib!')
    return {'includes': includes, 'libraries': libraries}

def get_compilation_flags():
    compilation_flags = {
        'includes': [],
        'libraries': ['jpeg', 'png'],
        'extra_link_args': [],
    }
    bf = get_boost_flags()
    compilation_flags['includes'].extend(bf['includes'])
    compilation_flags['libraries'].extend(bf['libraries'])
    compilation_flags['includes'].extend(mapnik_config(["--cflags"]).split())
    compilation_flags['extra_link_args'].extend(mapnik_config(["--libs"]).split())
    return compilation_flags


