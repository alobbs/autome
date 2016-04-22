import plugin

when, lapse = "3am", "24h"
ldap = plugin.get("ldap")


def run():
    ldap.update_cache()
