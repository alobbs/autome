import contextlib
import os
import shutil
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

    @staticmethod
    @contextlib.contextmanager
    def tmpdir_fp(**kw):
        path = tempfile.mkdtemp(**kw)
        yield path
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

    @staticmethod
    @contextlib.contextmanager
    def work_in_tmpdir(**kw):
        # Pre: Get dir, Create new, cd it
        orig = os.getcwd()
        path = tempfile.mkdtemp(**kw)
        os.chdir(path)
        yield path

        # Post: Go back, rm -rf tmp dir
        os.chdir(orig)
        try:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass
