import random
import time

import plugin
vpn = plugin.get("vpn")


def run():
    while True:
        vpn.connect()
        time.sleep(random.randint(10, 30))
