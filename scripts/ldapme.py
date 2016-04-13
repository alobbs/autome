import plugin

LOG = plugin.logger(__name__)
ldap = plugin.get("ldap")
lapse = 1300


def run():
    LOG.debug("starting")
    LOG.debug(ldap.find('Alvaro'))
    LOG.debug("finishing")
