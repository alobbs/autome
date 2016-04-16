#!/usr/bin/env python3

import conf

import argparse
import time

import requests
import tabulate

CLEAR = "\x1b[2J\x1b[1;1H"


def get(path):
    url = "http://localhost:{}".format(conf.CHIEF_API_PORT)
    r = requests.get(url + path)
    return r.json()


def table(info, *a, **ka):
    if 'tablefmt' not in ka:
        ka['tablefmt'] = "fancy_grid"

    if type(info) == dict:
        info = [list(i) for i in info.items()]
        return tabulate.tabulate(info, [], *a, **ka)
    elif type(info) == list and type(info[0] == dict):
        headers = sorted(info[0].keys())
        values = []
        for e in info:
            values.append([e[k] for k in headers])
        return tabulate.tabulate(values, headers, *a, **ka)

    return tabulate.tabulate(info, *a, **ka)


def do(args):
    now = time.strftime("%h %d, %H:%M")
    if args.cmd == "jobs":
        print(now + '\n' + table(get("/jobs/list")))
    elif args.cmd == "run":
        assert args.job, "--job required"
        url = "/jobs/run/{}".format(args.job)
        print(now + '\n' + table(get(url)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["jobs", "run", "ping"])
    parser.add_argument("--auto", type=int)
    parser.add_argument("--job")
    args = parser.parse_args()

    try:
        do(args)
        while args.auto:
            time.sleep(args.auto)
            print(CLEAR)
            try:
                do(args)
            except requests.exceptions.ConnectionError:
                now = time.strftime("%h %d, %H:%M")
                print(now + " - [ERROR] Autome API server not reachable")
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
