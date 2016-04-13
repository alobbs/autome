import os

import ujson as json


def get_path(component):
    path = "~/.autome/{}.json".format(component)
    return os.path.expanduser(path)


def get(component):
    with open(get_path(component), 'r') as f:
        return json.load(f)


def get_var_path(component):
    # Path
    basepath = "/usr/local/var/lib/autome"
    vardir = os.path.join(basepath, component)

    # Make sure it exists
    if not os.path.exists(vardir):
        os.makedirs(vardir)

    return vardir
