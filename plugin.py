import imp
import logging
import os

_shared_objs = {}


def _get_one(name):
    global _shared_objs

    # Build path
    here = os.path.dirname(os.path.abspath(__file__))
    plugins_dir = os.path.join(here, "plugins")
    filepath = os.path.join(plugins_dir, '%s.py' % name)

    # Load plug-in
    with open(filepath, 'r') as f:
        p = imp.load_module(name, f, filepath, ('py', 'r', imp.PY_SOURCE))

    # Cached obj?
    if name in _shared_objs:
        return _shared_objs[name]

    obj = None
    for n in dir(p):
        if n.lower() == name.lower():
            obj = getattr(p, n)()

    assert obj, "Class not found"

    # Cache obj?
    is_shared = getattr(obj, "SHARED_OBJ", False)
    if is_shared:
        _shared_objs[name] = obj

    return obj


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
