import logging
import os

import yapsy.PluginManager

_mgr = None


def manager():
    global _mgr

    if not _mgr:
        # Path to plugins
        here = os.path.dirname(os.path.abspath(__file__))
        plugins_dir = os.path.join(here, "plugins")

        # Plugin manager
        _mgr = yapsy.PluginManager.PluginManager()
        _mgr.setPluginPlaces([plugins_dir])

    # Refresh
    _mgr.collectPlugins()
    _mgr.all = {p.plugin_object.__class__.__name__.lower():
                p.plugin_object for p in _mgr.getAllPlugins()}
    return _mgr


def _get_one(name):
    mgr = manager()
    if name.lower() not in mgr.all:
        return None

    return mgr.all.get(name.lower())


def get(*args):
    if len(args) == 1:
        return _get_one(*args)
    else:
        return tuple([_get_one(s) for s in args])


def logger(script_name):
    # Logging file
    log_fname = "{}.log".format(script_name)
    dirfp = os.path.expanduser("~/.autome/logs")
    log_fp = os.path.join(dirfp, log_fname)

    # Logger
    fstring = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fstring)

    handler = logging.FileHandler(log_fp)
    handler.setFormatter(formatter)

    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger
