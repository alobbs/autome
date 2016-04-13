import os
import shutil
import tempfile

when = '4am'
lapse = '24h'
GIT = "https://github.com/alobbs/hosts-adblock.git"


def run():
    orid = os.getcwd()
    tmpd = tempfile.mkdtemp()
    os.chdir(tmpd)

    os.system('git clone --depth=1 %s' % GIT)
    os.system("./hosts-adblock/update-upload.py")

    os.chdir(orid)
    shutil.rmtree(tmpd)
