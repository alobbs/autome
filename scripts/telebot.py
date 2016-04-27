import time
import types

import plugin
import telepot
import telepot.namedtuple

when = '9am'
telegram = plugin.get("telegram")


def msg_cb(self, msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print("content_type, chat_type, chat_id", content_type, chat_type, chat_id)

    k = telegram.Keyboard()
    if content_type == 'location':
        print("location", msg['location'])
        k.hide_keyboard()
        self.bot.sendMessage(chat_id, **k.get_message_params("Got it!"))
    else:
        k.add('Plain text')
        k.add('Phone', request_contact=True)
        k.add('Location', request_location=True)
        self.bot.sendMessage(chat_id, **k.get_message_params("This is custom keyboard"))


def run():
    telegram.msg_received_cb = types.MethodType(msg_cb, telegram)

    while True:
        time.sleep(60)
