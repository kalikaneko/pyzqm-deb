"""CFFI backend (for PyPY)"""

# Copyright (C) PyZMQ Developers
# Distributed under the terms of the Modified BSD License.

import imp
import os.path
import sys

import cffi.vengine_cpy
import cffi.vengine_gen
_ma_triplet = None

def vengine_gen_find_module(self, module_name, path, so_suffixes):
    global _ma_triplet
    if _ma_triplet is None:
        try:
            import subprocess as sp
            p = sp.Popen(["gcc", "-print-multiarch"], stdout=sp.PIPE)
            _ma_triplet = str(p.communicate()[0].decode().strip())
        except:
            import warnings
            warnings.warn('failed to detect multiarch paths, please install gcc')

    for so_suffix in so_suffixes + ['.%s-%s.so' % (imp.get_tag(), _ma_triplet)]:
        basename = module_name + so_suffix
        if path is None:
            path = sys.path
            # import from non root package would try __pycache__ which is
            # cleaned by pypy installation
            path.insert(0, "/usr/lib/pypy/dist-packages/zmq/backend/cffi")
        for dirname in path:
            filename = os.path.join(dirname, basename)
            if os.path.isfile(filename):
                return filename


cffi.vengine_gen.VGenericEngine.find_module = vengine_gen_find_module

from zmq.backend.cffi import (constants, error, message, context, socket,
                           _poll, devices, utils)

__all__ = []
for submod in (constants, error, message, context, socket,
               _poll, devices, utils):
    __all__.extend(submod.__all__)

from .constants import *
from .error import *
from .message import *
from .context import *
from .socket import *
from .devices import *
from ._poll import *
from ._cffi import zmq_version_info, ffi
from .utils import *
