import plugin

ldap, ldap_rh = plugin.get("ldap", "ldap_redhat")
LOG = plugin.logger(__name__)

when, lapse = '9am', '24h'


def run():
    for search in ["James Whitehurst", "mrc", "Perry M", "lpeer", "Alvaro Lopez Ortega", "jpena", "Michal Pryc"]:
        chain = ldap.get_report_chain(search)
        LOG.debug(search)
        LOG.debug(" * Level: %s" % ldap_rh.get_search_weight(search))
        LOG.debug(" * Chain: [%s] %s" % (len(chain), ' '.join(chain)))
