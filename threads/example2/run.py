#!/usr/bin/env python3

import sys
import time

for n in range(1, sys.maxsize):
    print("test #{}".format(n))
    if n % 100 == 0:
        CRASH = 1/0
    time.sleep(.05)
