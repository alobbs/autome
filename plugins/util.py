import contextlib
import os
import sys
import tempfile

from yapsy.IPlugin import IPlugin


class Util(IPlugin):
    def __init__(self):
        super().__init__()

    @staticmethod
    def screenshot(path):
        if sys.platform == 'darwin':
            os.system("screencapture %s" % path)
        else:
            os.system("import -window root %s" % path)

    @staticmethod
    @contextlib.contextmanager
    def tmp_fp(**kw):
        fd, path = tempfile.mkstemp(**kw)
        yield path
        try:
            os.close(fd)
            os.unlink(path)
        except FileNotFoundError:
            pass
