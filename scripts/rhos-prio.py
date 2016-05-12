import bridge
import plugin

PRIO = "rhos-prio-list@redhat.com"
FWD_FROM = "aortega@redhat.com"
FWD_TO = "alvaro@alobbs.com"

lapse = "5m"
imap, smtp, tele = plugin.get("imap", "smtp", "telegram")


def run():
    # [!!] for msg in imap.get_new_msgs('INBOX', '(TEXT alvaro@alobbs.com)'):
    for msg in imap.get_new_msgs('INBOX', '(TO %s)' % PRIO):
        smtp.forward_msg(msg, FWD_FROM, FWD_TO)
        tele.send_me_msg(bridge.email.to_text(msg))
