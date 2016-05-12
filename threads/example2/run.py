#!/usr/bin/env python3

import sys
import time

CRASH = False

for n in range(1, sys.maxsize):
    if CRASH and n % 100 == 0:
        0/0
    time.sleep(.05)
