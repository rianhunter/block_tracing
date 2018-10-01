# This file is part of block_tracing

# Copyright (c) 2018 Rian Hunter

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
