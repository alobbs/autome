import plugin
ldap = plugin.get("ldap")


TITLE_WEIGHTS = [
 ("ceo", 500),
 ("exeutive vice president", 140),
 ("senior vice president", 120),
 ("vice president", 100),
 ("senior director", 80),
 ("director", 70),
 ('senior manager', 50),
 ('associate manager', 20),
 ('tax', 40),
 ('treasury', 40),
 ('credit', 40),
 ('payroll', 40),
 ('bid desk', 40),
 ('administrative assistant', 40),
 ('office administrator', 40),
 ('executive assistant', 40),
 ('manager', 40),
 ('senior principal', 40),
 ('purchasing', 30),
 ('principal', 30),
 ('security', 30),
 ('consultant', 20),
 ('senior', 20),
 ('marketing', 20),
 ('writer', 10),
 ('software', 10),
 ('quality engineer', 10),
 ('web', 10),
]


class LDAP_RedHat:
    @staticmethod
    def get_title_weight(title):
        title = title.lower()
        for t, w in TITLE_WEIGHTS:
            if t in title:
                return w

        print("WARNING:", title)
        return 0

    def get_search_weight(self, search):
        ret = ldap.find(search)
        if not len(ret):
            return 0

        ret_title = ret[0].get('attributes', {}).get('title')
        if not ret_title or not len(ret_title):
            return 0

        return self.get_title_weight(ret_title[0])
