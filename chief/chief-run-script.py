#!/usr/bin/env python3

import argparse
import logging
import os
import sys

import cron

# PYTHONPATH
dir_chief = os.path.dirname(os.path.realpath(__file__))
dir_base = os.path.realpath(__file__ + "/../..")
sys.path += [dir_chief, dir_base]


def main():
    # Parse parameters
    parser = argparse.ArgumentParser()
    parser.add_argument("script", help="Fullpath to script")
    args = parser.parse_args()

    # Run script
    m = cron.load(args.script)
    logging.basicConfig(stream=sys.stdout)
    m.run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
