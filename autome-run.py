import glob
import importlib.machinery
import logging
import os
import time
import math

LOGGING_ARGS = {'level': logging.INFO,
                'datefmt': '%H:%M:%S',
                'format': '%(asctime)s [%(levelname)s] %(message)s'}


def load(filepath):
    filename = os.path.basename(filepath)
    modname = filename.replace('.py', '')
    loader = importlib.machinery.SourceFileLoader(modname, filepath)
    return loader.load_module()


class Runnable:
    def __init__(self, script_filename):
        logging.info("loading {}".format(script_filename))
        self.script = load(script_filename)
        self.time_next = time.time() + self.script.lapse

    def sleep(self):
        to_sleep = math.ceil(max(0, self.time_next - time.time()))
        logging.info("sleep {}".format(to_sleep))
        time.sleep(to_sleep)

    def run(self):
        logging.info("{}.run()".format(self.script.__name__))
        re = self.script.run()
        self.time_next = time.time() + self.script.lapse
        return re


class Runner:
    def __init__(self):
        self.scripts = []

    def load(self, *args):
        self.scripts += [Runnable(*args)]

    def _find_run_next(self):
        self.scripts = sorted(self.scripts, key=lambda r: r.time_next)
        return self.scripts[0]

    def step(self):
        runnable = self._find_run_next()
        runnable.sleep()
        runnable.run()


def main():
    logging.basicConfig(**LOGGING_ARGS)

    runner = Runner()
    for e in glob.glob("scripts/*.py"):
        runner.load(e)

    while True:
        runner.step()


if __name__ == '__main__':
    main()
