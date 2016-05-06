import time

import plugin
util = plugin.get("util")


def run():
    n = 0
    while True:
        time.sleep(2)
        n += 1
