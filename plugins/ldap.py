import os
import shutil

import ldap3
import pluginconf
import ujson as json
from yapsy.IPlugin import IPlugin

FIND_ATTRIBUTES = ('cn', 'mail', 'displayName', 'givenName', 'sn', 'uid')


class LDAP(IPlugin):
    def __init__(self):
        super().__init__()
        self._objs = None

        # Read conf
        self.conf = pluginconf.get('ldap')

    def _get_cache_fp(self):
        cachedir = os.path.expanduser("~/.autome/cache")
        return os.path.join(cachedir, "%s.json" % self.conf['host'])

    def update_cache(self):
        # Fetch
        conn = ldap3.Connection(self.conf['host'], auto_bind=True)
        conn.search(self.conf['search'], '(objectClass=*)', attributes='*')
        ldap_json = ','.join([e.entry_to_json() for e in conn.entries])

        # Write to a new file
        fp = self._get_cache_fp()
        fp_new = fp + '.new'

        with open(fp_new, 'w+') as f:
            f.write('[ ')
            f.write(ldap_json)
            f.write(' ]')

        # Overwrite when it's done
        shutil.move(fp_new, fp)

    @property
    def objs(self):
        if not self._objs:
            with open(self._get_cache_fp(), 'r') as f:
                self._objs = json.load(f)
        return iter(self._objs)

    def find_by_dn(self, dn):
        for o in self.objs:
            if o.get('dn') == dn:
                return o

    def find_by_attr(self, attr, s):
        found = []
        for o in self.objs:
            attrs = o.get('attributes', {})
            if s in attrs.get(attr, [''])[0]:
                found.append(o)
                continue
        return found

    def find(self, s):
        found = []
        for k in FIND_ATTRIBUTES:
            for f in self.find_by_attr(k, s):
                if f not in found:
                    found.append(f)
        return found

    def __iter__(self):
        return self.objs
        return iter(self._objs)

    def get_report_chain(self, search):
        levels = []
        found = self.find(search)[0]
        ma = found.get('attributes', {}).get('manager', [None])[0]

        while ma:
            levels.append(ma)
            found = self.find_by_dn(ma)
            ma = found.get('attributes', {}).get('manager', [None])[0]

        return levels
