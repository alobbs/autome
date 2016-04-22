import os

import plugin

util = plugin.get("util")
when, lapse = '4am', '12h'
GIT = "https://github.com/alobbs/hosts-adblock.git"


def run():
    with util.work_in_tmpdir():
        os.system('git clone --depth=1 %s' % GIT)
        os.system("./hosts-adblock/update-upload.py")
