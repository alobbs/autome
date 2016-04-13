import plugin

ldap = plugin.get("ldap")
lapse = "24h"


def run():
    ldap.update_cache()
