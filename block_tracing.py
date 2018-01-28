import ctypes
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
else:
    def block_tracing():
        raise NotImplementedError()
