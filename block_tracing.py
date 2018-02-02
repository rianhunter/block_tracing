import ctypes
import ctypes.util
import sys

def unix_errcheck(result, func, args):
    if result:
        raise OSError(ctypes.get_errno(), os.strerror(ctypes.get_errno()))
    return result

if sys.platform.startswith('linux'):
    libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
    prctl_proto = ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.c_ulong,
        use_errno=True,
    )
    prctl = prctl_proto(("prctl", libc))
    prctl.errcheck = unix_errcheck

    PR_SET_DUMPABLE = 4

    def block_tracing():
        prctl(PR_SET_DUMPABLE, 0, 0, 0, 0)

    BLOCK_TRACING_INHERITS = True
elif sys.platform == 'darwin':
    libc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('c'))
    ptrace_proto = ctypes.CFUNCTYPE(
        ctypes.c_int,
        ctypes.c_int, # request
        ctypes.c_int,  # pid
        ctypes.POINTER(ctypes.c_char), # addr
        ctypes.c_int, # data
        use_errno=True,
    )
    ptrace = ptrace_proto(("ptrace", libc))

    PT_DENY_ATTACH = 31

    def block_tracing():
        ctypes.set_errno(0)
        ptrace(PT_DENY_ATTACH, 0, None, 0)
        errno = ctypes.get_errno()
        if errno:
            raise OSError(errno, os.strerror(errno))

    BLOCK_TRACING_INHERITS = False
else:
    def block_tracing():
        raise NotImplementedError()

    BLOCK_TRACING_INHERITS = False
