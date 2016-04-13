import plugin

when = '9am'
lapse = '24h'
telegram = plugin.get("telegram")


def msg_received():
    None


def run():
    telegram.msg_received_cb = msg_received
