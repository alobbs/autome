import bridge
import plugin

FWD_FROM = "aortega@redhat.com"
FWD_TO = "alvaro@alobbs.com"

lapse = 1300
imap, smtp, tele = plugin.get("imap", "smtp", "telegram")


def run():
    for msg in imap.get_new_msgs('INBOX', '(TEXT alvaro@alobbs.com)'):
        smtp.forward_msg(msg, FWD_FROM, FWD_TO)
        tele.send_me_msg(bridge.email.to_text(msg))
