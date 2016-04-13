import bridge
import plugin

FWD_FROM = "aortega@redhat.com"
FWD_TO = "alvaro@alobbs.com"

imap, smtp, tele = plugin.get("imap", "smtp", "telegram")

lapse = 1300

def run():
    for msg in imap.get_new_msgs('INBOX', '(TEXT alvaro@alobbs.com)'):
        smtp.forward_msg(msg, FWD_FROM, FWD_TO)
        tele.send_me_msg(bridge.email.to_text(msg))
